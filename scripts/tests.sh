#!/bin/bash

script="$(readlink -f $0)"
root="$(dirname "$script")/.."

PYTHONPATH="$root/src" python -m unittest discover \
	--top-level-directory "$root" \
	--start-directory "$root/tests"
