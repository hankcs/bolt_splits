# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2020-07-27 15:28
import argparse
import json
import math
import os
import sys
from collections import defaultdict
import shutil


def split_list(xs: list):
    xs = sorted(set(xs))
    total = len(xs)
    if total == 1:
        return [], [], []
    elif total == 1:
        trn, dev, tst = 1, 0, 0
    elif total == 2:
        trn, dev, tst = 1, 0, 1
    else:
        dev = math.ceil(total * 0.1)
        tst = dev
        trn = total - dev - tst
    trn, dev, tst = xs[:trn], xs[trn:trn + dev], xs[trn + dev:]
    assert not set(trn) & set(dev)
    assert not set(trn) & set(tst)
    assert not set(dev) & set(tst)
    assert len(set(trn) | set(dev) | set(tst)) == total
    return trn, dev, tst


def main():
    parser = argparse.ArgumentParser(
        description='Split Broad Operational Language Translation corpus into train/dev/test set')
    parser.add_argument("--bolt", required=True,
                        help='The root path to BOLT')
    parser.add_argument("--output", required=True,
                        help='The folder where to store the output')
    args = parser.parse_args()
    root = args.bolt
    genres = sorted(os.listdir(root))
    final_splits = defaultdict(set)
    exts = set()
    for genre in genres:
        files = os.listdir(f'{root}/{genre}')
        ext_files = defaultdict(list)
        for f in files:
            fname, ext = f.split('.', maxsplit=1)
            ext_files[ext].append(fname)
            exts.add(ext)

        for ext, group_files in ext_files.items():
            files_per_len = defaultdict(list)
            for name in group_files:
                files_per_len[len(name)].append(name)
            for files in files_per_len.values():
                for n, fs in zip(['trn', 'dev', 'tst'], split_list(files)):
                    final_splits[n] |= set(f'{genre}/{f}.{ext}' for f in fs)
    final_splits = dict((k, sorted(fs)) for k, fs in final_splits.items())
    output = args.output
    if os.path.exists(output):
        print(f'Output {output} already exists, please use a non-exist path.', file=sys.stderr)
        exit(1)

    os.makedirs(output)
    with open(f'{output}/splits.json', 'w') as out:
        json.dump(final_splits, out, indent=4)

    for split, files in final_splits.items():
        for f in files:
            src = f'{root}/{f}'
            dst = f'{output}/{split}/{f}'
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isfile(src):
                shutil.copyfile(src, f'{dst}')


if __name__ == '__main__':
    main()
