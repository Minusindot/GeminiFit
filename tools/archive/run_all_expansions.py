"""Run remaining expansion batches sequentially:
1. Run batch_kotone_expansion.py
2. Run batch_mio_expansion.py
3. Run batch_trio_expansion.py
"""
import sys
import subprocess
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def run_script(script_name):
    print(f"\n=======================================================")
    print(f">> [STARTING] {script_name}")
    print(f"=======================================================")
    res = subprocess.run([sys.executable, script_name])
    if res.returncode != 0:
        print(f">> Warning: {script_name} returned code {res.returncode}")
    else:
        print(f">> [SUCCESS] {script_name} finished!")
    time.sleep(3)

def main():
    run_script("batch_kotone_expansion.py")
    run_script("batch_mio_expansion.py")
    run_script("batch_trio_expansion.py")
    print("\n>> ALL CG BATCHES HAVE BEEN GENERATED!")

if __name__ == "__main__":
    main()
