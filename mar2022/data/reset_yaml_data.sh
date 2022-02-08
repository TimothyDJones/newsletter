#1/usr/bin/env sh
cat > ./blank.yaml << EOF
---
- type:
  title:
  url:
  content: |

EOF

declare -a file_list=(
    "career"
    "development"
    "fbom"
    "fun"
    "plom"
    "quotes"
    "telecom"
    "testing"
    "tips"
    "tutorials"
    "utilities"
)

for f in "${file_list[@]}"
do
    cp blank.yaml $f.yaml
done

rm -rf blank.yaml

chmod -x $0
