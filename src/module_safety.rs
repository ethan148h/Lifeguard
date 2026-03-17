/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use ahash::AHashSet;
use pyrefly_python::module_name::ModuleName;

use crate::errors::SafetyError;

#[derive(Debug)]
pub struct ModuleSafety {
    /// Errors that alter how a module should be imported (lazy/eager)
    pub errors: Vec<SafetyError>,
    /// Errors that alter if a module should eagerly import its imports
    pub force_imports_eager_overrides: Vec<SafetyError>,
    pub implicit_imports: Vec<ModuleName>,
}

impl ModuleSafety {
    pub fn new() -> Self {
        Self {
            errors: Vec::new(),
            force_imports_eager_overrides: Vec::new(),
            implicit_imports: Vec::new(),
        }
    }

    pub fn is_safe(&self) -> bool {
        self.errors.is_empty()
    }

    pub fn has_implicit_imports(&self) -> bool {
        !self.implicit_imports.is_empty()
    }

    pub fn should_load_imports_eagerly(&self) -> bool {
        !self.force_imports_eager_overrides.is_empty()
    }

    pub fn add_error(&mut self, error: SafetyError) {
        self.errors.push(error);
    }

    pub fn add_force_import_override(&mut self, error: SafetyError) {
        assert!(error.kind.requires_eager_loading_imports());
        self.force_imports_eager_overrides.push(error);
    }

    pub fn add_implicit_imports(&mut self, implicit_imports: &AHashSet<ModuleName>) {
        self.implicit_imports.extend(implicit_imports);
    }
}

#[derive(Debug)]
pub enum SafetyResult {
    Ok(ModuleSafety),
    AnalysisError(anyhow::Error),
}

impl SafetyResult {
    pub fn as_safety(&self) -> Option<&ModuleSafety> {
        match self {
            SafetyResult::Ok(safety) => Some(safety),
            _ => None,
        }
    }

    pub fn as_safety_mut(&mut self) -> Option<&mut ModuleSafety> {
        match self {
            SafetyResult::Ok(safety) => Some(safety),
            _ => None,
        }
    }
}
