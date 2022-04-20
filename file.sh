path1=main.py #the path of the pyhton script in case of depugging

output=output.mp4 #the path of the output files

inputfile=D:/imageProcessing/challenge_video.mp4 #the path of the input video



while getopts d:i: flag
do
    case "${flag}" in
        d) depug=${OPTARG};;
		i) inp=${OPTARG};;
    esac
done


python $path1 $inp $output $depug;




