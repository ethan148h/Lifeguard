# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import subprocess
import sys
import sysconfig


def get_lifeguard_bin() -> str:
    lifeguard_exe = "lifeguard" + sysconfig.get_config_var("EXE")
    lifeguard_bin = os.path.join(sysconfig.get_path("scripts"), lifeguard_exe)
    if os.path.isfile(lifeguard_bin):
        return lifeguard_bin
    user_scheme = sysconfig.get_preferred_scheme("user")
    lifeguard_bin = os.path.join(
        sysconfig.get_path("scripts", scheme=user_scheme), lifeguard_exe
    )
    if os.path.isfile(lifeguard_bin):
        return lifeguard_bin
    return "lifeguard"


if __name__ == "__main__":
    proc = subprocess.run([get_lifeguard_bin(), *sys.argv[1:]])
    sys.exit(proc.returncode)
