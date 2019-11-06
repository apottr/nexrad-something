
td[0]="2019 10 2 1 13"
td[1]="2019 5 1 2 42"
td[2]="2018 4 25 5 26"
td[3]="2017 8 2 2 10"
td[4]="2017 2 8 23 38"
td[5]="2016 2 25 23 1"
td[6]="2015 8 19 3 3"

for i in ${!td[*]}; do
    echo $i
    echo ${td[$i]}
    arr[$i]=$(echo ${td[$i]} | base64)
done

echo ${td[*]}
echo ${arr[*]}