# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe
from safer_lazy_imports.lifeguard.testdata.sample_project.importer import greet


def main():
    print(greet("world"))


if __name__ == "__main__":
    main()
