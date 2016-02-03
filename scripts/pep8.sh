#!/bin/bash

T="$(dirname $(dirname $(readlink -f $0)))"
pep8 --ignore=E501 --repeat "$T"/src/*.py "$T"/tests/*.py | sed "s+^$T/++"
