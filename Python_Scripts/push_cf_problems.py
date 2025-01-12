#!/usr/bin/env python3

import subprocess
import sys

if(len(sys.argv) < 2): 
  print("You forgot to enter the problem rating, BITCH!")
  sys.exit(1)

rating = sys.argv[1]
path=f"/home/eren/Mycode/Code_Forces/{rating}"

try:
  gitstatus = subprocess.run(
    ["git", "status"], 
    cwd=path, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
  )

  if(gitstatus.returncode != 0):
    print(f"Error executing git status: {gitstatus.stderr}")

except FileNotFoundError as e:
  print(f"File not found: {e}")
  print("This might be due to an invalid path or missing git command.")
  sys.exit(1)

except subprocess.CalledProcessError as e:
  print(f"Error processing command: {e}")
  sys.exit(1)

untracked_files = []
has_untracked_files = False

for line in gitstatus.stdout.split("\n"):
  if(line.startswith("Untracked files:")):
    has_untracked_files = True
  
  if has_untracked_files:
    if line.strip() == "": #end of untracked files
      break
    if line.strip().startswith("../"):  #to filter files from other directory
      continue
    if "cpp" in line:
      untracked_files.append(line.strip())

if not has_untracked_files:
  print("There is no untracked files, BITCH!")
  sys.exit(0)

for problem_name in untracked_files:

  try:
    subprocess.run(["git", "add", problem_name], cwd=path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except subprocess.CalledProcessError as e:
    print(f"Error while staging the file {problem_name}: {e}")
    subprocess.run(["git", "reset", "HEAD"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Unstaged {problem_name}. Changes are still in the working directory.")
    sys.exit(1)


  try:
    subprocess.run(
      ["git","commit", "-m", f"Solved Problem {problem_name.rsplit(".", 1)[0]}"], #rsplit to remove .cpp extension
      cwd=path,
      check=True,
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE
    )
  except subprocess.CalledProcessError as e:
    print(f"Error while commiting the file {problem_name}: {e}")
    subprocess.run(["git", "reset", "HEAD"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Unstaged {problem_name}. Changes are still in the working directory.")
    sys.exit(1)

  try:
    subprocess.run(["git", "push"], cwd=path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Successfully pushed: {problem_name}")

  except subprocess.CalledProcessError as e:
    print(f"Error pushing file {problem_name}: {e}")

    subprocess.run(["git", "reset", "--soft", "HEAD~1"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #uncommit
    print(f"Uncommitted changes for {problem_name}. Resetting to the previous commit.")

    subprocess.run(["git", "restore", "--staged", problem_name], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #unstage the file
    print(f"Unstaged {problem_name}. Changes are still in the working directory.")

    sys.exit(1)

