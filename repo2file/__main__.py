#!/usr/bin/env python3
import os
import argparse

try:
    from tqdm import tqdm
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without tqdm
    def tqdm(iterable, **_):
        """Fallback tqdm that just returns the iterable."""
        return iterable

def collect_source_files(directory, extensions):
    """
    Walk through the directory, collect all files matching the given extensions,
    and return their concatenated contents. Ignores common virtual environment folders.
    """
    ignore_dirs = {"venv", ".venv", "env", ".env"}
    matching_files = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Remove virtual environment directories from the traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                matching_files.append(os.path.join(root, file))
                
    collected_code = ""
    # Process each file with a progress bar
    for file_path in tqdm(matching_files, desc="Collecting files", unit="file"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Add a header for clarity between files
            collected_code += f"\n\n# --- {file_path} ---\n\n"
            collected_code += content
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return collected_code

def main():
    parser = argparse.ArgumentParser(
        description="Collect all source code from files in a directory and dump into a single output file."
    )
    parser.add_argument(
        "-d", "--directory", type=str, default=".",
        help="Directory to search (default: current directory)"
    )
    parser.add_argument(
        "-e", "--extensions", type=str, nargs='+', default=[".py"],
        help="File extensions to collect (e.g. .py .txt)"
    )
    parser.add_argument(
        "-o", "--output", type=str, default="collected_source.txt",
        help="Output file name (default: collected_source.txt)"
    )
    args = parser.parse_args()

    collected = collect_source_files(args.directory, args.extensions)
    try:
        with open(args.output, "w", encoding="utf-8") as out_file:
            out_file.write(collected)
        print(f"\nSuccessfully written collected source code to {args.output}")
    except Exception as e:
        print(f"Error writing to output file {args.output}: {e}")

if __name__ == "__main__":
    main()
