#!/bin/zsh
# Render one scene to video, with one retry.
# usage: tools/render1.sh PREFIX OUTDIR NAME [REV]   e.g. tools/render1.sh pk ~/broll-out/64-pinky b9 rev2
# Reads scenes/PREFIX-NAME.svg; writes OUTDIR/PREFIX-NAME-REV.mp4 (titles, NAME t*, come out as .mov with alpha).
cd "${0:A:h}/.."
P=$1; O=$2; n=$3; R=${4:-rev1}; ext=mp4; [[ $n == t* ]] && ext=mov
for try in 1 2; do
  rm -rf $O/rig-$n
  python3 svgpieces.py scenes/$P-$n.svg $O/rig-$n rig >/dev/null 2>&1 && python3 render.py $O/rig-$n $O/$P-$n-$R.$ext >$O/log-$n.txt 2>&1 && { echo "ok $P $n"; exit 0; }
done
echo "FAIL $P $n"
