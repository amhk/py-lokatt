#!/bin/bash

T="$(dirname $(dirname $(readlink -f $0)))"
pep8 --repeat "$T"/src/*.py | sed "s+^$T/++"
