#!/bin/bash
R=36
RATIO=2
for ((y = -R; y <= R; y += RATIO)); do
    x=$(dc -e "$R 2^${y/-/_} 2^-vp")
    printf '%*s%*s%*s\n' $((R - x)) x $x '' $x x
done
