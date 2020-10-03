#!/usr/bin/env bash
PYTHONPATH='./':$PYTHONPATH python code/capstone.py \
    --graph 'student' \
    --student 242368676 \
    --current-term 3 \
    --num-of-rec-courses 10 \
