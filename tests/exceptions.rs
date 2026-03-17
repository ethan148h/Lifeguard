/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#[cfg(test)]
mod tests {
    use lifeguard::test_lib::*;

    #[test]
    fn test_unhandled_exception() {
        let code = r#"
raise ValueError("bye!")  # E: unhandled-exception
"#;
        check(code);
    }

    #[test]
    fn test_handled_exception() {
        let code = r#"
try:
    raise ValueError("bye!")
except Exception as e:
    ...
"#;
        check(code);
    }

    #[test]
    fn test_raise_in_handler() {
        let code = r#"
try:
    raise ValueError("bye!")
except Exception as e:
    raise ValueError("unhandled!")  # E: unhandled-exception
"#;
        check(code);
    }

    #[test]
    fn test_raise_in_else() {
        let code = r#"
try:
    raise ValueError("bye!")
except Exception as e:
    pass
else:
    raise ValueError("unhandled!")  # E: unhandled-exception
"#;
        check(code);
    }

    #[test]
    fn test_raise_in_finally() {
        let code = r#"
try:
    raise ValueError("bye!")
except Exception as e:
    pass
finally:
    raise ValueError("unhandled!")  # E: unhandled-exception
"#;
        check(code);
    }
}
