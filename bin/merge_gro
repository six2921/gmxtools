import argparse
import pandas as pd

# argparse 설정
parser = argparse.ArgumentParser(
    description="Combine multiple .gro files (e.g., protein and ligand files) into a single .gro file, with atom and residue numbers updated sequentially."
)
parser.add_argument("gro_files", nargs='+', help="List of .gro files to combine (e.g., protein.gro lig1.gro lig2.gro ...)")
parser.add_argument("-o", "--output", default="combined.gro", help="Output .gro file name (default: combined.gro)")

# 인자 파싱
args = parser.parse_args()

# .gro 파일을 테이블로 변환하는 함수
def gro_to_dataframe(file_path):
    """Convert a .gro file into a pandas DataFrame.

    Args:
        file_path (str): Path to the .gro file.

    Returns:
        pd.DataFrame: DataFrame containing atom information from the .gro file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 테이블 부분 추출 (첫 번째 두 줄과 마지막 줄 제외)
    table_lines = lines[2:-1]
    
    # 각 라인의 정보를 나누어 DataFrame으로 변환
    data = []
    for line in table_lines:
        residue_number = int(line[:5].strip())
        residue_name = line[5:10].strip()
        atom_name = line[10:15].strip()
        atom_number = int(line[15:20].strip())
        x = float(line[20:28].strip())
        y = float(line[28:36].strip())
        z = float(line[36:44].strip())
        data.append([residue_number, residue_name, atom_name, atom_number, x, y, z])
    
    # DataFrame 생성
    columns = ['residue_number', 'residue_name', 'atom_name', 'atom_number', 'x', 'y', 'z']
    df = pd.DataFrame(data, columns=columns)
    
    return df

# .gro 파일 형식에 맞게 테이블을 포맷팅하는 함수
def format_gro_line(row):
    """Format a row of DataFrame to .gro file line format.

    Args:
        row (pd.Series): DataFrame row with atom information.

    Returns:
        str: Formatted .gro line as a string.
    """
    return f"{int(row['residue_number']):>5}{row['residue_name']:<5}{row['atom_name']:>5}{int(row['atom_number']):>5}{row['x']:8.3f}{row['y']:8.3f}{row['z']:8.3f}\n"

# 여러 개의 .gro 파일을 결합하고 .gro 파일로 저장하는 함수
def process_files(gro_files, output_file):
    """Combine multiple .gro files into a single .gro file with sequentially updated residue and atom numbers.

    Args:
        gro_files (list of str): List of .gro file paths to combine.
        output_file (str): Path for the output combined .gro file.
    """
    combined_df = pd.DataFrame()
    atom_offset = 0
    
    # 각 파일을 순서대로 DataFrame으로 변환하고 결합
    for i, gro_file in enumerate(gro_files):
        df = gro_to_dataframe(gro_file)
        
        # 첫 번째 파일을 제외하고 residue_number를 901부터 순차적으로 부여
        if i > 0:
            df['residue_number'] = 900 + i
        
        # atom_number 업데이트
        df['atom_number'] = range(atom_offset + 1, atom_offset + len(df) + 1)
        atom_offset += len(df)
        
        # DataFrame 결합
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    # .gro 파일의 첫 두 줄 생성
    row_count = len(combined_df)
    gro_content = ["protein-ligand complex\n", f" {row_count}\n"]
    
    # 테이블의 각 행을 .gro 파일 형식으로 변환하여 추가
    for _, row in combined_df.iterrows():
        gro_content.append(format_gro_line(row))
    
    # .gro 파일로 저장
    with open(output_file, 'w') as gro_file:
        gro_file.writelines(gro_content)

    print(f"Updated .gro file saved to: {output_file}")

# 파일 처리
process_files(args.gro_files, args.output)

