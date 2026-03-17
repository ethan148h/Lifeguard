/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use tracing::debug;

use crate::exports::ExportType;
use crate::exports::Exports;
use crate::imports::ImportGraph;
use crate::module_effects::ModuleImportsMap;

/// Print exports table in sorted format for debugging.
/// Outputs one line per export in format:
///   class | global | re_export: <module_name>
pub fn print_exports(exports: &Exports) {
    let mut lines = Vec::new();

    // Collect exports
    for (name, export) in exports.get_exports() {
        let prefix = match export.typ {
            ExportType::Class => "class",
            ExportType::Function => "function",
            ExportType::Global => "global",
        };
        lines.push(format!("{}: {}", prefix, name.as_str()));
    }

    // Collect re-exports
    for (name, _) in exports.get_re_exports() {
        lines.push(format!("re-export: {}", name.as_module_name().as_str()));
    }

    // Sort and print
    lines.sort();
    for line in lines {
        println!("{}", line);
    }
}

pub fn print_import_cycles(imports: &ImportGraph) {
    let cycles = imports.graph.find_cycles();
    for c in cycles {
        println!("cycle {{");
        for m in imports.graph.cycle_names(&c) {
            println!("  {}", m);
        }
        println!("}}");
    }
}

/// Print the called_imports / pending_imports map from the ModuleEffects struct
pub fn print_module_imports_map(imports_map: &ModuleImportsMap) {
    let mut scopes: Vec<_> = imports_map.iter().collect();
    scopes.sort_by_key(|(s, _)| s.as_str());
    for (scope, imports) in scopes {
        let mut imports: Vec<_> = imports.iter().collect();
        imports.sort_by_key(|i| i.as_str());
        println!("  {}:", scope.as_str());
        for import in imports {
            println!("    - {}", import.as_str());
        }
    }
}

/// Read and log VmRSS and VmHWM from /proc/self/status (Linux only).
pub fn report_memory(label: &str) {
    if let Ok(status) = std::fs::read_to_string("/proc/self/status") {
        let mut rss = None;
        let mut hwm = None;
        for line in status.lines() {
            if line.starts_with("VmRSS:") {
                rss = Some(line.trim());
            } else if line.starts_with("VmHWM:") {
                hwm = Some(line.trim());
            }
        }
        if let (Some(rss), Some(hwm)) = (rss, hwm) {
            debug!("[memory] {}: {} | {}", label, rss, hwm);
        }
    }
}

/// Report peak resident set size from /proc/self/status.
pub fn report_peak_memory() {
    if let Ok(status) = std::fs::read_to_string("/proc/self/status") {
        for line in status.lines() {
            if line.starts_with("VmHWM:") {
                debug!("Peak memory (VmHWM): {}", line.trim());
                return;
            }
        }
    }
}
