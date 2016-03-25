#!/bin/bash


if [[ $# -eq 0 ]] ; then
    echo 'You have to supply an argument'
    exit 1
fi
if [[ "$1" = "--render" && $# -eq 1 ]] ; then
    echo 'You have to supply an additional argument'
    exit 1
fi
if [ "$1" = "--rebuild" ]
then      
	python save_al.py "$2"

elif [ "$1" = "--render" ]  
then    
	python retreive.py "$2"
else
	echo 'No option available'
fi
