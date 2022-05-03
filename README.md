# compare-wheel

Download a wheel from pypi, build a wheel from git repo (inside docker), diff them, print the differences if any.

This is a basic security check for software supply chain risk.

## usage

```
./run.sh \
	requests==2.27.1 \
	requests-2.27.1-py2.py3-none-any.whl \
	v2.27.1
```

The arguments are:
- pip package spec (used for pip download)
- filename of wheel
- git branch representing desired version (but git repo is read from wheel metadata)
