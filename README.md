# Lifeguard for Lazy Imports
A fast static analysis tool to help Python projects adopt [Lazy Imports](https://peps.python.org/pep-0810/).

Lazy Imports can significantly reduce memory usage, startup times, and import overhead. However, adapting an existing codebase to use Lazy Imports can be both a daunting and tricky task (especially at scale) as there are a variety of patterns that are not compatible with Lazy Imports. Lifeguard provides a robust tool to identify these cases and enable adoption of the feature.

## Project Stage: Beta
Lifeguard is in active development. We are currently iterating on fixing as many bugs as we can and polishing rough edges.

<details>
<summary>View what we have planned!</summary>

### Open items that are very much on our roadmap
- We still need to set up the necessary GitHub actions to fully support external contributors.
- We do not yet release to [PyPI](https://pypi.org/).
- We currently support up to Python 3.14. This means we do not yet support the `lazy` keyword—but we fully intend to support this.
- At this stage, we've tested Lifeguard against 3.12 and 3.14.
- We are actively developing a standalone linter output mode to help users identify which modules in their codebase are compatible with Lazy Imports.
- We plan to add support for easy ingestion of Lifeguard's output to drive Lazy Imports enablement for advanced users.
</details>

## Prerequisites

- **Rust (nightly)** — the crate uses unstable features. Install via [rustup](https://rustup.rs/) and set with `rustup default nightly`.
- **Git** — clone with submodules: `git clone --recurse-submodules https://github.com/facebook/Lifeguard.git`

If you already cloned without `--recurse-submodules`, run `git submodule update --init --recursive`.

## Quick Start

The fastest way to try Lifeguard is the `run_tree` binary, which analyzes every `.py` file under a directory — no manual source DB needed:

```bash
cargo run --bin run_tree <INPUT_DIR> <OUTPUT_PATH>
```

For example, using the bundled sample project:

```bash
cargo run --bin run_tree testdata/sample_project output.json
```

For a full walkthrough including interpreting the output, see [GETTING_STARTED.md](GETTING_STARTED.md).

## Running Lifeguard

For larger projects where you need more control over the source DB, follow these steps:

1. Create a JSON file defining the file structure of your project (file format described below). This should include all source files and all Python dependencies. We provide a script to start this file for you, but you may need to tune it by hand. (As the project matures, we hope to make this process smoother.)
```
cargo run --bin gen_source_db <INPUT_DIR> <OUTPUT_PATH>
```

If your project has library dependencies, you can add the path to your pyproject.toml in a `lifeguard` section:

```
[lifeguard]
site_packages = "/path/to/site-packages"
```

You can find out your site-packages path via `python -m site`

2. Run Lifeguard in one of two modes:
   - **Default**: Prints a high-level analysis of your codebase (% of compatible files, top errors, etc.).
   ```
   cargo run --bin analyzer <DB_PATH> <OUTPUT_PATH>
   ```
   - **Verbose mode**: Shows which specific lines in each module cause incompatibility.
   ```
   cargo run --bin analyzer <DB_PATH> <OUTPUT_PATH> --verbose-output <VERBOSE_OUTPUT_PATH>
   ```

**Example Verbose Output:**
```text
## example.module.foo
### Errors
  Line 17 - ImportedModuleAssignment sys
  Line 38 - UnsafeFunctionCall example.demo.unsafe_method
```

## How does Lifeguard work?
Lifeguard analyzes Python source files for a given target in parallel. It assesses the effects produced within each module and maps Lazy Imports incompatible effects to errors, covering a variety of incompatibilities including implicit imports, side effects, the registry patterns, and metaclasses. The analyzer takes a conservative approach. Any module that we cannot programmatically determine to be safe is marked as unsafe by default. See `docs/` for more information.

Currently, Lifeguard relies on two inputs.
1. `DB_PATH`: This is a JSON file mapping the Python module name to its location on disk. The format of this file is:

    ```json
    {
      "build_map": {
          "foo/bar.py": "/local/usr/disk/foo/bar.py",
          "example/__init__.py": "/local/usr/disk/third-party/example/__init__.py"
      }
    }
    ```

2. `OUTPUT_PATH`: Where to write the JSON output file. The format of this file is:

    ```text
    {
        # Dictionary mapping safe modules to a list of Lazy Imports incompatible modules that must already be loaded for the dictionary key to load lazily
        'LAZY_ELIGIBLE': {
            'module1': [], # Safe to load lazily always
            'module2': ['module3', 'module4'], # Safe to load lazily if module3 and module4 are loaded
            ...
        },
        # Set of modules where we would like to load all of their imports eagerly. These modules are still eligible to be loaded lazily.
        'LOAD_IMPORTS_EAGERLY': {
            'module99',
            'module100',
            ...
        }
    }
    ```

## Implementation
Lifeguard is implemented in Rust. We leverage [ruff](https://github.com/astral-sh/ruff) for AST traversal and re-use several crates from [pyrefly](https://github.com/facebook/pyrefly). We also extend `.pyi` files to support "stubbing" for side effects. Our stubs are stored in the `resources/` folder.

## License
By contributing to Lifeguard, you agree that your contributions will be licensed under the LICENSE file in the root directory of this source tree.
