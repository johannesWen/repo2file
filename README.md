# Repo 2 File

![Coverage](./coverage.svg)

**repo2file** is a Python utility that recursively collects source code from a given directory. It allows you to specify which file extensions to include, ignores common virtual environment directories, and outputs the combined source code into a single file with clear file headers. 

## Table of Contents
- [Repo 2 File](#repo-2-file)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Using Poetry (Recommended)](#using-poetry-recommended)
    - [Using pip install](#using-pip-install)
  - [Usage](#usage)
  - [Example Commands](#example-commands)
  - [Package Structure for Module Execution](#package-structure-for-module-execution)
  - [License](#license)
  - [Contributing](#contributing)



## Features

- **Recursive Traversal:** Automatically traverse directories to collect files.
- **Selective File Collection:** Specify file extensions (e.g., `.py`, `.txt`).
- **Virtual Environment Filtering:** Automatically ignores common virtual environment folders (`venv`, `.venv`, `env`, `.env`).
- **Progress Bar:** Displays a progress bar while processing files using `tqdm`.
- **Concatenated Output:** Combines collected source code with file headers into a single output file.
- **Multiple Execution Modes:** Can be run as a standalone script or as a package module.

## Requirements

- Python 3.9 or later
- [tqdm](https://pypi.org/project/tqdm/)

If you are using [Poetry](https://python-poetry.org/) to manage your project, the required dependencies are defined in the [`pyproject.toml`](pyproject.toml) file.

## Installation

### Using [Poetry](https://python-poetry.org/) (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/johannesWen/repo2file.git
   cd repo2file
   ```
1. Install dependencies:
    ```bash
    poetry install
    ```
### Using pip install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/johannesWen/repo2file.git
   cd repo2file
   ```

1. Install the package using pip:
    ```bash
    pip install .
    ```

## Usage

The script accepts the following command-line arguments:

* `-d`, `--directory` \
    Specifies the directory to search. Defaults to the current directory (.).

* `-e`, `--extensions` \
    Specifies file extensions to collect. You can list one or more (e.g., .py .txt). Defaults to [".py"].

* `-o`, `--output` \
    Specifies the output file name. Defaults to collected_source.txt.

## Example Commands

* Collect Python and toml files from a specific directory and output to a custom file:
```bash
python ./repo2file/__main__.py -d /path/to/project -e .py .toml -o combined_sources.txt
```

## Package Structure for Module Execution

If you prefer to structure your project as a package and run it using Python's module execution, organize your files as follows:

repo2file \
├── \_\_init\_\_.py \
└── \_\_main\_\_.py

You can then run the package with:
```bash
python -m repo2file -d /path/to/project -e .py .txt -o combined_sources.txt
```
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.