# 🧠 CPU Scheduler Simulator

A dynamic and educational CPU scheduling simulator built with **Python and Tkinter**, supporting multiple scheduling algorithms including **Round Robin**, **FCFS**, **SJF (Preemptive & Non-Preemptive)**, and **Priority Scheduling (Preemptive & Non-Preemptive)**.

This simulator provides a live and static execution mode, visual Gantt chart output, process table, and essential performance metrics to aid learning and experimentation.

---

## 🚀 Features

✅ Multiple scheduling algorithms:
- Round Robin (Quantum time configurable)  
- First Come First Serve (FCFS)  
- Shortest Job First (Preemptive and Non-Preemptive)  
- Priority Scheduling (Preemptive and Non-Preemptive)

✅ Gantt Chart visualization (Canvas + Text form)  
✅ Live and Static modes  
✅ Average Waiting Time & Turnaround Time metrics  
✅ Dynamic process table updates  
✅ User-friendly input with validation  
✅ Thread-safe design using Python’s `threading.Lock`

---

## 🧮 Algorithms and Metrics

### 🧠 Core Scheduling Metrics

| Metric | Formula |
|--------|---------|
| **Turnaround Time (TAT)** | `Completion Time - Arrival Time` |
| **Waiting Time (WT)** | `Turnaround Time - Burst Time` |
| **Average Waiting Time** | `Σ Waiting Time / Number of Processes` |
| **Average Turnaround Time** | `Σ Turnaround Time / Number of Processes` |

Future improvements could include Response Time and Throughput calculations.

---

## 🛠️ How It Works

- Each algorithm runs in a separate thread to allow live GUI updates.
- The user adds processes with Arrival and Burst times (Priority and Quantum if applicable).
- The scheduler visualizes the execution order and logs times in a Gantt Chart.
- Metrics are calculated once all processes are completed.

---

## 🧑‍💻 Getting Started

### 🔧 Requirements

- Python 3.7+
- Tkinter (usually pre-installed with Python)

### 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cpu-scheduler-simulator.git
   cd cpu-scheduler-simulator



#### Process Table: 
Shows details for each process, including Process ID, arrival time, burst time, remaining time, and completion status.


#### Metrics: 
Displays average waiting time (WT) and average turnaround time (TAT) once the simulation is complete.


#### Static & Live Modes: 
You can choose between live simulation or a static run.

#### Reset Functionality: 
Resets the simulation to start over with new processes.

## 🎮 Usage Guide

1. **Choose a Scheduling Algorithm** from the dropdown menu.

2. **Enter**:
   - **Arrival Time**
   - **Burst Time** for the process

3. **Add Priority** (only if using a priority-based algorithm).

4. **Set Quantum** (only if using Round Robin).

5. Click **Add Process** to insert it into the queue.

6. Press one of the following:
   - **Start Live**: Simulates the scheduling step-by-step in real-time.
   - **Start Static**: Runs the full simulation instantly.

7. **View the Gantt Chart** and performance metrics (Average Waiting Time & Turnaround Time).

8. Click **Full Reset** to clear all data and restart the simulation.

