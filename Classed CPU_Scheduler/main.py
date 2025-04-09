import tkinter as tk
from tkinter import ttk
from core import processes, TIME_UNIT, reset_process_states
from gui_functions import (
    update_input_fields, safe_add_process, start_scheduler, 
    reset_scheduler, update_burst_table
)

def main():
    global root, tree, gantt_output, canvas, label_priority, entry_priority
    global label_quantum, entry_quantum, scheduler_var, btn_start, btn_static
    global entry_arrival, entry_burst, avg_wt, avg_tt
    
    # ======= UI Setup =======
    root = tk.Tk()
    root.title("Advanced CPU Scheduler")
    root.geometry("1200x850")

    frame_inputs = tk.Frame(root)
    frame_inputs.pack(pady=10)

    # Input fields
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
    canvas = tk.Canvas(gantt_frame, height=100, width=900, bg='white')
    canvas.pack(side='right', fill='both', expand=True)

    # Metrics Display
    metrics_frame = tk.Frame(root)
    metrics_frame.pack(pady=10)
    avg_wt = tk.StringVar()
    avg_tt = tk.StringVar()
    tk.Label(metrics_frame, textvariable=avg_wt, font=('Arial', 10)).pack(side='left', padx=20)
    tk.Label(metrics_frame, textvariable=avg_tt, font=('Arial', 10)).pack(side='left', padx=20)
    
    # Export UI variables to other modules
    from gui_functions import init_ui_vars
    init_ui_vars(
        root, tree, gantt_output, canvas, 
        label_priority, entry_priority, label_quantum, entry_quantum,
        scheduler_var, btn_start, btn_static, entry_arrival, entry_burst, 
        avg_wt, avg_tt
    )
    
    # Initialize UI AFTER exporting variables
    update_input_fields()
    
    root.mainloop()

if __name__ == "__main__":
    main()