#!/bin/bash
mkdir public
cd docs
export PYTHONPATH=..
make html
cd ..
mv docs/_build/html common/static