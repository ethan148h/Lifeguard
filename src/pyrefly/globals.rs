/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

//! Global variables defined at the top level of a module.
//!
//! We do not include `__doc__` as that has a type that changes based on other variables.

use ruff_python_ast::name::Name;

#[derive(Debug, Clone)]
pub struct Global {
    name: Name,
}

const GLOBALS: &[Global] = &[
    Global::new("__annotations__"),
    Global::new("__builtins__"),
    Global::new("__cached__"),
    Global::new("__debug__"),
    Global::new("__dict__"),
    Global::new("__file__"),
    Global::new("__loader__"),
    Global::new("__name__"),
    Global::new("__package__"),
    Global::new("__path__"),
    Global::new("__spec__"),
    Global::new("__doc__"),
];

impl Global {
    const fn new(name: &'static str) -> Self {
        Self {
            name: Name::new_static(name),
        }
    }

    pub fn globals(_docstring: bool) -> impl Iterator<Item = Global> {
        GLOBALS.iter().cloned()
    }

    #[allow(dead_code)]
    pub fn from_name(name: &Name) -> Option<Global> {
        if name.starts_with("__") && name.ends_with("__") {
            GLOBALS.iter().find(|x| &x.name == name).cloned()
        } else {
            None
        }
    }

    pub fn name(&self) -> &Name {
        &self.name
    }
}
