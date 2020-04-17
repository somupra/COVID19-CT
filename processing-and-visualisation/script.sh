ALL_TIMESTAMPS=$(cat $1 | cut -d , -f 2 | awk '!a[$0]++')
echo "Checkpoint 1"

TIMESTAMPS=$(echo "$ALL_TIMESTAMPS" | head -"$3")
echo "Checkpoint 2"

while IFS= read -r TIMESTAMP; do

    SNAPSHOTS=$(cat $1 | grep "$TIMESTAMP" | head -"$2")
    NUM_SNAPSHOTS=$(wc -l <<< "$SNAPSHOTS")
    
    for ((i=1; i<=$NUM_SNAPSHOTS; i++))
    do
        SHOT1=$(sed -n "$i"p <<< "$SNAPSHOTS")
        X1=$(cut -d , -f 3 <<< "$SHOT1")
        Y1=$(cut -d , -f 4 <<< "$SHOT1")
        
        for ((j=i+1; j<=$NUM_SNAPSHOTS; j++))
        do
            echo "$i $j"
            SHOT2=$(sed -n "$j"p <<< "$SNAPSHOTS")
            X2=$(cut -d , -f 3 <<< "$SHOT2")
            Y2=$(cut -d , -f 4 <<< "$SHOT2")
            DISTANCE="$(python3 geo.py $X1 $X2 $Y1 $Y2)"

            if [ $DISTANCE != "-1" ]
            then
                ID1=$(cut -d , -f 1 <<< "$SHOT1")
                ID2=$(cut -d , -f 1 <<< "$SHOT2")
                echo "$ID1,$ID2,$TIMESTAMP,$DISTANCE" >> "$1.contact.csv"
                echo "New Entry Added"
            fi
        done
    done
done <<< "$TIMESTAMPS"

echo "Checkpoint 3"

#USERS=$(cat contact.csv | cut -d , -f 1 | awk '!a[$0]++')
#echo "$USERS" | sed 's/$/,no/' > people.csv

sed -i '1s/^/id,infected\n/' people.csv
sed -i '1s/^/id1,id2,time,distance\n/' contact.csv

