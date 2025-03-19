import os
import subprocess
import sys
import argparse

def process_files(file_list):
    for file in file_list:
        if os.path.isfile(file):
            print(f"Processing {file} with acpype...")
            try:
                # acpype 명령 실행
                result = subprocess.run(['acpype', '-i', file], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"Error processing {file}: {result.stderr.strip()}")
                else:
                    print(f"{file} processed successfully.")
            except Exception as e:
                print(f"Exception occurred while processing {file}: {e}")
        else:
            print(f"File not found: {file}")

def main():
    parser = argparse.ArgumentParser(
        description="Process molecular files (e.g., .mol2, .pdb) with acpype.",
        epilog="Example usage: python acpype_loop.py file1.mol2 file2.pdb file3.mol"
    )
    parser.add_argument(
        "files", nargs="+", help="List of molecular files (e.g., .mol2, .pdb) to process using acpype."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output to show acpype command execution details."
    )
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled.")

    # 파일 처리
    process_files(args.files)

    print("All files processed.")

if __name__ == "__main__":
    main()

