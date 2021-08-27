#!/bin/bash

NAMETAG_WIDTH=2885
NAMETAG_HEIGHT=3498

while read p; do
	URL=`echo $p | awk -F ',' '{print $1}'`
	NUMBER=`echo $p | awk -F ',' '{print $2}'`

    qrencode -l H -m 0 -s 16 -d 300 \
		-o ./clueqrs/${URL}_qr.png \
		https://abbyandscott.fun/scavenge/$URL

    convert scavenge_template.png \
		-font Tinos \
		-pointsize 128 \
		-draw "text 126,138 'Clue ${NUMBER}'" \
    	-draw "image srcOver 126,183 1156,1156 './clueqrs/${URL}_qr.png'" \
		./render/${URL}.png
	
	echo "Finished with ${URL}"
done < scavenge_urls.txt

