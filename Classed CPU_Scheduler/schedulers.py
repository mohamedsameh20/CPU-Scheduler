import time
import tkinter as tk
from threading import Thread
from core import (
    processes, lock, TIME_UNIT, reset_process_states, 
    check_completion, current_quantum, static_mode
)
from visualization import draw_gantt_block, update_gantt_chart
from gui_functions import update_burst_table, on_scheduler_complete

def round_robin_scheduler():
    """Round Robin CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()

    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            if queue:
                process = queue.pop(0)
                execute_time = min(float(core.current_quantum), process['remaining_time'])

                if core.current_time > core.last_gantt_end:
                    draw_gantt_block(-1, core.last_gantt_end, core.current_time - core.last_gantt_end)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = core.current_time

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    # Use tkinter's after method to call on_scheduler_complete
    from gui_functions import root
    root.after(100, on_scheduler_complete)


def FCFS_scheduler():
    """First-Come, First-Served CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()

    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: x['arrival_time'])

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if core.current_time > core.last_gantt_end:
                    gap_duration = core.current_time - core.last_gantt_end
                    draw_gantt_block(-1, core.last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = core.current_time
                update_burst_table()

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    from gui_functions import root
    root.after(100, on_scheduler_complete)


def Preemptive_SJF_scheduler():
    """Shortest Job First (Preemptive) CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()

    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = 1.0  # Preemption interval

                if core.current_time > core.last_gantt_end:
                    gap_duration = core.current_time - core.last_gantt_end
                    draw_gantt_block(-1, core.last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = core.current_time

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    from gui_functions import root
    root.after(100, on_scheduler_complete)


def Non_Preemptive_SJF_scheduler():
    """Shortest Job First (Non-Preemptive) CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()
    
    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if core.current_time > core.last_gantt_end:
                    gap_duration = core.current_time - core.last_gantt_end
                    draw_gantt_block(-1, core.last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = core.current_time
                update_burst_table()

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    from gui_functions import root
    root.after(100, on_scheduler_complete)


def preemptive_priority_scheduler():
    """Priority (Preemptive) CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()

    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['priority'], x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = 1.0  # Preemption interval

                if core.current_time > core.last_gantt_end:
                    gap_duration = core.current_time - core.last_gantt_end
                    draw_gantt_block(-1, core.last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                update_burst_table()

                if process['remaining_time'] > 0:
                    queue.append(process)
                else:
                    process['completed'] = True
                    process['completion_time'] = core.current_time

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    from gui_functions import root
    root.after(100, on_scheduler_complete)


def non_preemptive_priority_scheduler():
    """Priority (Non-Preemptive) CPU scheduling algorithm"""
    import core
    
    queue = []
    core.current_time = 0.0
    core.last_gantt_end = 0.0
    core.gantt_x = 10
    reset_process_states()

    while core.started:
        while core.running:
            with lock:
                arrivals = [p for p in processes if
                            p['arrival_time'] <= core.current_time and not p['in_queue'] and not p['completed']]
                for p in arrivals:
                    queue.append(p)
                    p['in_queue'] = True

            queue.sort(key=lambda x: (x['priority'], x['remaining_time'], x['Process']))

            if queue:
                process = queue.pop(0)
                execute_time = process['remaining_time']

                if core.current_time > core.last_gantt_end:
                    gap_duration = core.current_time - core.last_gantt_end
                    draw_gantt_block(-1, core.last_gantt_end, gap_duration)

                draw_gantt_block(process['Process'], core.current_time, execute_time)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + execute_time:.1f}: P{process['Process']}")

                if not core.static_mode:
                    time.sleep(execute_time * TIME_UNIT)

                core.current_time += execute_time
                process['remaining_time'] -= execute_time
                process['completed'] = True
                process['completion_time'] = core.current_time
                update_burst_table()

                if check_completion():
                    core.running = False
                    core.started = False
            else:
                idle_duration = 1.0
                if not core.static_mode:
                    time.sleep(idle_duration * TIME_UNIT)
                draw_gantt_block(-1, core.current_time, idle_duration)
                update_gantt_chart(f"Time {core.current_time:.1f}-{core.current_time + idle_duration:.1f}: IDLE")
                core.current_time += idle_duration

            if not core.running:
                break

    from gui_functions import root
    root.after(100, on_scheduler_complete)