import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Lock
import time

# ======= Global Configuration =======
TIME_UNIT = 1
process_id_counter = 1
processes = []
lock = Lock()
current_time = 0.0
running = False
started = False
static_mode = False
current_quantum = 2.0
last_gantt_end = 0.0
gantt_x = 10


def check_completion():
    return all(p['completed'] for p in processes)


def reset_process_states():
    with lock:
        for p in processes:
            p['remaining_time'] = p['burst_time']
            p['completed'] = False
            p['in_queue'] = False


def draw_gantt_block(process, start, duration):
    global gantt_x, last_gantt_end
    color = "#CCCCCC" if process == -1 else f"#{(process * 123456) % 0xFFFFFF:06x}"
    text = "IDLE" if process == -1 else f"P{process}"

    if start > last_gantt_end:
        gap_duration = start - last_gantt_end
        canvas.create_rectangle(gantt_x, 10, gantt_x + 40 * gap_duration, 60,
                                fill="#EEEEEE", outline="black")
        canvas.create_text(gantt_x + 20 * gap_duration, 35, text="IDLE")
        gantt_x += 40 * gap_duration

    block_width = 40 * duration
    canvas.create_rectangle(gantt_x, 10, gantt_x + block_width, 60,
                            fill=color, outline="black")
    canvas.create_text(gantt_x + (block_width / 2), 35, text=text)
    canvas.create_text(gantt_x, 65, text=f"{start:.1f}", anchor='n')
    gantt_x += block_width
    canvas.create_text(gantt_x, 65, text=f"{start + duration:.1f}", anchor='n')
    last_gantt_end = start + duration


def round_robin_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()

    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            if queue:
                process = queue.pop(0)
                execute_time = min(float(current_quantum), process['remaining_time'])

                if current_time > last_gantt_end:
                    draw_gantt_block(-1, last_gantt_end, current_time - last_gantt_end)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = current_time

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


