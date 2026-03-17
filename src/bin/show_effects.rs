/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// Dump effects for a single python file (.py or .pyi).
//
// $ buck run :show_effects <path_to_file.py>
// $ buck run :show_effects <path_to_file.pyi>

use std::path::PathBuf;

use anyhow::Result;
use clap::Parser;
use lifeguard::analyzer;
use lifeguard::debug::print_module_imports_map;
use lifeguard::imports::ImportGraph;
use lifeguard::module_parser;
use lifeguard::pyrefly::module_name::ModuleName;
use lifeguard::pyrefly::sys_info::SysInfo;
use lifeguard::source_map::ModuleProvider;
use lifeguard::test_lib::TestSources;
use lifeguard::traits::SysInfoExt;
use ruff_python_ast::PySourceType;

#[derive(Parser)]
struct Args {
    input_file: PathBuf,
}

fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    let args = Args::parse();
    let module_name = ModuleName::from_str("current_module");
    let path = args.input_file;
    let source = std::fs::read_to_string(&path)?;

    let sources = TestSources::new(&[("current_module", &source)]);
    let sys_info = SysInfo::lg_default();
    let (import_graph, exports) = ImportGraph::make_with_exports(&sources, &sys_info);

    // Run the analysis
    let typ = module_parser::file_source_type(&path).unwrap();
    let is_init = path
        .file_name()
        .is_some_and(|f| f == "__init__.py" || f == "__init__.pyi");
    let module = module_parser::parse_file(&source, typ, module_name, is_init);
    let output = analyzer::analyze(&module, &exports, &import_graph, sources.stubs(), &sys_info);

    // Display output
    let module_effects = output.module_effects;
    let is_stub = typ == PySourceType::Stub;
    module_effects
        .effects
        .pretty_print(&module, &source, !is_stub);

    // Display called imports
    if !module_effects.called_imports.is_empty() {
        println!("\nCalled imports:");
        print_module_imports_map(&module_effects.called_imports);
    }

    // Display pending imports
    if !module_effects.pending_imports.is_empty() {
        println!("\nPending imports:");
        print_module_imports_map(&module_effects.pending_imports);
    }

    Ok(())
}
