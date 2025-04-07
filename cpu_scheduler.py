import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Lock
import time

# ======= Scheduler Configuration =======
TIME_UNIT = 1  # 1 second per unit
process_id_counter = 1
processes = []
lock = Lock()
current_time = 0
running = False
static_mode = False
current_quantum = 2


# ======= Scheduler Logic =======
def check_completion():
    return all(p['completed'] for p in processes)


def round_robin_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        if queue:
            process = queue.pop(0)
            execute_time = min(current_quantum, process['remaining_time'])
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                with lock:
                    arrivals = [p for p in processes if
                                p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

                if check_completion():
                    running = False
                    break

            if process['remaining_time'] > 0 and running:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

        if not running:
            break

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


def FCFS_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        if queue:
            process = queue.pop(0)
            execute_time = process['remaining_time']
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                if check_completion():
                    running = False
                    break

            process['completed'] = True
            process['completion_time'] = current_time

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

        if not running:
            break

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


def Preemptive_SJF_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        queue.sort(key=lambda p: (p['remaining_time'], p['Process']))

        if queue:
            process = queue.pop(0)
            execute_time = 1
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1
            process['remaining_time'] -= 1
            update_table()

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time

            with lock:
                new_arrivals = [p for p in processes if
                                p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in new_arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


def Non_Preemptive_SJF_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        queue.sort(key=lambda p: (p['remaining_time'], p['Process']))

        if queue:
            process = queue.pop(0)
            execute_time = process['remaining_time']
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                if check_completion():
                    running = False
                    break

            process['completed'] = True
            process['completion_time'] = current_time

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


def preemptive_priority_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        queue.sort(key=lambda p: (p['priority'], p['remaining_time'], p['Process']))

        if queue:
            process = queue.pop(0)
            execute_time = 1
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1
            process['remaining_time'] -= 1
            update_table()

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time

            with lock:
                new_arrivals = [p for p in processes if
                                p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                for p in new_arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


def non_preemptive_priority_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            arrivals = [p for p in processes if
                        p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        queue.sort(key=lambda p: (p['priority'], p['remaining_time'], p['Process']))

        if queue:
            process = queue.pop(0)
            execute_time = process['remaining_time']
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                if check_completion():
                    running = False
                    break

            process['completed'] = True
            process['completion_time'] = current_time

            if check_completion():
                running = False
                break
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    if check_completion():
        root.after(100, lambda: messagebox.showinfo("Simulation Complete",
                                                    f"All processes completed!\nTotal time: {current_time} units"))


# ======= GUI Setup =======
def update_input_fields(*_):
    scheduler_name = scheduler_var.get()
    priority_required = scheduler_name in ["Preemptive Priority", "Non-Preemptive Priority"]
    quantum_required = scheduler_name == "Round Robin"

    label_priority.grid() if priority_required else label_priority.grid_remove()
    entry_priority.grid() if priority_required else entry_priority.grid_remove()
    label_quantum.grid() if quantum_required else label_quantum.grid_remove()
    entry_quantum.grid() if quantum_required else entry_quantum.grid_remove()


def start_scheduler(live=True):
    global static_mode, current_quantum, running
    if running:
        messagebox.showwarning("Already Running", "Scheduler is already running!")
        return

    static_mode = not live

    try:
        if scheduler_var.get() == "Round Robin":
            current_quantum = max(1, int(entry_quantum.get()))
    except ValueError:
        current_quantum = 2
        entry_quantum.delete(0, tk.END)
        entry_quantum.insert(0, "2")

    scheduler_name = scheduler_var.get()
    scheduler_func = {
        "Round Robin": round_robin_scheduler,
        "FCFS": FCFS_scheduler,
        "Preemptive SJF": Preemptive_SJF_scheduler,
        "Non-Preemptive SJF": Non_Preemptive_SJF_scheduler,
        "Preemptive Priority": preemptive_priority_scheduler,
        "Non-Preemptive Priority": non_preemptive_priority_scheduler
    }.get(scheduler_name)

    if not processes:
        messagebox.showerror("No Processes", "Add at least one process before starting!")
        return

    for widget in [btn_add, btn_start, btn_static, scheduler_menu]:
        widget['state'] = 'disabled'

    Thread(target=scheduler_func,
           args=(update_gantt_chart, update_burst_table, update_metrics, draw_gantt_block)).start()


def safe_add_process():
    global process_id_counter

    try:
        burst = int(entry_burst.get())
        arrival = int(entry_arrival.get())
        if burst <= 0 or arrival < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Valid burst (≥1) and arrival (≥0) times required!")
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

    entry_burst.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    if scheduler_var.get() in ["Preemptive Priority", "Non-Preemptive Priority"]:
        entry_priority.delete(0, tk.END)
    update_burst_table()


def reset_scheduler():
    global processes, process_id_counter, current_time, running, gantt_x
    running = False
    time.sleep(0.2)

    processes = []
    process_id_counter = 1
    current_time = 0
    gantt_x = 10

    for row in tree.get_children():
        tree.delete(row)
    gantt_output.delete(1.0, tk.END)
    canvas.delete("all")
    avg_wt.set("")
    avg_tt.set("")

    entry_burst.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_priority.delete(0, tk.END)
    entry_quantum.delete(0, tk.END)
    entry_quantum.insert(0, "2")

    for widget in [btn_add, btn_start, btn_static, scheduler_menu]:
        widget['state'] = 'normal'


def update_gantt_chart(text):
    gantt_output.insert(tk.END, text + '\n')
    gantt_output.see(tk.END)


def update_burst_table():
    for row in tree.get_children():
        tree.delete(row)
    for p in processes:
        tree.insert('', tk.END, values=(
            p['Process'], p['arrival_time'], p['burst_time'], p['remaining_time'], p['priority'],
            "Yes" if p['completed'] else "No"))


def update_metrics():
    total_wait = 0
    total_turnaround = 0
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


gantt_x = 10


def draw_gantt_block(Process, start, duration):
    global gantt_x
    color = f"#{(Process * 123456) % 0xFFFFFF:06x}"
    canvas.create_rectangle(gantt_x, 10, gantt_x + 40 * duration, 60, fill=color)
    canvas.create_text(gantt_x + 20 * duration, 35, text=f"P{Process}")
    canvas.create_text(gantt_x, 65, text=str(start), anchor='n')
    gantt_x += 40 * duration
    canvas.create_text(gantt_x, 65, text=str(start + duration), anchor='n')


# ======= Main Window =======
root = tk.Tk()
root.title("Process Scheduler")
root.geometry("1200x800")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# Input Fields
label_burst = tk.Label(frame_inputs, text="Burst Time")
label_burst.grid(row=0, column=0)
entry_burst = tk.Entry(frame_inputs, width=10)
entry_burst.grid(row=0, column=1)

label_arrival = tk.Label(frame_inputs, text="Arrival Time")
label_arrival.grid(row=0, column=2)
entry_arrival = tk.Entry(frame_inputs, width=10)
entry_arrival.grid(row=0, column=3)

label_priority = tk.Label(frame_inputs, text="Priority")
entry_priority = tk.Entry(frame_inputs, width=10)

label_quantum = tk.Label(frame_inputs, text="Quantum")
entry_quantum = tk.Entry(frame_inputs, width=10)
entry_quantum.insert(0, "2")

# Scheduler Selection
scheduler_var = tk.StringVar(value="Round Robin")
scheduler_options = ["Round Robin", "FCFS", "Preemptive SJF", "Non-Preemptive SJF",
                     "Preemptive Priority", "Non-Preemptive Priority"]
scheduler_menu = tk.OptionMenu(frame_inputs, scheduler_var, *scheduler_options, command=update_input_fields)
scheduler_menu.grid(row=0, column=9, padx=10)

# Buttons
btn_add = tk.Button(frame_inputs, text="Add Process", command=safe_add_process)
btn_add.grid(row=0, column=4, padx=10)
btn_start = tk.Button(frame_inputs, text="Start (Live)", command=lambda: start_scheduler(True))
btn_start.grid(row=0, column=5, padx=10)
btn_static = tk.Button(frame_inputs, text="Start (Static)", command=lambda: start_scheduler(False))
btn_static.grid(row=0, column=6, padx=10)
btn_reset = tk.Button(frame_inputs, text="Reset", command=reset_scheduler)
btn_reset.grid(row=0, column=7, padx=10)

# Process Table
tree = ttk.Treeview(root, columns=('Process', 'Arrival', 'Burst', 'Remaining', 'Priority', 'Done'), show='headings')
tree.heading('Process', text='Process')
tree.heading('Arrival', text='Arrival Time')
tree.heading('Burst', text='Burst Time')
tree.heading('Remaining', text='Remaining')
tree.heading('Priority', text='Priority')
tree.heading('Done', text='Completed')
tree.pack(pady=10)

# Gantt Chart
gantt_output = tk.Text(root, height=8, width=60)
gantt_output.pack(pady=5)
canvas = tk.Canvas(root, height=100, width=1200, bg='white')
canvas.pack()

# Metrics
avg_wt = tk.StringVar()
avg_tt = tk.StringVar()
tk.Label(root, textvariable=avg_wt).pack()
tk.Label(root, textvariable=avg_tt).pack()

update_input_fields()
root.mainloop()