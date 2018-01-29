#!/bin/bash
echo Initializing minisql engine
# bash trap is taken care of i.e. bash trap executed when CTRL-C is pressed

trap bashtrap INT
set -f
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

	if [[ $comm == "exit" || $comm == "exit;" ]]
	then
		echo Bye
		break
	fi

	if [[ $comm == "clear" || $comm == "clear;" ]]
	then
		eval $comm
		continue
	fi

	declare -a ARRAY
	count=0

	temp=""
	for word in $comm;
	do
		ARRAY[$count]=$word
		if [[ $count == 0 ]]
		then
			temp=$word
		else
			temp=''$temp' '$word''
		fi
		((count++))
	done
	# if [[ $count -ge 3 ]]
	# then
	# 	if [[ ${ARRAY[0]} == 'python' &&  ${ARRAY[1]} == 'engine.py' ]]
	# 	then
	# 		eval $comm
	# 	else
	# 		echo 'Error :- Command should be of form :- python engine.py "statement"'
	# 	fi

	# else
	# 	echo 'Error :- Command should be of form :- python engine.py "statement"'
	# fi
	comm='python engine.py "'$temp'"' 
	# echo $comm
	eval $comm

done
set +f
