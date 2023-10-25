#!/bin/sh -l

echo "[start] ai.tm.py..."

ARGS="$1 --inputs $2 --output $3 -ai $4 -atmi $5 --model $6 --temperature $7 -usos ${10} -t ${11} --provider ${12}"

if $8 = 'true'; then
    ARGS="$ARGS --verbose"
fi

if $9 = 'true'; then
    ARGS="$ARGS --debug"
fi

echo $ARGS

/usr/local/bin/python /app/ai-threat-modeling/ai-tm.py $ARGS
