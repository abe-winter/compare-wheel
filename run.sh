#!/usr/bin/env bash
# this builds a wheel from git in docker, copies it to ./built, downloads a wheel from pypi to ./, then compares them

set -euo pipefail

repo=$1 # "https://github.com/JustAnotherArchivist/snscrape"
branch=$2 # "v0.4.3.20220106"
whlname=$3 # "snscrape-0.4.3.20220106-py3-none-any.whl"
package=$4 # "snscrape==0.4.3.20220106"

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
tar xf buildcheck.tar --strip=1 --wildcards '*/layer.tar'
mkdir -p built
cd built
tar xf ../layer.tar
cd ..
rm buildcheck.tar layer.tar

# download
pip download --no-deps $package

# compare
./ziphash.py $whlname --compare built/$whlname
