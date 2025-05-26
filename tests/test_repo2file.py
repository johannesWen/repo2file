# test_repo2file.py
# MIT License
#
# Copyright (c)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pytest
import runpy

# Import the functions to be tested.
from repo2file.__main__ import collect_source_files, main


def test_collect_source_files(tmp_path):
    """
    Test that files with specified extensions are collected,
    headers are added, and files with non-targeted extensions are skipped.
    """
    # Create a Python file.
    file_py = tmp_path / "file1.py"
    file_py.write_text("print('Hello World')", encoding="utf-8")

    # Create a text file.
    file_txt = tmp_path / "file2.txt"
    file_txt.write_text("This is a text file.", encoding="utf-8")

    # Create a markdown file which should not be collected.
    file_md = tmp_path / "file3.md"
    file_md.write_text("# Markdown File", encoding="utf-8")

    # Call the function with extensions .py and .txt.
    result = collect_source_files(str(tmp_path), [".py", ".txt"])

    # Verify that the Python and text files are included.
    assert "print('Hello World')" in result
    assert "This is a text file." in result

    # Verify that the markdown file content is not included.
    assert "# Markdown File" not in result

    # Verify that file header lines are added.
    assert "# ---" in result


def test_ignore_virtualenv(tmp_path):
    """
    Test that directories named as virtual environments (e.g., 'venv') are ignored.
    """
    # Create a virtual environment directory.
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    venv_file = venv_dir / "ignore.py"
    venv_file.write_text("print('Should be ignored')", encoding="utf-8")

    # Create a normal file that should be included.
    include_file = tmp_path / "include.py"
    include_file.write_text("print('Should be included')", encoding="utf-8")

    result = collect_source_files(str(tmp_path), [".py"])

    # Check that the normal file's content is in the result.
    assert "print('Should be included')" in result
    # Ensure that the virtual environment file's content is not.
    assert "print('Should be ignored')" not in result


def test_deterministic_ordering(tmp_path):
    """
    Verify that files are processed in a deterministic, sorted order.
    """
    # Create files in an unsorted order.
    file_b = tmp_path / "b.py"
    file_b.write_text("print('B')", encoding="utf-8")

    file_a = tmp_path / "a.py"
    file_a.write_text("print('A')", encoding="utf-8")

    result = collect_source_files(str(tmp_path), [".py"])

    header_a = f"# --- {file_a} ---"
    header_b = f"# --- {file_b} ---"

    assert header_a in result
    assert header_b in result
    # Ensure the header for 'a.py' appears before the header for 'b.py'.
    assert result.index(header_a) < result.index(header_b)


def test_no_matching_files(tmp_path):
    """
    Test that if there are no files matching the extensions, an empty string is returned.
    """
    # Create a file with a non-targeted extension.
    file_md = tmp_path / "file.md"
    file_md.write_text("Some markdown content", encoding="utf-8")

    result = collect_source_files(str(tmp_path), [".py"])

    # Since no .py files exist, the result should be empty.
    assert result == ""


def test_collect_source_files_exception(monkeypatch, tmp_path, capsys):
    """
    Test that collect_source_files properly handles an exception during file read.
    This test monkeypatches open() to throw an exception when reading a specific file.
    """
    # Create a file that will simulate a read error.
    bad_file = tmp_path / "bad.py"
    bad_file.write_text("This content won't be read", encoding="utf-8")
    
    # Create a normal file that should be read.
    good_file = tmp_path / "good.py"
    good_file.write_text("print('Good file')", encoding="utf-8")
    
    # Save original open function.
    original_open = open
    def fake_open(file, mode="r", *args, **kwargs):
        if file == str(bad_file):
            raise Exception("Simulated read error")
        return original_open(file, mode, *args, **kwargs)
    
    monkeypatch.setattr("builtins.open", fake_open)
    
    result = collect_source_files(str(tmp_path), [".py"])
    
    # Check that an error message was printed.
    captured = capsys.readouterr().out
    assert "Error reading" in captured
    # The good file should be included in the output.
    assert "print('Good file')" in result
    # The bad file content should not be included.
    assert "This content won't be read" not in result


def test_main_direct_call(tmp_path, monkeypatch, capsys):
    """
    Test the main() function by directly calling it after monkeypatching sys.argv.
    """
    # Create a sample Python file in the temporary directory.
    sample_file = tmp_path / "sample.py"
    sample_file.write_text("print('Hello from main direct call')", encoding="utf-8")

    # Setup command line arguments:
    # - Directory to search (-d) is the tmp_path.
    # - Output file (-o) will be created inside tmp_path.
    # - Extensions (-e) is .py so that our sample file is collected.
    output_file = str(tmp_path / "output_direct.txt")
    monkeypatch.setattr("sys.argv", [
        "repo2file", "-d", str(tmp_path), "-o", output_file, "-e", ".py"
    ])

    # Directly call main().
    main()

    # Verify the output file was created and contains the expected content.
    assert os.path.exists(output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Hello from main direct call" in content


def test_main_run_module(tmp_path, monkeypatch, capsys):
    import sys
    # Remove the module from sys.modules to avoid the warning.
    sys.modules.pop("repo2file.__main__", None)

    # Create a sample Python file in the temporary directory.
    sample_file = tmp_path / "sample_run.py"
    sample_file.write_text("print('Hello from main run module')", encoding="utf-8")

    # Setup command line arguments.
    output_file = str(tmp_path / "output_run_module.txt")
    monkeypatch.setattr("sys.argv", [
        "repo2file", "-d", str(tmp_path), "-o", output_file, "-e", ".py"
    ])

    # Run the module as if it were executed as a script.
    runpy.run_module("repo2file.__main__", run_name="__main__")

    # Verify that the output file was created and contains the expected content.
    assert os.path.exists(output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Hello from main run module" in content


def test_main_exception_write(monkeypatch, tmp_path, capsys):
    """
    Test that main() handles an exception during file writing.
    This test monkeypatches open() to simulate an exception when writing the output file.
    """
    # Create a sample file that will be collected.
    sample_file = tmp_path / "sample.py"
    sample_file.write_text("print('Sample file')", encoding="utf-8")
    
    output_file = str(tmp_path / "output_exception.txt")
    
    # Save original open function.
    original_open = open
    def fake_open(file, mode="r", *args, **kwargs):
        if file == output_file and "w" in mode:
            raise Exception("Simulated write error")
        return original_open(file, mode, *args, **kwargs)
    
    monkeypatch.setattr("builtins.open", fake_open)
    
    monkeypatch.setattr("sys.argv", [
        "repo2file", "-d", str(tmp_path), "-o", output_file, "-e", ".py"
    ])
    
    # Run main() which should attempt to write and catch the exception.
    main()
    
    captured = capsys.readouterr().out
    assert "Error writing to output file" in captured
