from threading import Lock

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
    """Check if all processes have completed execution"""
    return all(p['completed'] for p in processes)

def reset_process_states():
    """Reset process execution states but keep the process list"""
    with lock:
        for p in processes:
            p['remaining_time'] = p['burst_time']
            p['completed'] = False
            p['in_queue'] = False


