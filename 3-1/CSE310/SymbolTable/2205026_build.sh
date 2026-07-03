#!/usr/bin/env bash
set -euo pipefail

OUT=${1:-a.out}

g++ *.cpp -o $OUT
