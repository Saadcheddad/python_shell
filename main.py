import sys
import os
import subprocess

def main():
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            line = sys.stdin.readline().strip()
            if not line:
                continue

            parts = line.split(" ")
            command = parts[0]
            args = parts[1:]
            shell_builtins = {"echo", "exit", "type","pwd"}

            if command == "exit":
                if len(parts) > 1 and parts[1] == "0":
                    sys.exit(0)
                elif len(parts) > 1 and parts[1] == "1":
                    sys.exit("exit command error: exit 0 is the right command")
                else:
                    print("Error: Usage is 'exit 0'")
                    continue
            elif command=="pwd":
                print(os.getcwd())
                continue
            elif command == "type":
                if len(parts) > 1:
                    word = parts[1]

                    # Check if the command is a built-in
                    if word in shell_builtins:
                        print(f"{word} is a shell builtin")
                        continue

                    # Check if the command is in the PATH
                    path_directories = os.environ["PATH"].split(os.pathsep)
                    for directory in path_directories:
                        fullpath = os.path.join(directory, word)
                        if os.access(fullpath, os.X_OK):  # Check if it's executable
                            print(f"{word} is {fullpath}")
                            break
                    else:
                        print(f"{word}: not found")
                else:
                    print("type: missing argument")
                continue

            elif command == "echo":
                print(" ".join(parts[1:]))
                continue

            # Handle external commands
            path_directories = os.environ["PATH"].split(os.pathsep)
            for directory in path_directories:
                fullpath = os.path.join(directory, command)
                if os.access(fullpath, os.X_OK):  # Check if it's executable
                    try:
                        # Execute the command with arguments
                        result = subprocess.run([command] + args, executable=fullpath, text=True, capture_output=True)
                        # Print the output of the program
                        if result.stdout:
                            print(result.stdout, end="")
                        if result.stderr:
                            print(result.stderr, end="")
                    except Exception as e:
                        print(f"Error executing {command}: {e}")
                    break
            else:
                print(f"{command}: command not found")

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected (Ctrl+C).")
            break
        except IndexError:
            print("Error: Invalid input.")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()