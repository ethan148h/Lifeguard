# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from contextlib import contextmanager
from typing import Generator

def use_python_stack_traces() -> None: ...
@contextmanager
def StackTraceGuard() -> Generator[None, None, None]: no_effects()
def is_under_guard() -> bool: no_effects()
def is_opted_in() -> bool: no_effects()
