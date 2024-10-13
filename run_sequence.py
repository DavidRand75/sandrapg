import subprocess

# List of Python scripts to run
scripts = ["router_for_download_workers.py", "router_for_algorithm_workers.py", "run_down_wrkrs.py", "run_algo_wrkrs.py"]

def run_scripts_in_separate_windows(scripts):
    for script in scripts:
        try:
            # Run each script in a new command prompt window
            subprocess.Popen(
                ["python", script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print(f"Started {script} in a new command prompt.")
        except Exception as e:
            print(f"Failed to start {script}: {e}")

if __name__ == "__main__":
    run_scripts_in_separate_windows(scripts)
