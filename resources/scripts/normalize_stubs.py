#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe
"""
Script to normalize all .pyi files in resources/stubs by merging overload effects.
"""

import sys
from pathlib import Path

from .merge_overload_effects import merge_overload_effects


def get_stubs_dir():
    # Get the stubs directory path from command line or use default relative path
    if len(sys.argv) > 1:
        stubs_dir = Path(sys.argv[1])
    else:
        # Default: ../stubs relative to this script
        # This script is at resources/scripts/normalize_stubs.py
        # Stubs are at resources/stubs/
        # Resolve symlinks to get the real source file location
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        stubs_dir = script_dir.parent / "stubs"

    if not stubs_dir.exists():
        print(f"Error: Stubs directory not found at {stubs_dir}")
        print("Usage: normalize_stubs.py [stubs_directory]")
        sys.exit(1)

    return stubs_dir


def main():
    stubs_dir = get_stubs_dir()
    pyi_files = list(stubs_dir.rglob("*.pyi"))

    if not pyi_files:
        print(f"No .pyi files found in {stubs_dir}")
        sys.exit(0)

    print(f"Found {len(pyi_files)} .pyi files in {stubs_dir}")
    print()

    # Process each file
    success_count = 0
    error_count = 0

    for pyi_file in sorted(pyi_files):
        try:
            with open(pyi_file, "r") as f:
                content = f.read()

            result = merge_overload_effects(content)

            with open(pyi_file, "w") as f:
                f.write(result)

            print(f"✓ {pyi_file.relative_to(stubs_dir)}")
            success_count += 1
        except Exception as e:
            print(f"✗ {pyi_file.relative_to(stubs_dir)}: {e}")
            error_count += 1

    # Summary
    print()
    print(f"Successfully processed: {success_count}")
    if error_count > 0:
        print(f"Errors: {error_count}")
        sys.exit(1)


if __name__ == "__main__":
    main()
