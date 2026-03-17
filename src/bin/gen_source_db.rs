/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// Generate a source DB JSON file from a directory tree of Python files.
//
// $ cargo run --bin gen_source_db <input_dir> <output_path>

use std::collections::BTreeMap;
use std::io::BufWriter;
use std::io::Write;
use std::path::PathBuf;

use anyhow::Context;
use anyhow::Result;
use clap::Parser;
use lifeguard::source_map::is_python_file;
use serde::Serialize;
use walkdir::WalkDir;

#[derive(Parser)]
struct Args {
    /// Directory containing Python files to scan
    input_dir: PathBuf,

    /// Path to output JSON file
    output_path: PathBuf,
}

#[derive(Serialize)]
struct SourceDb {
    build_map: BTreeMap<String, String>,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let input_dir = args.input_dir.canonicalize()?;

    let mut build_map = BTreeMap::new();
    for entry in WalkDir::new(&input_dir)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| is_python_file(e.path()))
    {
        let full_path = entry.path().canonicalize()?;
        let rel_path = full_path
            .strip_prefix(&input_dir)
            .context("file resolved to a path outside of input_dir")?;
        build_map.insert(
            rel_path.to_string_lossy().into_owned(),
            full_path.to_string_lossy().into_owned(),
        );
    }

    let source_db = SourceDb { build_map };
    let output_file = std::fs::File::create(&args.output_path)?;
    let mut writer = BufWriter::new(output_file);
    serde_json::to_writer_pretty(&mut writer, &source_db)?;
    writer.flush()?;

    println!(
        "Wrote {} entries to {}",
        source_db.build_map.len(),
        args.output_path.display()
    );

    Ok(())
}
