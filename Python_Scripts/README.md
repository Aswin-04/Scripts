## Script-1: push_codeforces_problem.py

The `push_codeforces_problems.py` script is a Python automation tool designed to streamline the process of pushing Codeforces problem solutions to a GitHub repository.

It automates the Git workflow by detecting untracked (new) and modified `.cpp` files within a specified directory, such as `/home/eren/Mycode/Code_Forces/<rating>/`, where `<rating>` represents Codeforces categories like `800`, `900`, `1000`, `Contests`, or `Practice`.

For each detected file, the script stages it using `git add <filename>`, commits it with a descriptive message `"Solved Problem <filename>" for new files` and `"Update Problem <filename>" for modified ones`, and pushes the changes to the remote repository.

The script features robust error handling, automatically reverting changes (unstaging and uncommitting) if any step fails. Additionally, it supports a command-line interface via the `push-cfp` executable, providing a convenient and efficient way to push solution files to my Github repository.

---