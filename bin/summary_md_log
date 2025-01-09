import os
import argparse
from datetime import datetime, timedelta

# argparse를 사용해 사용자로부터 로그 파일 입력받기
parser = argparse.ArgumentParser(
    description="This script reads a GROMACS md.log file and prints time information\n",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("log_file", type=str, help="md.log (GROMACS)")
args = parser.parse_args()
log_file = args.log_file

# Initialize variables
dt = None
nsteps = None
started_time = None
first_step = None
first_time = None
last_step = None
last_time = None

# Step 1: Read from the start to extract dt, nsteps, started_time, and first_step, first_time
with open(log_file, 'r') as file:
    for line in file:
        # Extract dt and nsteps
        if line.strip().startswith("dt"):
            dt = float(line.split('=')[1].strip())
        elif line.strip().startswith("nsteps"):
            nsteps = int(line.split('=')[1].strip())
        
        # Extract started_time
        elif "Started mdrun on" in line:
            date_string = " ".join(line.split()[-5:])
            started_time = datetime.strptime(date_string, "%a %b %d %H:%M:%S %Y")
        
        # Extract first Step and Time
        elif "Step" in line and "Time" in line:
            step_line = next(file).strip()
            first_step, first_time = map(float, step_line.split())
            break  # Stop reading after finding the first Step and Time

# Step 2: Read from the end to extract last_step and last_time
with open(log_file, 'rb') as file:
    file.seek(0, os.SEEK_END)
    position = file.tell()
    buffer = []

    while position >= 0:
        file.seek(position)
        position -= 1
        char = file.read(1)

        if char == b'\n':
            line = b''.join(reversed(buffer)).decode('utf-8')
            buffer = []

            # Ensure the line contains only numbers to avoid headers
            if line.strip() and line.split()[0].isdigit():
                try:
                    last_step, last_time = map(float, line.split())
                    break
                except ValueError:
                    continue  # Ignore lines that do not parse correctly
        else:
            buffer.append(char)

# Calculate the outputs only if all required values were found
if dt is not None and nsteps is not None and started_time is not None and first_step is not None and first_time is not None:
    # Calculate ns metrics
    total_ns = (dt * nsteps) / 1000  # Total ns expected
    current_ns = last_step * dt / 1000  # Corrected current ns calculation

    # Daily ns calculation
    elapsed_time_days = (datetime.now() - started_time).total_seconds() / 86400  # in days
    daily_ns = current_ns / elapsed_time_days if elapsed_time_days > 0 else 0

    # Estimate remaining time and end date based on current daily ns speed
    remaining_ns = total_ns - current_ns
    estimated_days_to_complete = remaining_ns / daily_ns if daily_ns > 0 else float('inf')
    estimated_end_time = datetime.now() + timedelta(days=estimated_days_to_complete)

    # Calculate the duration in days, hours, and minutes
    estimated_duration_seconds = estimated_days_to_complete * 86400  # Convert days to seconds
    duration_days = int(estimated_duration_seconds // 86400)
    duration_hours = int((estimated_duration_seconds % 86400) // 3600)
    duration_minutes = int((estimated_duration_seconds % 3600) // 60)

    # Display the required information
    print(f"{'Start:'.ljust(10)} {started_time.strftime('%m.%d %H:%M')}")
    print(f"{'End:'.ljust(10)} {estimated_end_time.strftime('%m.%d %H:%M')}")
    print(f"{'Duration:'.ljust(10)} {duration_days} days {duration_hours} hours {duration_minutes} minutes")
    print(f"{'ns/day:'.ljust(10)} {daily_ns:.0f}")
    print(f"{'Elapse:'.ljust(10)} {current_ns:.0f}/{total_ns:.0f}")

else:
    print("Error: Required data not found in the log file.")

