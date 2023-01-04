#!/bin/bash

IFS=$'\n'
year=$(date +'%Y')

files_without_header=()

# loop through all changed files
for file in $(git diff --diff-filter=du --name-only --cached); do
    if [[ "$file" =~ ^(aerographer)[\/].*\.(py|pyi)$ ]]; then
        full_path="$(git rev-parse --show-toplevel)/$file"

        # Check for Copyright statement
        if ! head -2 $full_path | grep -q "Copyright $year"; then
            files_without_header+=($file)
        fi
    fi
done

if [ -n "$files_without_header" ]; then
    echo "License header not found in the following files:"
    for f in "${files_without_header[@]}"; do
        echo "   - $f";
    done
    exit 1;
else
    echo "All files have license header.";
    exit 0;
fi