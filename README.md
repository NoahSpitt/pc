# PC Simulator

This project contains a minimal PC configuration simulator and a simple shell.

The builder stores detailed hardware parameters such as cache sizes and
clock speeds. Network options include latency and bandwidth. Configurations are
saved under `configs/` as JSON.

```
python main.py
```

From the menu you can create configurations, list them, and launch a shell.

Configurations are stored under the `configs/` directory as JSON files.
Configuration names must be simple filenames without slashes or `..`.

Run basic checks with:

```
python -m py_compile builder.py shell_sim.py main.py pc_sim.py
```

The shell supports these commands:

- `ls [path]`
- `cd <path>`
- `cat <file>`
- `echo <text> > <file>`
- `mkdir <dir>` create a directory
- `touch <file>` create an empty file
- `rm <path>` remove file or directory
- `mv <src> <dst>` move files or directories
- `cp <src> <dst>` copy files
- `run <ram_gb> <cycles>` simulate a program consuming RAM and CPU cycles
- `download <size_mb>` simulate a download using the configured network speed
- `free` display RAM usage
- `cpuinfo` show CPU information
- `exit`

This is a lightweight demo inspired by the project description.

