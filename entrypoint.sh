#!/bin/sh -l

echo "[start] ai.tm.py..."

/usr/local/bin/python /app/ai-threat-modeling/ai-tm.py $1 --inputs "$2" --output "$3" -ai "$4" -atmi "$5" --model $6 --temperature $7 --verbose $8 --debug $9 -usos "${10}" -t "${11}" --provider "${12}"
