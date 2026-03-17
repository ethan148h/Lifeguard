/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use ahash::AHashSet;
use pyrefly_python::module_name::ModuleName;
use ruff_python_ast::PySourceType;

use crate::class::ClassTable;
use crate::exports::Exports;
use crate::imports::ImportGraph;
use crate::module_effects::ModuleEffects;
use crate::module_info::DefinitionTable;
use crate::module_parser::ParsedModule;
use crate::pyrefly::sys_info::SysInfo;
use crate::source_analyzer;
use crate::stub_analyzer;
use crate::stubs::Stubs;

/// A Python module that's been analyzed for definitions and side effects.
///
/// The side effects are computed independently of other modules.
#[derive(Debug)]
pub struct AnalyzedModule {
    pub module_effects: ModuleEffects,
    pub definitions: DefinitionTable,
    pub classes: ClassTable,

    /// Implicit imports in the module.  Filled in later during project analysis.
    pub implicit_imports: AHashSet<ModuleName>,
}

impl AnalyzedModule {
    pub fn empty() -> Self {
        Self {
            module_effects: ModuleEffects::new(),
            definitions: DefinitionTable::empty(),
            classes: ClassTable::empty(),
            implicit_imports: AHashSet::new(),
        }
    }
}

/// Processes a Python module AST and figures out things like definitions and effects.
pub trait Analyzer<'a> {
    fn new(
        parsed_module: &'a ParsedModule,
        exports: &'a Exports,
        import_graph: &'a ImportGraph,
        stubs: &'a Stubs,
        sys_info: &'a SysInfo,
    ) -> Self;

    fn analyze(self) -> AnalyzedModule;
}

// Type alias for analyze functions
pub type AnalyzeFn = fn(&ParsedModule, &Exports, &ImportGraph, &Stubs, &SysInfo) -> AnalyzedModule;

// Analyze a single module
pub fn analyze(
    parsed_module: &ParsedModule,
    exports: &Exports,
    import_graph: &ImportGraph,
    stubs: &Stubs,
    sys_info: &SysInfo,
) -> AnalyzedModule {
    let analyzer: AnalyzeFn = match parsed_module.source_type {
        PySourceType::Python => source_analyzer::analyze,
        PySourceType::Stub => stub_analyzer::analyze,
        _ => panic!("Unexpected module type"),
    };
    analyzer(parsed_module, exports, import_graph, stubs, sys_info)
}
