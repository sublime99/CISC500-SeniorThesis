#!/bin/bash
for i in $(seq 0 0.05 1); do
   echo -e "\nROUND $i\n"
   python3 comp_graphs.py $i
done
