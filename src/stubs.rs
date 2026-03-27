/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::sync::OnceLock;

use pyrefly_python::module_name::ModuleName;
use starlark_map::small_map::SmallMap;

use crate::analyzer::AnalyzedModule;
use crate::builtins::Builtins;
use crate::stub_analyzer;

/// A lazily initialized map of parsed stubs. Stores the text of the stub files in the `raw` map on
/// creation, and then parses the stub into an AnalyzedModule the first time it's accessed.
#[derive(Debug)]
pub struct Stubs {
    raw: SmallMap<ModuleName, String>,
    parsed: SmallMap<ModuleName, OnceLock<AnalyzedModule>>,
}

impl Stubs {
    pub fn new() -> Self {
        let bundle = lifeguard_stubs::bundled_stubs().unwrap();
        let mut raw = SmallMap::new();
        let mut parsed = SmallMap::new();
        for (path, val) in bundle {
            let key = ModuleName::from_relative_path(&path).unwrap();
            raw.insert(key, val);
            parsed.insert(key, OnceLock::new());
        }
        Self { raw, parsed }
    }

    /// Get the analysis output for a stub module, running the analysis if it hasn't happened yet.
    pub fn get(&self, key: &ModuleName) -> Option<&AnalyzedModule> {
        let raw = self.raw.get(key)?;
        let parsed = self.parsed.get(key)?;
        let ret = parsed.get_or_init(|| stub_analyzer::analyze_str(*key, raw, self));
        Some(ret)
    }

    /// Get an iterator to the name and contents of the raw stub sources.
    pub fn raw_sources_iter(&self) -> impl Iterator<Item = (&ModuleName, &String)> {
        self.raw.iter()
    }

    /// Get the raw source text for a stub module by name.
    pub fn get_raw_source(&self, key: &ModuleName) -> Option<&str> {
        self.raw.get(key).map(|s| s.as_str())
    }

    /// Get the analysis output for the builtins module, running it if it hasn't happened yet.
    pub fn builtins(&self) -> Builtins<'_> {
        // We should panic if builtins is not in the stubs, so unwrap is fine here.
        Builtins::new(self.get(&ModuleName::builtins()).unwrap())
    }
}

#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use lifeguard_stubs;
    use ruff_python_ast::name::Name;

    use super::*;

    #[test]
    fn test_bundled_stubs() {
        let bundle = lifeguard_stubs::bundled_stubs().unwrap();
        let key = PathBuf::from("builtins.pyi");
        assert!(bundle.contains_key(&key));
        let builtins = bundle.get(&key).unwrap();
        assert!(builtins.contains("class filter"));
    }

    #[test]
    fn test_lazy_parsing() {
        let stubs = Stubs::new();
        let key = ModuleName::from_str("builtins");
        assert!(stubs.raw.contains_key(&key));
        assert!(stubs.parsed.contains_key(&key));
        // parsed value is uninitialized
        assert!(stubs.parsed.get(&key).unwrap().get().is_none());
        // gets and initializes the map entry
        let stub = stubs.get(&key);
        assert!(stub.is_some());
        assert!(stubs.parsed.get(&key).unwrap().get().is_some());
    }

    #[test]
    fn test_builtins_lookup() {
        let stubs = Stubs::new();
        let builtins = stubs.builtins();
        let list = Name::new("list");
        assert!(builtins.get(&list).is_some());
        assert!(builtins.is_class(&list));
    }

    #[test]
    fn test_shared_lookup() {
        let stubs = Stubs::new();
        let key = ModuleName::from_str("lifeguard_test");
        let test = stubs.get(&key);
        assert!(test.is_some());
        assert!(
            test.unwrap()
                .classes
                .contains(&ModuleName::from_str("lifeguard_test.A"))
        );
    }
}
