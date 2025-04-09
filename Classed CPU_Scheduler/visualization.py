import tkinter as tk

# These will be initialized by gui_functions.py
canvas = None
gantt_output = None

def init_visualization(canvas_ref, gantt_output_ref):
    """Initialize the visualization components"""
    global canvas, gantt_output
    canvas = canvas_ref
    gantt_output = gantt_output_ref

def draw_gantt_block(process, start, duration):
    """Draw a block in the Gantt chart representing process execution"""
    from core import gantt_x, last_gantt_end
    
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
    
    # Update the global last_gantt_end
    import core
    core.last_gantt_end = start + duration
    core.gantt_x = gantt_x

def update_gantt_chart(text):
    """Add text to the Gantt chart output area"""
    gantt_output.insert(tk.END, text + '\n')
    gantt_output.see(tk.END)