#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
IMG_RE = re.compile(r'<img\b[^>]*\bsrc=["\'](/assets/photos/[^"\']+)["\'][^>]*>', re.I)
WIDTH_RE = re.compile(r'\swidth=["\']\d+["\']', re.I)
HEIGHT_RE = re.compile(r'\sheight=["\']\d+["\']', re.I)


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b'\xff\xd8':
        raise ValueError(f'Not a JPEG: {path}')
    i = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while i + 3 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9}:
            continue
        if marker == 0xDA:
            break
        if i + 2 > len(data):
            break
        seg_len = struct.unpack('>H', data[i:i + 2])[0]
        if seg_len < 2 or i + seg_len > len(data):
            raise ValueError(f'Invalid JPEG segment in {path}')
        if marker in sof:
            if seg_len < 7:
                raise ValueError(f'Invalid JPEG SOF in {path}')
            height = struct.unpack('>H', data[i + 3:i + 5])[0]
            width = struct.unpack('>H', data[i + 5:i + 7])[0]
            if width <= 0 or height <= 0:
                raise ValueError(f'Invalid JPEG dimensions in {path}: {width}x{height}')
            return width, height
        i += seg_len
    raise ValueError(f'JPEG dimensions not found: {path}')


def image_size(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    if suffix in {'.jpg', '.jpeg'}:
        return jpeg_size(path)
    if suffix == '.png':
        data = path.read_bytes()
        if len(data) >= 24 and data[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', data[16:24])
    raise ValueError(f'Unsupported local photo format: {path}')


def patch_tag(tag: str, src: str, dims: dict[str, tuple[int, int]]) -> str:
    if src not in dims:
        asset = PUBLIC / src.lstrip('/')
        if not asset.is_file():
            raise FileNotFoundError(f'Missing local photo: {src}')
        dims[src] = image_size(asset)
    width, height = dims[src]
    tag = WIDTH_RE.sub('', tag)
    tag = HEIGHT_RE.sub('', tag)
    close = '/>' if tag.endswith('/>') else '>'
    body = tag[:-len(close)]
    return f'{body} width="{width}" height="{height}"{close}'


def patch_html(path: Path, dims: dict[str, tuple[int, int]]) -> tuple[int, int]:
    text = path.read_text(encoding='utf-8')
    matched = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal matched
        matched += 1
        return patch_tag(match.group(0), match.group(1), dims)

    patched = IMG_RE.sub(repl, text)
    if patched != text:
        path.write_text(patched, encoding='utf-8')
    return matched, int(patched != text)


def validate(dims: dict[str, tuple[int, int]]) -> int:
    checked = 0
    failures: list[str] = []
    for path in sorted(PUBLIC.rglob('*.html')):
        text = path.read_text(encoding='utf-8')
        for match in IMG_RE.finditer(text):
            tag, src = match.group(0), match.group(1)
            asset = PUBLIC / src.lstrip('/')
            if not asset.is_file():
                failures.append(f'{path}: missing asset {src}')
                continue
            actual = dims.setdefault(src, image_size(asset))
            wm = re.search(r'\bwidth=["\'](\d+)["\']', tag, re.I)
            hm = re.search(r'\bheight=["\'](\d+)["\']', tag, re.I)
            if not wm or not hm:
                failures.append(f'{path}: missing intrinsic dimensions for {src}')
                continue
            declared = (int(wm.group(1)), int(hm.group(1)))
            if declared != actual:
                failures.append(f'{path}: {src} declared {declared[0]}x{declared[1]} != actual {actual[0]}x{actual[1]}')
                continue
            checked += 1
    if failures:
        raise SystemExit('Image dimension gate failed:\n' + '\n'.join(failures[:30]))
    return checked


def main() -> None:
    dims: dict[str, tuple[int, int]] = {}
    tags = 0
    changed_files = 0
    for path in sorted(PUBLIC.rglob('*.html')):
        matched, changed = patch_html(path, dims)
        tags += matched
        changed_files += changed
    if tags < 100:
        raise SystemExit(f'Expected at least 100 local photo tags, found {tags}')
    checked = validate(dims)
    print(f'Intrinsic image dimensions OK: {checked} photo tags across {changed_files} changed HTML files; {len(dims)} unique local photos')


if __name__ == '__main__':
    main()
