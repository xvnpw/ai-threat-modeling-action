new_version=$1
echo "setting version to ${new_version}..."
sed -Ei "s|xvnpw/ai-threat-modeling-action@v[0-9]+\.[0-9]+\.[0-9]+|xvnpw/ai-threat-modeling-action@v${new_version}|g" ai-threat-modeling-action/README.md