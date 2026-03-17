# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe
class Resource:
    def __init__(self):
        self.handle = None

    def __del__(self):
        if self.handle:
            self.handle.close()
