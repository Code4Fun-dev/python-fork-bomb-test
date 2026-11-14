# Cross-Platform Python Process Exhaustion Demo (Fork Bomb)

> **Disclaimer:** This repository is an educational hobby project created to explore operating system process management and resource limits. Do not run this code on production systems or machines where you do not have explicit permission to test system stability.

## Overview
A fork bomb is a classic denial-of-service (DoS) mechanism that demonstrates what happens when a program replicates itself exponentially. This project uses a cross-platform Python script to observe how different operating systems (POSIX vs. Windows) handle rapid process creation, memory allocation, and Process ID (PID) exhaustion.

## Transparency Note
The raw Python script in this repository was generated with the assistance of an AI tool as part of a personal learning experiment. My goal with this repo was not to write complex custom software from scratch, but to safely observe cross-platform operating system behavior, test process limits, and document how system administrators defend against resource exhaustion.

## How the Code Works
The script detects the host operating system via `os.name` and runs a platform-specific replication loop:

* **POSIX Systems (Linux / macOS):**
  * Uses `os.fork()` inside an infinite `while True` loop to clone the current process.
  * When `pid == 0` (identifying the newly created child process), it recursively calls `posix()`, causing exponential process growth.
* **Windows Systems (`os.name == "nt"`):**
  * Because Windows lacks a native `fork()` system call, the script uses `subprocess.Popen()` to repeatedly launch new instances of the Python interpreter (`sys.executable`) running the same script (`os.path.abspath(__file__)`).
  * Applies the `subprocess.CREATE_NO_WINDOW` flag so background processes spawn silently without flooding the desktop with console windows.
* **Resilient Error Handling:**
  * Both loops wrap process creation in a `try...except OSError` block. When the OS temporarily refuses to spawn new processes due to resource limits, the script pauses briefly (`time.sleep(0.1)`) and immediately tries again rather than crashing.

## Mitigation & Prevention
Exploring how to stop process exhaustion is just as important as understanding how it starts.

### On Linux / Unix-like Systems
Administrators prevent fork bombs by setting user-level process quotas:
* **Check current process limits:**
  ```bash
  ulimit -u
  ```
* **Temporarily restrict maximum user processes (e.g., to 100):**
  ```bash
  ulimit -S -u 100
  ```
* **Permanent configuration:** Limits can be enforced permanently via `/etc/security/limits.conf` or by using Linux Control Groups (`cgroups`) and `systemd` resource controls (`TasksMax`).

### On Windows Systems
Because Windows creates full processes rather than lightweight forks, memory and handle exhaustion typically occur before hitting a hard PID ceiling:
* Administrators use **Windows Job Objects** to cap the number of active processes and memory usage per application or user session.

## Safe Testing Environment
If you want to experiment with this code safely:
1. Run it inside an isolated **Virtual Machine (VM)** or a **Docker container** with strict PID and memory flags (e.g., `docker run --pids-limit 50 --memory 256m ...`).
2. Save all work on your host machine beforehand, as recovering from a live run usually requires a hard reboot or killing the user session.
