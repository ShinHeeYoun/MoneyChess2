import subprocess
import datetime
import os
import sys

def update_readme_and_push(commit_msg: str, readme_update: str):
    """
    Updates the README.md with technical documentation, commits all changes, and pushes.
    """
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(repo_path, "README.md")
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    header = f"## [{date_str}] {commit_msg}\n"
    
    # Prepend or append to README. Assuming append for logging style.
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(readme_update + "\n\n")
        
    # Git commands
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, check=True)
        print(f"Committed changes: {commit_msg}")
        
        # Push with timeout and error handling
        result = subprocess.run(
            ["git", "push", "origin", "main"], 
            cwd=repo_path, 
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"[WARNING] Git push failed (Exit Code {result.returncode}):\n{result.stderr}", file=sys.stderr)
        else:
            print("Successfully pushed changes to remote.")
            
    except subprocess.TimeoutExpired:
        print("[WARNING] Git push operation timed out. Changes committed locally.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"[WARNING] Git operation failed: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[WARNING] Unexpected error during Git workflow: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Test execution or CLI usage
    if len(sys.argv) > 2:
        update_readme_and_push(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python git_helper.py \"Commit Message\" \"- Update description...\"")
