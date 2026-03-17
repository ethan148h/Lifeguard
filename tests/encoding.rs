/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#[cfg(test)]
mod tests {
    use std::io::Write;
    use std::path::PathBuf;

    use anyhow::Result;
    use lifeguard::module_parser::read_and_parse_source;
    use lifeguard::pyrefly::module_name::ModuleName;
    use tempfile::NamedTempFile;

    fn test_parse(code: &[u8]) -> Result<()> {
        let mut temp_file = NamedTempFile::with_suffix(".py")?;
        temp_file.write_all(code)?;
        temp_file.flush()?;

        let path = PathBuf::from(temp_file.path());
        let module_name = ModuleName::from_str("test");
        let ret = read_and_parse_source(&path, module_name, false);
        assert!(ret.is_ok());
        Ok(())
    }

    /// Test lossy decoding of Latin-1 files
    #[test]
    fn test_latin1_encoding() {
        // The byte 0xa6 (¦ broken bar) is valid in Latin-1 but invalid in UTF-8
        let code: &[u8] = b"# -*- coding: latin-1 -*-\nx = \"hello \xa6 world\"\n";
        test_parse(code).unwrap();
    }

    /// Test that regular UTF-8 files still work correctly.
    #[test]
    fn test_utf8_encoding() {
        let code: &[u8] = b"# -*- coding: utf-8 -*-\nx = \"hello world\"\n";
        test_parse(code).unwrap();
    }

    /// Test UTF-8 file with unicode characters (valid UTF-8).
    #[test]
    fn test_utf8_with_unicode() {
        let code = "# -*- coding: utf-8 -*-\nx = \"hello 世界 🌍\"\n";
        test_parse(code.as_bytes()).unwrap();
    }

    /// Test file with multiple invalid UTF-8 bytes (CP1252/Windows-1252 encoding).
    #[test]
    fn test_windows_1252_encoding() {
        // Windows-1252 "smart quotes" (0x93, 0x94) are invalid UTF-8
        let code: &[u8] = b"# -*- coding: cp1252 -*-\nx = \x93hello\x94\n";
        test_parse(code).unwrap();
    }
}
