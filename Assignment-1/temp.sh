set -f
if [ $# -ne 1 ];
then
	echo "Only one argument should be present"
else
	comm='python engine.py "'$1'"'
	eval $comm
fi
set +f
