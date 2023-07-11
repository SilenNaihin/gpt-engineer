import os
import sys
from typing import Tuple
import pexpect


def run_specific_agent(task: str) -> Tuple[str, int]:
    # Ensure the directory for the project exists
    os.makedirs("projects/my-new-project", exist_ok=True)

    # Create/overwrite the prompt file with the task
    with open("projects/my-new-project/prompt", "w") as prompt_file:
        prompt_file.write(task)

    # Run the gpt-engineer command
    child = pexpect.spawn("gpt-engineer projects/my-new-project")

    # Send 'c' and 'enter' keys
    child.sendline("c")
    child.sendline()
    child.sendline()

    # Create a loop to continuously read output
    while True:
        try:
            child.expect("\n")  # This waits until a newline appears
            print(child.before.decode())  # This prints the line
        except pexpect.EOF:
            break  # No more output, break the loop

    # Check the exit status
    child.close()  # Close the child process

    # Return child process's exit status and any error messages
    return child.before.decode(), child.exitstatus


if __name__ == "__main__":
    # The first argument is the script name itself, second is the task
    if len(sys.argv) != 2:
        print("Usage: python script.py <task>")
        sys.exit(1)
    task = sys.argv[1]
    run_specific_agent(task)
