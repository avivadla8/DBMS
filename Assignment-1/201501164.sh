#!/bin/bash
echo Initializing minisql engine
# bash trap is taken care of i.e. bash trap executed when CTRL-C is pressed

trap bashtrap INT

while [ 1 ];
do

	bashtrap()
	{
		echo -n ""
	}

	echo -n "minisql>> "
	read comm

	if [[ $comm == "" ]]
	then
		continue
	fi

	if [[ $comm == "exit" ]]
	then
		echo Bye
		break
	fi

	if [[ $comm == "clear" ]]
	then
		command $comm
		continue
	fi

	declare -a ARRAY
	count=0

	for word in $comm;
	do
		ARRAY[$count]=$word
		((count++))
	done
	if [[ $count -eq 3 ]]
	then
		if [[ ${ARRAY[0]} == 'python' &&  ${ARRAY[1]} == 'engine.py' ]]
		then
			command $comm
		else
			echo 'Error :- Command should be of form :- python engine.py "command"'
		fi

	else
		echo 'Error :- Command should be of form :- python engine.py "command"'
	fi
done
