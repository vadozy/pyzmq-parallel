import subprocess
import atexit
import os

processes = []


def main():
    atexit.register(cleanup)
    cpu_count = os.cpu_count()
    for i in range(cpu_count):
        p = subprocess.Popen(['python', '-m', 'zpen.finv.worker'])
        processes.append(p)
    p = subprocess.Popen(['python', '-m', 'zpen.finv.collector'])
    processes.append(p)
    print("Sub-Processes started!")
    print(f"{cpu_count} workers and 1 collector")
    print("Open another terminal and run command [ $ python -m zpen.finv.tester ]")

    code = None
    while code != "q":
        code = input("Enter 'q' to terminate\n")


def cleanup():
    print("Cleaning Up ...")
    for p in processes:
        p.kill()


if __name__ == "__main__":
    main()
