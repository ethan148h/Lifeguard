/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::env;
use std::fs::File;
use std::path::Path;
use std::path::PathBuf;

fn get_input_path() -> PathBuf {
    match env::var_os("STUBS_ROOT") {
        Some(root) => {
            // When building with Buck, the filegroup dir is passed in using STUBS_ROOT
            Path::new(&root).join("stubs")
        }
        None => {
            // When building with Cargo, find stubs directory relative to this build.rs
            let manifest_dir = env::var("CARGO_MANIFEST_DIR")
                .expect("CARGO_MANIFEST_DIR should be set when building with Cargo");
            Path::new(&manifest_dir).join("stubs")
        }
    }
}

fn get_output_path() -> Result<PathBuf, std::env::VarError> {
    // When building with Buck, output artifact path is specified directly using this env var
    match env::var_os("OUT") {
        Some(path) => Ok(PathBuf::from(path)),
        None => {
            // When building with Cargo, this env var is the containing directory of the artifact
            let out_dir = env::var("OUT_DIR")?;
            Ok(Path::new(&out_dir).join("lifeguard_stubs.tar.zst"))
        }
    }
}

fn main() -> Result<(), std::io::Error> {
    // TODO: do we need this?
    // Only watch for metadata changes to avoid having Cargo repeatedly crawling for
    // changes in the entire typeshed dir.
    // println!("cargo::rerun-if-changed=third_party/typeshed_metadata.json");

    let input_path = get_input_path();
    let output_path = get_output_path().unwrap();
    let output_file = File::create(output_path)?;
    let encoder = zstd::stream::write::Encoder::new(output_file, 0)?;
    let mut tar = tar::Builder::new(encoder);
    tar.mode(tar::HeaderMode::Deterministic);
    tar.append_dir_all("", input_path)?;
    let encoder = tar.into_inner()?;
    encoder.finish()?;
    Ok(())
}
