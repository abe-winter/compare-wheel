#!/usr/bin/env python3
"extract metadata from a wheel. ugh how is this not built in to pip"

import zipfile, email.parser, argparse, re, logging

def main():
    p = argparse.ArgumentParser()
    p.add_argument('wheel_path')
    p.add_argument('-k', '--key', default='_')
    p.add_argument('-s', '--subkey', help="for distinguishing between multiple Project-URL keys")
    args = p.parse_args()

    zf = zipfile.ZipFile(args.wheel_path)
    # intentional crash if len != 1
    meta_path, = filter(
        re.compile(r'\.dist-info/METADATA$').search,
        zf.namelist(),
    )
    logging.debug('meta_path: %s', meta_path)
    msg = email.parser.BytesParser().parse(zf.open(meta_path))
    # ['Documentation, https://requests.readthedocs.io', 'Source, https://github.com/psf/requests']
    if args.key == '_':
        print('key is _, printing all keys')
        print(list(msg.keys()))
        return
    if args.subkey:
        value, = [
            val for subkey, _, val in
            (raw.partition(', ') for raw in msg.get_all(args.key))
            if subkey == args.subkey
        ]
    else:
        value = msg.get(args.key)
    print(value)

if __name__ == '__main__':
    main()
