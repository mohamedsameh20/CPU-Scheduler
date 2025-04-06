import tkinter as tk
from tkinter import ttk
from threading import Thread, Lock
import time

# ======= Scheduler Configuration =======
TIME_QUANTUM = 2
TIME_UNIT = 1  #1 second per unit
process_id_counter = 1
processes = []
lock = Lock()
current_time = 0
running = False
static_mode = False

# ======= Scheduler Logic =======
def round_robin_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        # Sort the queue based on priority (lower priority value means higher priority)
        queue.sort(key=lambda p: p['priority'])

        if queue:
            process = queue.pop(0)
            execute_time = min(TIME_QUANTUM, process['remaining_time'])
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()

def FCFS_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that have arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
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

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()

def Preemptive_SJF_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that have arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        # Sort the queue based on remaining time (shortest first)
        queue.sort(key=lambda p: p['remaining_time'])

        if queue:
            process = queue.pop(0)
            execute_time = min(TIME_QUANTUM, process['remaining_time'])
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    
def Non_Preemptive_SJF_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that have arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        # Sort the queue based on remaining time (shortest first)
        queue.sort(key=lambda p: p['remaining_time'])

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

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    
def preemptive_priority_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that have arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        # Sort the queue based on priority (lower priority value means higher priority)
        queue.sort(key=lambda p: (p['priority'], p['remaining_time']))

        if queue:
            process = queue.pop(0)
            execute_time = min(TIME_QUANTUM, process['remaining_time'])
            update_gantt(f"Time {current_time}-{current_time + execute_time}: P{process['Process']}")
            draw_gantt_block(process['Process'], current_time, execute_time)

            for _ in range(execute_time):
                if not static_mode:
                    time.sleep(TIME_UNIT)
                current_time += 1
                process['remaining_time'] -= 1
                update_table()

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    
def non_preemptive_priority_scheduler(update_gantt, update_table, update_metrics, draw_gantt_block):
    global current_time, running
    queue = []
    current_time = 0
    running = True

    while running:
        with lock:
            # Get processes that have arrived and are not yet completed and not in queue
            arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
            for p in arrivals:
                queue.append(p)
                p['in_queue'] = True

        # Sort the queue based on priority (lower priority value means higher priority)
        queue.sort(key=lambda p: (p['priority'], p['remaining_time']))

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

                with lock:
                    arrivals = [p for p in processes if p['arrival_time'] <= current_time and not p['in_queue'] and not p['completed']]
                    for p in arrivals:
                        queue.append(p)
                        p['in_queue'] = True

            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completed'] = True
                process['completion_time'] = current_time
        else:
            if not static_mode:
                time.sleep(TIME_UNIT)
            current_time += 1

    update_metrics()
    
# ======= GUI Setup =======
def start_scheduler(live=True):
    global static_mode
    static_mode = not live
    Thread(target=round_robin_scheduler, args=(update_gantt_chart, update_burst_table, update_metrics, draw_gantt_block)).start()

def add_process():
    global process_id_counter
    burst = int(entry_burst.get())
    arrival = int(entry_arrival.get())
    priority = int(entry_priority.get())

    with lock:
        processes.append({
            'Process': process_id_counter,
            'arrival_time': arrival,
            'burst_time': burst,
            'remaining_time': burst,
            'priority': priority,  # Add priority field
            'completed': False,
            'in_queue': False
        })
        process_id_counter += 1

    entry_burst.delete(0, tk.END)
    entry_arrival.delete(0, tk.END)
    entry_priority.delete(0, tk.END)  # Clear the priority input
    update_burst_table()

def update_gantt_chart(text):
    gantt_output.insert(tk.END, text + '\n')
    gantt_output.see(tk.END)

def update_burst_table():
    for row in tree.get_children():
        tree.delete(row)
    for p in processes:
        tree.insert('', tk.END, values=(p['Process'], p['arrival_time'], p['burst_time'], p['remaining_time'], p['priority'], "Yes" if p['completed'] else "No"))

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

# ======= Gantt Chart Drawing =======
gantt_x = 10

