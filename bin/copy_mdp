import os
import sys
import argparse

# argparse를 사용해 사용자로부터 입력 인자 받기
parser = argparse.ArgumentParser(
    description="Configure a GROMACS .mdp file with specified simulation time"
)
parser.add_argument("mdp_file", type=str, help="Path of the template .mdp file")
parser.add_argument("-t", "--time", type=float, required=True, help="Simulation time in ns")
parser.add_argument("-o", "--output", type=str, required=True, help="Output .mdp file name")

args = parser.parse_args()

# 입력 인자들 할당
mdp_file = args.mdp_file        # 템플릿 .mdp 파일 경로
time_in_ns = args.time          # 시뮬레이션 시간(ns)
output_file = args.output       # 생성할 .mdp 파일 이름

# 입력된 .mdp 파일이 존재하는지 확인
if not os.path.isfile(mdp_file):
    print(f"Error: MDP file '{mdp_file}' not found.")
    sys.exit(1)

# nsteps 계산
# 주어진 시간(ns)을 기준으로 nsteps 값 계산, dt=0.002 ps를 가정하고 있음
dt = 0.002  # Time step in picoseconds (ps)
steps = int(time_in_ns * 1000 / dt)  # 총 steps 수 계산 (1000으로 나눠 ps를 ns로 변환)

# .mdp 파일 수정: nsteps 값을 계산된 steps 값으로 설정
with open(mdp_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # nsteps 라인을 수정하여 계산된 steps 값으로 대체
        if line.startswith("nsteps"):
            outfile.write(f"nsteps                  = {steps}    ;  {time_in_ns} ns\n")
        else:
            outfile.write(line)

# 결과 출력
print(f"nsteps has been set to: {steps} for {time_in_ns} ns in {output_file}")

