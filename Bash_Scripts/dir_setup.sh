#!/bin/bash

# Assign the current working directory to a variable
DIR=$(pwd)

# Create the .vscode directory inside the current directory
mkdir -p "$DIR/.vscode"

# Create the tasks.json file inside the .vscode directory and add the modified JSON content
cat <<EOL > "$DIR/.vscode/tasks.json"
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "compile and run",
            "type": "shell",
            "command": "mkdir -p bin && g++ -std=c++17 -o bin/\${fileBasenameNoExtension} \${file} && ./bin/\${fileBasenameNoExtension} < input.txt > output.txt",
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
EOL

# Create empty input.txt and output.txt files in the current directory
touch "$DIR/input.txt"
touch "$DIR/output.txt"
touch "$DIR/error.txt"

echo "Setup complete. tasks.json, input.txt, output.txt and error.txt have been created in $DIR."
