#!/bin/sh

script_name=$0
script_full_path=$(dirname "$0")

pip install jupytext

jupytext --to py $script_full_path/*.ipynb 
