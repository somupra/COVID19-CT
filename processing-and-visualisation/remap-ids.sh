ORIGINAL_IDS=$(cat $1 | cut -d , -f 1 | awk '!a[$0]++')

NEW_ID=0

while IFS= read -r ID; do

    cat $1 | grep ^$ID, | sed "s/^$ID,/$NEW_ID,/g" >> "$1_remaped.csv"
    NEW_ID=$((NEW_ID+1))

done <<< "$ORIGINAL_IDS"
