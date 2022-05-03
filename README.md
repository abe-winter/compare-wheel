# compare-wheel

Download a wheel from pypi, build a wheel from git repo (inside docker), diff them, print the differences if any.

This is a basic security check for software supply chain risk.

## usage

```
./run.sh \
	https://github.com/psf/requests \
	v2.27.1 \
	requests-2.27.1-py2.py3-none-any.whl \
	requests==2.27.1
```

The arguments are:
- git repo
- git branch
- filename of wheel (used for comparison)
- pip package spec (used for downloading)
