#!/bin/sh

echo "starting!"

for item in "reflectivity" "velocity" "differential_reflectivity" "differential_phase" "spectrum_width" "cross_correlation_ratio"
do
    echo "executing $item"
    if [ -f "pdfs/$item.pdf" ]; then
        echo "$item.pdf exists"
    else
        sh app.sh $item
    fi
done

echo "done!"