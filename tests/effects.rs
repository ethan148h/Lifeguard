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
    fn test_top_level_imported_var_assignment() {
        let code = r#"
import a
a.x = 10  # E: imported-var-mutation
"#;
        check_effects(code);
    }

    #[test]
    fn test_function_imported_var_assignment() {
        let code = r#"
import a

def f():
    a.x = 10  # E: imported-var-mutation
"#;
        check_effects(code);
    }

    #[test]
    fn test_global_var_assignment() {
        let code = r#"
a = 10

def f():
    global a
    a = 20  # E: global-var-assign
"#;
        check_effects(code);
    }

    #[test]
    fn test_global_var_subscript_assignment() {
        let code = r#"
a = [1, 2, 3]

def f():
    a[2] = 20  # E: global-var-mutation
"#;
        check_effects(code);
    }

    #[test]
    fn test_global_var_attr_assignment() {
        let code = r#"
a = A()  # E: unknown-function-call

def f():
    a.x = 20  # E: global-var-mutation
"#;
        check_effects(code);
    }

    #[test]
    fn test_unknown_function_call() {
        let code = r#"
a = (x + y)(z)  # E: unknown-function-call
"#;
        check_effects(code);
    }
}
