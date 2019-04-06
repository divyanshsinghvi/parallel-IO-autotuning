#!/bin/bash

for i in `seq 1 11`
do
	python3 model/randomParameters.py 
	python3 read_config.py
done
