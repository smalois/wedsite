#!/bin/bash

NAMETAG_WIDTH=3919
NAMETAG_HEIGHT=1650

while read p; do
	FIRST_NAME=`echo $p | awk -F ',' '{print $1}'`
	LAST_NAME=`echo $p | awk -F ',' '{print $2}'`
	GUEST_HASH=`echo $p | awk -F ',' '{print $3}'`
	TABLE_NUM=`echo $p | awk -F ',' '{print $4}'`

	LAST_NAME_CLEAN=${LAST_NAME//[^a-zA-Z0-9_]/}
	FIRST_NAME=${FIRST_NAME//[^a-zA-Z0-9_]/}
	LAST_NAME_ENCODED="${LAST_NAME// /%20}"

    qrencode -l H -m 0 -s 16 -d 300 \
		-o ./guestqrs/$FIRST_NAME$LAST_NAME_CLEAN.png \
		https://abbyandscott.fun/guest/$FIRST_NAME$LAST_NAME_ENCODED/$GUEST_HASH

    convert nametag_blank_300dpi.png \
    	-font Tinos \
    	-fill black \
    	-undercolor 'rgba(250,250,250,0.0)' \
    	-pointsize 156  \
    	-gravity NorthWest \
    	-draw "text 765,500 \"\"" \
    	-draw "scale 0.68,0.68 text 1608,1455 '$TABLE_NUM'" \
    	-draw "image srcOver 2830,520 745,745 './guestqrs/$FIRST_NAME$LAST_NAME_CLEAN.png'" \
    	./render/$FIRST_NAME$LAST_NAME_CLEAN.png
	
	echo "Finished with $FIRST_NAME $LAST_NAME..."
done < extra_guests.txt