def FCFS_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()

    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: x['arrival_time'])

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if current_time > last_gantt_end:
                    gap_duration = current_time - last_gantt_end
                    draw_gantt_block(-1, last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = current_time
                update_burst_table()

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


def Preemptive_SJF_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()

    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = 1.0  # Preemption interval

                if current_time > last_gantt_end:
                    gap_duration = current_time - last_gantt_end
                    draw_gantt_block(-1, last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = current_time

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


def Non_Preemptive_SJF_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()
    
    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if current_time > last_gantt_end:
                    gap_duration = current_time - last_gantt_end
                    draw_gantt_block(-1, last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = current_time
                update_burst_table()

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


def preemptive_priority_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()

    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['priority'], x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = 1.0  # Preemption interval

                if current_time > last_gantt_end:
                    gap_duration = current_time - last_gantt_end
                    draw_gantt_block(-1, last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = current_time

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


def non_preemptive_priority_scheduler():
    global started, current_time, running, gantt_x, last_gantt_end
    queue = []
    current_time = 0.0
    last_gantt_end = 0.0
    gantt_x = 10
    running = True
    reset_process_states()

    while started:
        while running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['priority'], x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if current_time > last_gantt_end:
                    gap_duration = current_time - last_gantt_end
                    draw_gantt_block(-1, last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], current_time, execute_time)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + execute_time:.1f}: P{process['Process']}")

                if not static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = current_time
                update_burst_table()

                if check_completion():
                    running = False
                    started = False
            else:
                idle_duration = 1.0
                if not static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, current_time, idle_duration)
                update_gantt_chart(f"Time {current_time:.1f}-{current_time + idle_duration:.1f}: IDLE")
                current_time += idle_duration

            if not running:
                break

    root.after(100, on_scheduler_complete)


# ======= GUI Functions =======
def update_input_fields(*_):
    scheduler_name = scheduler_var.get()
    priority_required = scheduler_name in ["Preemptive Priority", "Non-Preemptive Priority"]
    quantum_required = scheduler_name == "Round Robin"

    label_priority.grid() if priority_required else label_priority.grid_remove()
    entry_priority.grid() if priority_required else entry_priority.grid_remove()
    label_quantum.grid() if quantum_required else label_quantum.grid_remove()
    entry_quantum.grid() if quantum_required else entry_quantum.grid_remove()


def start_scheduler(live=True):
    global started, static_mode, current_quantum, running, gantt_x, last_gantt_end
    if started:
        if running:

            btn_start.config(text="Resume")
            running = False
            return

        else:
            btn_start.config(text="Pause")
            running = True
            return

    # Clear previous Gantt visualization

    started = True
    btn_start.config(text="Pause")
    gantt_x = 10
    last_gantt_end = 0.0
    canvas.delete("all")
    gantt_output.delete(1.0, tk.END)

    static_mode = not live

    try:
        if scheduler_var.get() == "Round Robin":
            current_quantum = max(0.1, float(entry_quantum.get()))
    except ValueError:
        current_quantum = 2.0
        entry_quantum.delete(0, tk.END)
        entry_quantum.insert(0, "2.0")

    scheduler_map = {
        "Round Robin": round_robin_scheduler,
        "FCFS": FCFS_scheduler,
        "Preemptive SJF": Preemptive_SJF_scheduler,
        "Non-Preemptive SJF": Non_Preemptive_SJF_scheduler,
        "Preemptive Priority": preemptive_priority_scheduler,
        "Non-Preemptive Priority": non_preemptive_priority_scheduler
    }

    if not processes:

        started = False
        btn_start.config(text="Start Live")
        messagebox.showerror("Error", "Add at least one process first!")

        return

    # toggle_start_buttons('disabled')
    reset_process_states()
    Thread(target=scheduler_map[scheduler_var.get()]).start()


def safe_add_process():
    global process_id_counter
    try:
        arrival = float(entry_arrival.get())
        burst = float(entry_burst.get())
        if burst <= 0 or arrival < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Invalid values!\nBurst must be > 0\nArrival must be ≥ 0")
        return

    priority = 0
    if scheduler_var.get() in ["Preemptive Priority", "Non-Preemptive Priority"]:
        try:
            priority = int(entry_priority.get())
        except ValueError:
            messagebox.showerror("Input Error", "Priority must be an integer!")
            return

    with lock:
        processes.append({
            'Process': process_id_counter,
            'arrival_time': arrival,
            'burst_time': burst,
            'remaining_time': burst,
            'priority': priority,
            'completed': False,
            'in_queue': False
        })
        process_id_counter += 1

    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    if scheduler_var.get() in ["Preemptive Priority", "Non-Preemptive Priority"]:
        entry_priority.delete(0, tk.END)
    update_burst_table()


def reset_scheduler(full=True):
    global started, processes, process_id_counter, running
    if started:
        btn_start.config(text="Start Live")
        started = False
        running = False

    time.sleep(0.2)

    if full:
        processes = []
        process_id_counter = 1
    else:
        reset_process_states()

    current_time = 0.0
    gantt_x = 10
    last_gantt_end = 0.0

    for row in tree.get_children():
        tree.delete(row)
    gantt_output.delete(1.0, tk.END)
    canvas.delete("all")
    avg_wt.set("")
    avg_tt.set("")

    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_quantum.delete(0, tk.END)
    entry_quantum.insert(0, "2.0")

    toggle_start_buttons('normal')


def update_gantt_chart(text):
    gantt_output.insert(tk.END, text + '\n')
    gantt_output.see(tk.END)


def update_burst_table():
    for row in tree.get_children():
        tree.delete(row)
    for p in processes:
        tree.insert('', tk.END, values=(
            p['Process'],
            f"{p['arrival_time']:.2f}",
            f"{p['burst_time']:.2f}",
            f"{p['remaining_time']:.2f}",
            p['priority'],
            "Yes" if p['completed'] else "No"
        ))


def update_metrics():
    total_wait = 0.0
    total_turnaround = 0.0
    count = 0
    for p in processes:
        if p['completed']:
            turnaround = p['completion_time'] - p['arrival_time']
            wait = turnaround - p['burst_time']
            total_turnaround += turnaround
            total_wait += wait
            count += 1
    if count > 0:
        avg_wt.set(f"Average Waiting Time: {total_wait / count:.2f}")
        avg_tt.set(f"Average Turnaround Time: {total_turnaround / count:.2f}")


def toggle_start_buttons(state):
    btn_start['state'] = state
    btn_static['state'] = state


def on_scheduler_complete():
    toggle_start_buttons('normal')
    update_metrics()
    if check_completion():
        btn_start.config(text="Start Live")
        messagebox.showinfo("Simulation Complete", "All processes finished execution!")


# ======= UI Setup =======
root = tk.Tk()
root.title("Advanced CPU Scheduler")
root.geometry("1200x850")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Swapped input fields (Arrival before Burst)
label_arrival = tk.Label(frame_inputs, text="Arrival Time:")
label_arrival.grid(row=0, column=0, padx=5)
entry_arrival = tk.Entry(frame_inputs, width=8)
entry_arrival.grid(row=0, column=1, padx=5)

label_burst = tk.Label(frame_inputs, text="Burst Time:")
label_burst.grid(row=0, column=2, padx=5)
entry_burst = tk.Entry(frame_inputs, width=8)
entry_burst.grid(row=0, column=3, padx=5)

label_priority = tk.Label(frame_inputs, text="Priority:")
entry_priority = tk.Entry(frame_inputs, width=8)

label_quantum = tk.Label(frame_inputs, text="Quantum:")
entry_quantum = tk.Entry(frame_inputs, width=8)
entry_quantum.insert(0, "2.0")

# Scheduler Selection
scheduler_var = tk.StringVar(value="Round Robin")
scheduler_menu = tk.OptionMenu(frame_inputs, scheduler_var,
                               "Round Robin", "FCFS",
                               "Preemptive SJF", "Non-Preemptive SJF",
                               "Preemptive Priority", "Non-Preemptive Priority",
                               command=update_input_fields)
scheduler_menu.grid(row=0, column=9, padx=10)

# Control Buttons
btn_add = tk.Button(frame_inputs, text="Add Process", command=safe_add_process)
btn_add.grid(row=0, column=4, padx=5)

btn_start = tk.Button(frame_inputs, text="Start Live", command=lambda: start_scheduler(True))
btn_start.grid(row=0, column=5, padx=5)






btn_static = tk.Button(frame_inputs, text="Start Static", command=lambda: start_scheduler(False))
btn_static.grid(row=0, column=6, padx=5)

btn_reset = tk.Button(frame_inputs, text="Full Reset", command=lambda: reset_scheduler(True))
btn_reset.grid(row=0, column=7, padx=5)



# Process Table
tree = ttk.Treeview(root, columns=('ID', 'Arrival', 'Burst', 'Remaining', 'Priority', 'Done'), show='headings')
tree.heading('ID', text='Process ID')
tree.heading('Arrival', text='Arrival Time')
tree.heading('Burst', text='Burst Time')
tree.heading('Remaining', text='Remaining')
tree.heading('Priority', text='Priority')
tree.heading('Done', text='Completed')
tree.column('ID', width=80)
tree.column('Arrival', width=100)
tree.column('Burst', width=100)
tree.column('Remaining', width=100)
tree.column('Priority', width=80)
tree.column('Done', width=80)
tree.pack(pady=10)

# Gantt Chart
gantt_frame = tk.Frame(root)
gantt_frame.pack(fill='x', padx=10, pady=5)
gantt_output = tk.Text(gantt_frame, height=8, width=40)
gantt_output.pack(side='left', fill='y')
canvas_container = tk.Frame(gantt_frame)
canvas_container.pack(side='right', fill='both', expand=True)
h_scroll = tk.Scrollbar(canvas_container, orient='horizontal')
h_scroll.pack(side='bottom', fill='x')
canvas = tk.Canvas(canvas_container, height=100, width=600, bg='white',
                   xscrollcommand=h_scroll.set, scrollregion=(0, 0, 2000, 100))  
canvas.pack(side='top', fill='both', expand=True)
h_scroll.config(command=canvas.xview)
canvas.configure(scrollregion=(0, 0, 3000, 100))

# Metrics Display
metrics_frame = tk.Frame(root)
metrics_frame.pack(pady=10)
avg_wt = tk.StringVar()
avg_tt = tk.StringVar()
tk.Label(metrics_frame, textvariable=avg_wt, font=('Arial', 10)).pack(side='left', padx=20)
tk.Label(metrics_frame, textvariable=avg_tt, font=('Arial', 10)).pack(side='left', padx=20)

update_input_fields()
root.mainloop()
