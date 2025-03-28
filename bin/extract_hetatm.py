import argparse
import os

# argparse 설정
parser = argparse.ArgumentParser(description="Extract and remove selected HETATM residues from PDB.")
parser.add_argument("pdb_file", help="Input PDB file path")
args = parser.parse_args()

# 입력 파일 경로 설정
pdb_file = args.pdb_file

def get_hetatm_residues(pdb_file):
    residues = {}
    with open(pdb_file, 'r') as file:
        for line in file:
            # 무시할 줄 조건 추가
            if line.startswith("TER") or line.startswith("CONECT") or line.startswith("END"):
                continue
            
            # HETATM 처리
            if line.startswith("HETATM"):
                if len(line) < 26:  # line[22:26]에 접근하기 위해 최소 길이 확인
                    print(f"Skipping short line: {line.strip()}")
                    continue
                residue_name = line[17:20].strip()  # 잔기 이름
                chain_id = line[21].strip() if len(line) > 21 else ""  # 체인 ID
                residue_id = line[22:26].strip() if len(line) > 26 else ""  # 잔기 번호
                unique_id = f"{residue_name}{residue_id}_{chain_id}"  # 이름번호_체인ID
                if unique_id not in residues:
                    residues[unique_id] = []
                residues[unique_id].append(line)
    return residues

# 잔기 선택 및 제거 반복 함수
def interactive_residue_extraction(pdb_file, residues):
    extracted_files = []
    while residues:
        residue_names = list(residues.keys())
        
        # 잔기 목록 출력
        print("\n추출할 잔기를 선택하세요 (c: 저장 없이 종료, e: 저장 후 종료):")
        print("c. 저장 없이 종료 (close without saving)")
        print("e. 저장 후 종료 (exit with save)")
        for i, residue_name in enumerate(residue_names, 1):
            print(f"{i}. {residue_name}")
        
        # 사용자 입력 받기
        choice = input("번호를 입력하세요: ").strip()
        
        # 종료 조건 - c: 저장 없이 종료
        if choice.lower() == "c":
            # 생성된 파일 삭제
            for file_name in extracted_files:
                os.remove(file_name)
            print("저장된 파일이 모두 삭제되었습니다. 프로그램을 종료합니다.")
            return
        
        # 종료 조건 - e: 저장 후 종료
        if choice.lower() == "e":
            break
        
        # 유효한 숫자 선택인지 확인
        try:
            choice = int(choice)
            if choice < 1 or choice > len(residue_names):
                raise ValueError
        except ValueError:
            print("잘못된 선택입니다. 다시 시도하세요.")
            continue
        
        # 선택한 잔기 처리
        selected_residue = residue_names[choice - 1]
        
        # 선택한 잔기만 별도로 저장
        split_residue_file = f"{selected_residue}.pdb"
        with open(split_residue_file, 'w') as out_file:
            out_file.writelines(residues[selected_residue])
        extracted_files.append(split_residue_file)
        print(f"{split_residue_file} 파일이 생성되었습니다.")
        
        # 선택된 잔기를 residues에서 제거
        del residues[selected_residue]
    
    # e를 선택한 경우, 최종 수정된 파일 저장
    split_file_name = pdb_file.replace(".pdb", "_split.pdb")
    with open(pdb_file, 'r') as file, open(split_file_name, 'w') as modified_file:
        for line in file:
            if len(line) < 26:  # 최소 길이 확인
                modified_file.write(line)
                continue
            residue_name = line[17:20].strip()
            chain_id = line[21].strip() if len(line) > 21 else ""
            residue_id = line[22:26].strip() if len(line) > 26 else ""
            unique_id = f"{residue_name}{residue_id}_{chain_id}"
            if line.startswith("HETATM") and unique_id not in residues:
                continue
            modified_file.write(line)
    print(f"{split_file_name} 파일이 저장되었습니다. 프로그램을 종료합니다.")

# 실행
residues = get_hetatm_residues(pdb_file)
interactive_residue_extraction(pdb_file, residues)
