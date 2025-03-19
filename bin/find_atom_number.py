import os
import sys

# PDB 파일 로드 함수
def load_pdb(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.startswith('ATOM')]

# PDB 파싱 함수
def parse_pdb(lines):
    parsed = []
    for line in lines:
        atom_number = int(line[6:11].strip())
        atom_name = line[12:16].strip()
        residue_name = line[17:20].strip()
        residue_number = int(line[22:26].strip())
        parsed.append((atom_number, atom_name, residue_name, residue_number, line))
    return parsed

# 데이터 출력 함수
def print_selected(selected):
    for _, _, _, _, line in selected:
        print(line)

# 저장 함수
def save_pdb(selected, filename):
    if not filename.endswith('.pdb'):
        print("Error: Filename must end with .pdb")
        return
    with open(filename, 'w') as file:
        for _, _, _, _, line in selected:
            file.write(line + '\n')
    print(f"Saved to {filename}")

# 명령어 설명 출력 함수 (상세 버전)
def print_help():
    print("\nAvailable commands:")
    print("  all            - Reload all data from PDB file")
    print("  range 1 10     - Select residues 1~10")
    print("  pick 1 10 20   - Select residues 1, 10, 20")
    print("  type CA CB     - Select specific atom types")
    print("  save test.pdb  - Save selected information")
    print("  list           - List atom numbers")
    print("  exit           - Exit the script\n")
    print("  help           - Print help text\n")

if len(sys.argv) != 2:
    print("Usage: python find_atom_number.py <PDB_FILE>")
    sys.exit(1)

# 파일 이름 가져오기
filename = sys.argv[1]
if not os.path.exists(filename):
    print(f"Error: {filename} not found!")
    sys.exit(1)

all_data = parse_pdb(load_pdb(filename))
selected = all_data[:]

# 초기 설명 출력
print_help()

# 명령어 실행 루프
while True:
    print_help()
    command = input("Command: ").strip().split()

    if not command:
        continue

    cmd = command[0].lower()

    if cmd == "all":
        selected = all_data[:]
        print_selected(selected)

    elif cmd == "range":
        if len(command) != 3:
            print("Usage: range start end")
            continue
        try:
            start, end = int(command[1]), int(command[2])
            selected = [x for x in all_data if start <= x[3] <= end]
            if not selected:
                print("Error: No residues in the specified range.")
            else:
                print_selected(selected)
        except ValueError:
            print("Invalid input. Please enter integers.")

    elif cmd == "pick":
        if len(command) < 2:
            print("Usage: pick res1 res2 ...")
            continue
        try:
            picks = set(map(int, command[1:]))
            selected = [x for x in all_data if x[3] in picks]
            missing = picks - set(x[3] for x in selected)
            if missing:
                print(f"Warning: Missing residues: {', '.join(map(str, missing))}")
            print_selected(selected)
        except ValueError:
            print("Invalid input. Please enter integers.")

    elif cmd == "type":
        if len(command) < 2:
            print("Usage: type ATOM1 ATOM2 ...")
            continue
        atom_types = set(command[1:])
        selected = [x for x in selected if x[1] in atom_types]
        if not selected:
            print("Error: No matching atom types found.")
        else:
            print_selected(selected)

    elif cmd == "save":
        if len(command) != 2:
            print("Usage: save filename.pdb")
            continue
        save_pdb(selected, command[1])

    elif cmd == "list":
        atom_numbers = [str(x[0]) for x in selected]
        print(",".join(atom_numbers))

    elif cmd == "help":
        print_help()

    elif cmd == "exit":
        print("Exiting...")
        break

    else:
        print(f"Unknown command: {cmd}")
