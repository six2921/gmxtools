#!/bin/bash

# Usage: md.sh <mdp 파일 위치> -t <시간> -o <생성할 mdp 파일 이름>

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <mdp 파일 위치> -t <시간> -o <생성할 mdp 파일 이름>"
    exit 1
fi

MDP_FILE=$1
TIME_IN_NS=$3
OUTPUT_FILE=$5

# Check if the MDP file exists
if [ ! -f "$MDP_FILE" ]; then
    echo "Error: MDP file '$MDP_FILE' not found."
    exit 1
fi

# Calculate steps based on the provided time in ns using awk
STEPS=$(awk -v time_ns="$TIME_IN_NS" 'BEGIN { print int(time_ns * 1000 / 0.002) }')

# Read the mdp file and modify the nsteps, then save it as the specified output file
sed "s/^nsteps.*/nsteps                  = $STEPS    ;  $TIME_IN_NS ns/" "$MDP_FILE" > "$OUTPUT_FILE"

# Output the calculated nsteps
echo "nsteps has been set to: $STEPS for $TIME_IN_NS ns in $OUTPUT_FILE"

# Run GROMACS grompp command
gmx grompp -f "$OUTPUT_FILE" -c npt.gro -t npt.cpt -p topol.top -o "${OUTPUT_FILE%.mdp}.tpr"

