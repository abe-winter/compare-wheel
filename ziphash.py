#!/usr/bin/env python3
"ziphash -- hash each thing in a zip file"

import zipfile, hashlib, argparse, pprint, difflib

def digest_dict(path):
    zf = zipfile.ZipFile(path)
    return {
        info.filename: hashlib.md5(zf.open(info.filename).read()).hexdigest()
        for info in zf.infolist()
    }

def compare(hashes1, hashes2):
    if (s1 := set(hashes1)) != (s2 := set(hashes2)):
        print("BAD! file lists aren't the same")
        print('missing', s1 - s2, 'extra', s2 - s1)
    not_equal = []
    for key in sorted(s1 & s2):
        match = hashes1[key] == hashes2[key]
        mark = (' *diff*', '  ok   ')[match]
        print(mark, key)
        if not match:
            not_equal.append(key)
    return not_equal

def diff_not_equal(unequal_keys, path1, path2):
    zips = [zipfile.ZipFile(path1), zipfile.ZipFile(path2)]
    for key in unequal_keys:
        left = list(zips[0].open(key))
        right = list(zips[1].open(key))
        print('UNEQUAL FILE', key)
        for diff in difflib.diff_bytes(difflib.unified_diff, left, right):
            print(diff)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('path')
    p.add_argument('-c', '--compare', help="a second path to compare to")
    args = p.parse_args()

    f1 = digest_dict(args.path)
    if args.compare:
        not_equal = compare(f1, digest_dict(args.compare))
        if not_equal:
            diff_not_equal(not_equal, args.path, args.compare)
    else:
        pprint.pprint(f1)

if __name__ == '__main__': main()
