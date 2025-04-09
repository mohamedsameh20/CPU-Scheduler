import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread

from core import (
    processes, reset_process_states, process_id_counter, 
    lock, check_completion, current_quantum, static_mode
)
from visualization import init_visualization

# UI elements that will be initialized from main.py
root = None
tree = None
gantt_output = None
canvas = None
label_priority = None
entry_priority = None
label_quantum = None
entry_quantum = None
scheduler_var = None
btn_start = None
btn_static = None
entry_arrival = None
entry_burst = None
avg_wt = None
avg_tt = None

def init_ui_vars(root_ref, tree_ref, gantt_output_ref, canvas_ref, 
                 label_priority_ref, entry_priority_ref, label_quantum_ref, entry_quantum_ref,
                 scheduler_var_ref, btn_start_ref, btn_static_ref, entry_arrival_ref, entry_burst_ref, 
                 avg_wt_ref, avg_tt_ref):
    """Initialize UI variables from main.py"""
    global root, tree, gantt_output, canvas, label_priority, entry_priority
    global label_quantum, entry_quantum, scheduler_var, btn_start, btn_static
    global entry_arrival, entry_burst, avg_wt, avg_tt
    
    root = root_ref
    tree = tree_ref
    gantt_output = gantt_output_ref
    canvas = canvas_ref
    label_priority = label_priority_ref
    entry_priority = entry_priority_ref
    label_quantum = label_quantum_ref
    entry_quantum = entry_quantum_ref
    scheduler_var = scheduler_var_ref
    btn_start = btn_start_ref
    btn_static = btn_static_ref
    entry_arrival = entry_arrival_ref
    entry_burst = entry_burst_ref
    avg_wt = avg_wt_ref
    avg_tt = avg_tt_ref
    
    # Initialize visualization module
    init_visualization(canvas, gantt_output)

def update_input_fields(*_):
    """Update input fields based on scheduler selection"""
    scheduler_name = scheduler_var.get()
    priority_required = scheduler_name in ["Preemptive Priority", "Non-Preemptive Priority"]
    quantum_required = scheduler_name == "Round Robin"

    label_priority.grid() if priority_required else label_priority.grid_remove()
    entry_priority.grid() if priority_required else entry_priority.grid_remove()
    label_quantum.grid() if quantum_required else label_quantum.grid_remove()
    entry_quantum.grid() if quantum_required else entry_quantum.grid_remove()

def start_scheduler(live=True):
    """Start the CPU scheduler simulation"""
    import core
    
    if core.started:
        if core.running:
            btn_start.config(text="Resume")
            core.running = False
            return
        else:
            btn_start.config(text="Pause")
            core.running = True
            return

    # Clear previous Gantt visualization
    core.started = True
    btn_start.config(text="Pause")
    core.gantt_x = 10
    core.last_gantt_end = 0.0
    canvas.delete("all")
    gantt_output.delete(1.0, tk.END)

    core.static_mode = not live

    try:
        if scheduler_var.get() == "Round Robin":
            core.current_quantum = max(0.1, float(entry_quantum.get()))
    except ValueError:
        core.current_quantum = 2.0
        entry_quantum.delete(0, tk.END)
        entry_quantum.insert(0, "2.0")

    scheduler_map = {
        "Round Robin": "round_robin_scheduler",
        "FCFS": "FCFS_scheduler",
        "Preemptive SJF": "Preemptive_SJF_scheduler",
        "Non-Preemptive SJF": "Non_Preemptive_SJF_scheduler",
        "Preemptive Priority": "preemptive_priority_scheduler",
        "Non-Preemptive Priority": "non_preemptive_priority_scheduler"
    }

    if not processes:
        core.started = False
        btn_start.config(text="Start Live")
        messagebox.showerror("Error", "Add at least one process first!")
        return

    reset_process_states()
    
    # Import the scheduler function dynamically
    from schedulers import (
        round_robin_scheduler, FCFS_scheduler, Preemptive_SJF_scheduler,
        Non_Preemptive_SJF_scheduler, preemptive_priority_scheduler,
        non_preemptive_priority_scheduler
    )
    
    scheduler_functions = {
        "round_robin_scheduler": round_robin_scheduler,
        "FCFS_scheduler": FCFS_scheduler,
        "Preemptive_SJF_scheduler": Preemptive_SJF_scheduler,
        "Non_Preemptive_SJF_scheduler": Non_Preemptive_SJF_scheduler,
        "preemptive_priority_scheduler": preemptive_priority_scheduler,
        "non_preemptive_priority_scheduler": non_preemptive_priority_scheduler
    }
    
    scheduler_func = scheduler_functions[scheduler_map[scheduler_var.get()]]
    core.running = True  # Set running to True before starting the thread
    Thread(target=scheduler_func).start()

def safe_add_process():
    """Add a process with validation"""
    global process_id_counter
    import core
    
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
            'Process': core.process_id_counter,
            'arrival_time': arrival,
            'burst_time': burst,
            'remaining_time': burst,
            'priority': priority,
            'completed': False,
            'in_queue': False
        })
        core.process_id_counter += 1

    entry_arrival.delete(0, tk.END)
    entry_burst.delete(0, tk.END)
    if scheduler_var.get() in ["Preemptive Priority", "Non-Preemptive Priority"]:
        entry_priority.delete(0, tk.END)
    update_burst_table()

def reset_scheduler(full=True):
    """Reset the scheduler state"""
    import core
    
    if core.started:
        btn_start.config(text="Start Live")
        core.started = False
        core.running = False

    time.sleep(0.2)

    if full:
        processes.clear()
        core.process_id_counter = 1
    else:
        reset_process_states()

    core.current_time = 0.0
    core.gantt_x = 10
    core.last_gantt_end = 0.0

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

def update_burst_table():
    """Update the process table with current process states"""
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
    """Calculate and update average waiting and turnaround time metrics"""
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
    """Enable or disable start buttons"""
    btn_start['state'] = state
    btn_static['state'] = state

def on_scheduler_complete():
    """Handle actions when scheduler completes execution"""
    toggle_start_buttons('normal')
    update_metrics()
    if check_completion():
        btn_start.config(text="Start Live")
        messagebox.showinfo("Simulation Complete", "All processes finished execution!")