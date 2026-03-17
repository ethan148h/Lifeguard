# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe
def greet(name):
    return f"Hello, {name}"


class Config:
    DEBUG = False
    VERSION = "1.0"
