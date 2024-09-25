#!/bin/bash
set -e

# 도움말 및 사용법을 출력하는 함수
show_help() {
    echo "예시: ./run_cmds.sh /path/to/commands.txt"
    exit 1
}

# 인자가 충분히 제공되었는지 확인
if [ "$#" -ne 1 ]; then
    echo "오류: CMD_FILE 인자가 필요합니다."
    show_help
fi

# 스크립트 실행 시 인자로 받는 txt 파일 경로
CMD_FILE=$1

# 사용자가 입력한 CMD_FILE 확인
echo "명령어 파일 경로: $CMD_FILE"
echo

# 명령어 파일이 존재하는지 확인 후 실행
if [ -f "$CMD_FILE" ]; then
    echo "명령어 파일을 실행합니다..."
    
    # 파일에 있는 명령어들을 순서대로 실행
    bash "$CMD_FILE"
else
    echo "오류: 명령어 파일을 찾을 수 없습니다."
    exit 1
fi

