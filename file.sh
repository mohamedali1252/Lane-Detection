path1=D:/imageProcessing/main.py #the path of the pyhton script in case of depugging
path2=D:/imageProcessing/ndepug.py #the path of the pyhton script in case of not depugging 
output=D:/imageProcessing/tmp.mp4 #the path of the output files
inputfile=D:/imageProcessing/challenge_video.mp4 #the path of the input video



while getopts d: flag
do
    case "${flag}" in
        d) depug=${OPTARG};;
    esac
done


#
case "$depug" in
    #case 1
    1) python $path1 $inputfile $output;;
      
    #case 0
    0) python $path2 $inputfile $output;;
      
	#default
	*) echo "Please ";;
esac


