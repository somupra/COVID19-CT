#!/bin/bash
ORIGINAL_IDS=$(cut -d , -f 1 $1 | awk '!a[$0]++')

NEW_ID=0

while IFS= read -r ID; do
    sed -i "s/^$ID,/$NEW_ID,/g" $1
    NEW_ID=$((NEW_ID+1))
done <<< "$ORIGINAL_IDS"
