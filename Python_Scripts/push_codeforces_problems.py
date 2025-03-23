#!/usr/bin/env python3

import subprocess
import sys
import os

def run_git_command(command, path, error_message):
  try:
    result = subprocess.run(
      command, cwd=path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30 
    )
    return result.stdout.strip()
  except subprocess.CalledProcessError as e:
    print(f"{error_message}\n\n{e.stderr.strip()}")
    return None
  except subprocess.TimeoutExpired as e:
    print(f"Command '{' '.join(command)}' timed out after {e.timeout} seconds.")
    return None

def push_to_github(problem_name, path, is_modified):
  if  run_git_command(["git", "add", problem_name], path, f"Error while staging {problem_name}") is None:
    print(f"Failed to stage {problem_name}.\nAborting...")

  action = "Update" if is_modified else "Solved"
  commit_message = f"{action} Problem {problem_name.rsplit(".", 1)[0]}"
  if  run_git_command(["git", "commit", "-m", commit_message], path, f"Error while committing {problem_name}") is None:
    print(f"Failed to commit {problem_name}.\nUnstaging changes..")
    
    if run_git_command(["git", "restore", "--staged", problem_name], path, "Error restoring staged file") is None:
      print(f"Failed to unstage {problem_name}. Manual intervention required")
    sys.exit(1)

  if run_git_command(["git", "push"], path, f"Error pushing {problem_name}") is not None:
    print(f"Successfully pushed {problem_name}")
  else:
    if run_git_command(["git", "reset", "--soft", "HEAD~1"], path, "Error uncommitting changes.") is None:
      print(f"Failed to uncommit {problem_name}. Manual intervention required.")
    
    if run_git_command(["git", "restore", "--staged", problem_name], path, "Error restoring staged file") is None:
      print(f"Failed to unstage {problem_name}. Manual intervention required")
    print(f"\nReverted changes successfully for {problem_name}.")
    sys.exit(1)

valid_ratings = {"800", "900", "1000", "Contests", "Practice"}

if len(sys.argv) < 2:
  print("Error: Invalid argument.\nUsage: push-cfp <problem_rating>\nExample: push-cfp 1000")
  sys.exit(1)

rating = sys.argv[1]

if rating not in valid_ratings:
  print(f"Error: Invalid argument '{rating}.\nMust be one of {valid_ratings}.")
  sys.exit(1)

path=f"/home/eren/Mycode/Code_Forces/{rating}"

if not os.path.isdir(path):
  print(f"Invalid path: {path}")
  sys.exit(1)

git_status = run_git_command(["git", "status", "--porcelain"], path, "Error executing git status")

untracked_files = []
modified_files = []


for line in git_status.split("\n"):
  status, file_path = line.strip().split()
  if status.startswith("??") and file_path.endswith(".cpp"): #untracked files
    if file_path.startswith(rating):
      untracked_files.append(os.path.basename(file_path))
  elif status.startswith("M") and file_path.endswith(".cpp"):
    if file_path.startswith(rating):
      modified_files.append(os.path.basename(file_path))

if not untracked_files and not modified_files:
  print("No files to push, working tree is clean.")
  sys.exit(0)

for file in untracked_files:
  push_to_github(file, path, False)

for file in modified_files:
  push_to_github(file, path, True)

sys.exit(0)


