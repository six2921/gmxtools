import argparse
import subprocess
import time
from datetime import datetime

parser = argparse.ArgumentParser(description="Search for files, display activity status and progress.")
parser.add_argument("path", help="The directory to search in (e.g., ./)", type=str)
parser.add_argument("--log", help="The name of the file to search for (e.g., 'md.log')", type=str, default="md.log")
args = parser.parse_args()

command = f"find {args.path} -name '{args.log}' -exec stat -c '%Y %n' {{}} \;"
result = subprocess.check_output(command, shell=True, text=True)
files = []
for line in result.strip().split('\n'):
    if line.strip():
        mod_time, file_path = line.split(' ', 1)
        files.append((int(mod_time), file_path))

files.sort(key=lambda x: x[0], reverse=True)

for mod_time, file_path in files:
    current_time = int(time.time())
    diff = current_time - mod_time
    status = "active" if diff <= 10 else "inactive"

    total_steps = None
    current_step = None
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if 'nsteps' in line:
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        total_steps = int(part)
                        break
                if total_steps is not None:
                    break

        for i in range(len(lines) - 1, -1, -1):  # 파일 끝에서 시작
            if lines[i].strip().startswith("Step") and "Time" in lines[i]:
                if i + 1 < len(lines):  # 다음 줄이 존재하는지 확인
                    next_line = lines[i + 1].strip()
                    parts = next_line.split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        current_step = int(parts[0])
                break

        if total_steps is not None and current_step is not None:
            progress = (current_step / total_steps) * 100
            dt = 0.000002
            print(f"{status}  |  {current_step*dt:.0f}/{total_steps*dt:.0f} ({progress:.0f}%)  |  {file_path}")
        else:
            print(f"{status}  |  No progress data found  |  {file_path}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
