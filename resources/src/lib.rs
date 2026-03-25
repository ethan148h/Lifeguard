/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::env;
use std::io::Read;
use std::path::Component;
use std::path::PathBuf;

use anyhow::Context as _;
use starlark_map::small_map::SmallMap;
use tar::Archive;
use zstd::stream::read::Decoder;

const BUNDLED_STUBS_BYTES: &[u8] =
    include_bytes!(concat!(env!("OUT_DIR"), "/lifeguard_stubs.tar.zst"));

fn is_stub_directory(component: &Option<Component>) -> bool {
    component
        .map(|comp| comp.as_os_str())
        .map(|dir| dir == "stdlib" || dir == "shared")
        .unwrap_or(false)
}

pub fn bundled_stubs() -> anyhow::Result<SmallMap<PathBuf, String>> {
    let decoder = Decoder::new(BUNDLED_STUBS_BYTES)?;
    let mut archive = Archive::new(decoder);
    let entries = archive
        .entries()
        .context("Cannot query all entries in typeshed archive")?;

    let mut items = SmallMap::new();
    for maybe_entry in entries {
        let mut entry = maybe_entry.context("Cannot read individual entry in typeshed archive")?;
        if entry.header().entry_type().is_dir() {
            // Skip directories
            continue;
        }
        let relative_path_context = entry
            .path()
            .context("Cannot extract path from archive entry")?;
        let mut relative_path_components = relative_path_context.components();
        let first_component = relative_path_components.next();
        if !is_stub_directory(&first_component) {
            continue;
        }
        let relative_path = relative_path_components.collect::<PathBuf>();
        if relative_path.extension().is_none_or(|ext| ext != "pyi") {
            continue;
        }
        let size = entry.size();
        let mut contents = String::with_capacity(size as usize);
        entry
            .read_to_string(&mut contents)
            .context("Cannot read content of archive entry")?;
        items.entry(relative_path).or_insert(contents);
    }
    Ok(items)
}
