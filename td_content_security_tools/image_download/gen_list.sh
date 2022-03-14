echo "$0 curdir [exclude_suffix]"
#test $# -ne 1  && exit 0

root=$1

if [ $# -eq 2 ]; then
	exclude_suffix=$2
fi

for subdir in `ls $root`
do	
	if [ -d $subdir -a $# -eq 2 ]; then
		if [[ $subdir == *${exclude_suffix}* ]]; then
			continue
		fi
	fi

	if [ -d $subdir ]; then
		cd $subdir
		curdir=`pwd`
		echo $curdir
		find $curdir -name "*.jpg" -type f  >  $curdir/../${subdir}.lst
		find $curdir -name "*.jpeg" -type f >> $curdir/../${subdir}.lst
		find $curdir -name "*.JPG" -type f  >> $curdir/../${subdir}.lst
		find $curdir -name "*.JPEG" -type f >> $curdir/../${subdir}.lst
		find $curdir -name "*.png" -type f  >> $curdir/../${subdir}.lst
		cd ..
	fi
done
