#! /bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <pid>"
    exit 1
fi

PID=$1
OUT=trace_${PID}.txt

if ! ps -p $PID > /dev/null; then
    echo "Process with PID $PID not found"
    exit 1
fi

echo "Tracing process $PID to $OUT"
(perf trace -s -p $PID -o $OUT) 2>&1 & pid=$!
(sleep 10 && kill $pid) 
echo waiting for trace to finish
wait $pid

SCRIPT='
BEGIN {
    printf "    syscall    calls    mean   total\n"
}
/\%$/ {if (NF == 7) {
                 calls[$1] += $2
                 total[$1] += $3
}}

END {
    printf "    syscall    calls    mean   total\n"
    for (syscall in calls) {
        printf "%12s %6d 9.4f %12.3f\n", syscall, calls[syscall], calls[syscall]/total[syscall], total[syscall]
    }
}

'

awk "$SCRIPT" $OUT
rm $OUT

