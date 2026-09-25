#!/usr/bin/env python3
"""
Upload large asset files to Alibaba Cloud OSS.

Usage:
    python scripts/upload_to_oss.py

Required environment variables (or pass as CLI args):
    OSS_ACCESS_KEY_ID       — your AccessKey ID
    OSS_ACCESS_KEY_SECRET   — your AccessKey Secret
    OSS_BUCKET              — bucket name, e.g. poef-assets
    OSS_ENDPOINT            — regional endpoint, e.g. oss-cn-hangzhou.aliyuncs.com

Optional:
    OSS_PREFIX              — key prefix inside the bucket (default: empty)
    --skip-existing         — skip files already in OSS (default: on)
    --force                 — re-upload even if file already exists

Install deps first:
    pip install oss2 tqdm
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import oss2
    from oss2 import SizedFileAdapter, determine_part_size
    from oss2.models import PartInfo
except ImportError:
    sys.exit("Missing dependency: pip install oss2")

try:
    from tqdm import tqdm
except ImportError:
    sys.exit("Missing dependency: pip install tqdm")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
ASSET_DIRS = [
    ("src/assets/gltfs", "gltfs"),   # (local_dir, oss_prefix)
    ("src/assets/videos", "videos"),
]

# Files smaller than this are uploaded in one shot; larger use multipart.
MULTIPART_THRESHOLD = 100 * 1024 * 1024   # 100 MB
PART_SIZE = 50 * 1024 * 1024              # 50 MB per part
NUM_THREADS = 8


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_auth_and_bucket(args):
    ak_id  = args.access_key_id     or os.environ.get("OSS_ACCESS_KEY_ID")
    ak_sec = args.access_key_secret or os.environ.get("OSS_ACCESS_KEY_SECRET")
    bucket = args.bucket            or os.environ.get("OSS_BUCKET")
    ep     = args.endpoint          or os.environ.get("OSS_ENDPOINT")

    missing = [k for k, v in [
        ("OSS_ACCESS_KEY_ID",     ak_id),
        ("OSS_ACCESS_KEY_SECRET", ak_sec),
        ("OSS_BUCKET",            bucket),
        ("OSS_ENDPOINT",          ep),
    ] if not v]
    if missing:
        sys.exit(f"Missing required config: {', '.join(missing)}")

    auth = oss2.Auth(ak_id, ak_sec)
    return oss2.Bucket(auth, f"https://{ep}", bucket)


def oss_key(oss_dir_prefix, filename, global_prefix):
    parts = [p for p in [global_prefix, oss_dir_prefix, filename] if p]
    return "/".join(parts)


def file_exists_in_oss(bucket, key):
    try:
        bucket.head_object(key)
        return True
    except oss2.exceptions.NoSuchKey:
        return False


def upload_file(bucket, local_path: Path, key: str):
    size = local_path.stat().st_size

    with tqdm(
        total=size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=local_path.name,
        leave=False,
        ncols=90,
    ) as bar:
        if size < MULTIPART_THRESHOLD:
            # Single-part upload
            with open(local_path, "rb") as fh:
                bucket.put_object(
                    key,
                    SizedFileAdapter(fh, size),
                    progress_callback=lambda consumed, total: bar.update(consumed - bar.n),
                )
        else:
            # Multipart upload with auto part sizing
            part_size = determine_part_size(size, preferred_size=PART_SIZE)
            upload_id = bucket.init_multipart_upload(key).upload_id
            parts = []

            with open(local_path, "rb") as fh:
                part_number = 1
                offset = 0
                while offset < size:
                    chunk = min(part_size, size - offset)
                    result = bucket.upload_part(
                        key, upload_id, part_number,
                        SizedFileAdapter(fh, chunk),
                        progress_callback=lambda consumed, total, _bar=bar: _bar.update(consumed - _bar.n),
                    )
                    parts.append(PartInfo(part_number, result.etag))
                    offset += chunk
                    part_number += 1

            bucket.complete_multipart_upload(key, upload_id, parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Upload assets to Alibaba Cloud OSS")
    parser.add_argument("--access-key-id",     default=None)
    parser.add_argument("--access-key-secret",  default=None)
    parser.add_argument("--bucket",             default=None)
    parser.add_argument("--endpoint",           default=None)
    parser.add_argument("--prefix",             default=os.environ.get("OSS_PREFIX", ""),
                        help="Global key prefix inside the bucket")
    parser.add_argument("--force", action="store_true",
                        help="Re-upload even if object already exists in OSS")
    args = parser.parse_args()

    bucket = build_auth_and_bucket(args)

    total_files = 0
    skipped = 0
    uploaded = 0
    failed = []

    for local_dir, oss_dir in ASSET_DIRS:
        src = REPO_ROOT / local_dir
        if not src.exists():
            print(f"[warn] Directory not found, skipping: {src}")
            continue

        files = sorted(src.iterdir())
        print(f"\n{'─'*60}")
        print(f"  {local_dir}  →  oss://{bucket.bucket_name}/{oss_dir}/")
        print(f"  {len(files)} file(s) found")
        print(f"{'─'*60}")

        for f in files:
            if not f.is_file():
                continue
            total_files += 1
            key = oss_key(oss_dir, f.name, args.prefix)

            if not args.force and file_exists_in_oss(bucket, key):
                print(f"  [skip] {f.name}")
                skipped += 1
                continue

            print(f"  [upload] {f.name}  ({f.stat().st_size / 1e6:.1f} MB)")
            try:
                upload_file(bucket, f, key)
                uploaded += 1
            except Exception as exc:
                print(f"  [ERROR] {f.name}: {exc}")
                failed.append((f.name, str(exc)))

    print(f"\n{'='*60}")
    print(f"Done. total={total_files}  uploaded={uploaded}  skipped={skipped}  failed={len(failed)}")
    if failed:
        print("\nFailed files:")
        for name, err in failed:
            print(f"  {name}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
