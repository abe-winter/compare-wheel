#!/usr/bin/env bash
# this builds a wheel from git in docker, copies it to ./built, downloads a wheel from pypi to ./, then compares them

set -euo pipefail

package=$1
whlname=$2
branch=$3

# download
pip download --no-deps $package
repo=$(./metakey.py $whlname -k Project-URL -s Source)
echo found repo in wheel metadata: $repo

prefix=$(echo $repo | awk -F/ '{print $NF}')

# build in docker
docker build -t buildcheck \
	--build-arg "prefix=$prefix" \
	--build-arg "repo=$repo" \
	--build-arg "branch=$branch" \
	--build-arg "whlname=$whlname" \
	.

# painfully extract from docker
docker image save buildcheck -o buildcheck.tar
# todo: stream this instead of writing and deleting files
tar xf buildcheck.tar --strip=1 --wildcards '*/layer.tar'
mkdir -p built
cd built
tar xf ../layer.tar
cd ..
rm buildcheck.tar layer.tar

# compare
./ziphash.py $whlname --compare built/$whlname