def draw_gantt_block(Process, start, duration):
    global gantt_x
    color = f"#{(Process * 123456) % 0xFFFFFF:06x}"
    canvas.create_rectangle(gantt_x, 10, gantt_x + 40 * duration, 60, fill=color)
    canvas.create_text(gantt_x + 20 * duration, 35, text=f"P{Process}")
    canvas.create_text(gantt_x, 65, text=str(start), anchor='n')
    gantt_x += 40 * duration
    canvas.create_text(gantt_x, 65, text=str(start + duration), anchor='n')

# ======= Reset Scheduler Function =======
def reset_scheduler():
    global processes, process_id_counter, current_time, running, gantt_x
    processes = []
    process_id_counter = 1
    current_time = 0
    running = False
    gantt_x = 10

    for row in tree.get_children():
        tree.delete(row)
    gantt_output.delete(1.0, tk.END)
    canvas.delete("all")
    avg_wt.set("")
    avg_tt.set("")

# ======= Main Window =======
root = tk.Tk()
root.title("Process Scheduler")
root.geometry("1200x600")


# ======= Frame for Inputs =======
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

# ======= Entry Fields and Labels =======
entry_burst = tk.Entry(frame_inputs, width=10)
entry_burst.grid(row=0, column=1)
entry_arrival = tk.Entry(frame_inputs, width=10)
entry_arrival.grid(row=0, column=3)
entry_priority = tk.Entry(frame_inputs, width=10)
entry_priority.grid(row=0, column=5)

label_burst = tk.Label(frame_inputs, text="Burst Time")
label_burst.grid(row=0, column=0)
label_arrival = tk.Label(frame_inputs, text="Arrival Time")
label_arrival.grid(row=0, column=2)
label_priority = tk.Label(frame_inputs, text="Priority")
label_priority.grid(row=0, column=4)

# ======= Buttons =======
# UI menu for choosing the scheduler type
scheduler_menu = tk.StringVar(value="Round Robin")
scheduler_options = ["Round Robin", "FCFS", "Preemptive SJF", "Non-Preemptive SJF", "Preemptive Priority", "Non-Preemptive Priority"]
scheduler_menu.set(scheduler_options[0])
scheduler_menu = tk.OptionMenu(frame_inputs, scheduler_menu, *scheduler_options)
scheduler_menu.grid(row=0, column=10, padx=10)

btn_add = tk.Button(frame_inputs, text="Add Process", command=add_process)
btn_add.grid(row=0, column=6, padx=10)
btn_start = tk.Button(frame_inputs, text="Start (Live)", command=lambda: start_scheduler(True))
btn_start.grid(row=0, column=7, padx=10)
btn_static = tk.Button(frame_inputs, text="Start (Static)", command=lambda: start_scheduler(False))
btn_static.grid(row=0, column=8, padx=10)

# ======= Reset Button =======
btn_reset = tk.Button(frame_inputs, text="Reset", command=reset_scheduler)
btn_reset.grid(row=0, column=9, padx=10)

# ======= Burst Time Table =======
tree = ttk.Treeview(root, columns=('Process', 'Arrival', 'Burst', 'Remaining', 'Priority', 'Done'), show='headings')
tree.heading('Process', text='Process')
tree.heading('Arrival', text='Arrival Time')
tree.heading('Burst', text='Burst Time')
tree.heading('Remaining', text='Remaining')
tree.heading('Priority', text='Priority')
tree.heading('Done', text='Completed')
tree.pack(pady=10)

# ======= Gantt Chart Output (Textual and Visual) =======
gantt_output = tk.Text(root, height=15, width=60)
gantt_output.pack(pady=5)

canvas = tk.Canvas(root, height=100, width=1200, bg='white')
canvas.pack()

# ======= Metrics Output =======
avg_wt = tk.StringVar()
avg_tt = tk.StringVar()
label_wt = tk.Label(root, textvariable=avg_wt)
label_tt = tk.Label(root, textvariable=avg_tt)
label_wt.pack()
label_tt.pack()

# Start the main GUI loop
root.mainloop()
