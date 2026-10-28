#!/usr/bin/env python3
"""Restore and verify explicit source pixels on an exactly aligned image."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops


def read_rgb(path):
    with Image.open(path) as im:
        im.load()
        return im.convert('RGB')


def mask_binary(path, size):
    with Image.open(path) as im:
        im.load()
        if im.size != size:
            raise ValueError('Mask dimensions do not match source')
        m = im.convert('L')
    values = set(m.getdata())
    if not values.issubset({0, 255}):
        raise ValueError('Mask must contain only 0 and 255')
    if 255 not in values:
        raise ValueError('Mask has no protected pixels')
    return m


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='mode', required=True)
    c = sub.add_parser('compose')
    for k in ('source', 'treatment', 'mask', 'output'):
        c.add_argument('--'+k, required=True)
    v = sub.add_parser('verify')
    for k in ('source', 'output', 'mask'):
        v.add_argument('--'+k, required=True)
    a = p.parse_args()
    source = read_rgb(a.source)
    mask = mask_binary(a.mask, source.size)
    out = Path(a.output)
    if a.mode == 'compose':
        target = out.resolve()
        inputs = [Path(a.source).resolve(), Path(a.treatment).resolve(), Path(a.mask).resolve()]
        if target in inputs or out.exists():
            raise ValueError('Output exists or would overwrite an input')
        if out.suffix.lower() != '.png':
            raise ValueError('Output must be a lossless PNG')
        treatment = read_rgb(a.treatment)
        if treatment.size != source.size:
            raise ValueError('Treatment dimensions do not match source; registration required')
        result = Image.composite(source, treatment, mask)
        with out.open('xb') as f:
            result.save(f, format='PNG')
    result = read_rgb(out)
    if result.size != source.size:
        raise ValueError('Output dimensions do not match source')
    diff = ImageChops.difference(source, result)
    zero = Image.new('RGB', source.size, (0, 0, 0))
    protected_diff = Image.composite(diff, zero, mask)
    ok = protected_diff.getbbox() is None
    print(json.dumps({'protected_rgb_pixels_equal': ok, 'source_sha256': digest(a.source),
                      'mask_sha256': digest(a.mask), 'output_sha256': digest(out),
                      'size': list(source.size), 'scope': 'mask pixels only; mask completeness and registration require review'}))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
