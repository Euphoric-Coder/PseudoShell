import os
import shutil
import sys
import readline

# Initialize command history and autocompletion
readline.parse_and_bind("tab: complete")
readline.set_completer_delims(" \t\n;")


def list_directory(args):
    """List the contents of the directory with optional flags."""
    path = "." if not args or args[0].startswith("-") else args[0]
    show_all = "-a" in args
    long_format = "-l" in args
    ignore_hidden = "-I" in args

    try:
        files = os.listdir(path)
        if ignore_hidden:
            files = [f for f in files if not f.startswith(".")]
        if not show_all:
            files = [f for f in files if not f.startswith(".")]
        if long_format:
            for file in files:
                stats = os.stat(file)
                print(f"{file} - {stats.st_size} bytes")
        else:
            print(" ".join(files))
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory")


def change_directory(args):
    """Change the current working directory."""
    if not args:
        print("cd: missing operand")
        return
    try:
        os.chdir(args[0])
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")


def print_working_directory(_):
    """Print the current working directory."""
    print(os.getcwd())


def make_directory(args):
    """Create a directory."""
    if not args:
        print("mkdir: missing operand")
        return
    try:
        os.mkdir(args[0])
    except FileExistsError:
        print(f"mkdir: cannot create directory '{args[0]}': File exists")


def remove_directory(args):
    """Remove a directory."""
    if not args:
        print("rmdir: missing operand")
        return
    try:
        os.rmdir(args[0])
    except FileNotFoundError:
        print(f"rmdir: failed to remove '{args[0]}': No such file or directory")


def remove_file(args):
    """Remove a file."""
    if not args:
        print("rm: missing operand")
        return
    try:
        os.remove(args[0])
    except FileNotFoundError:
        print(f"rm: cannot remove '{args[0]}': No such file or directory")


def create_file(args):
    """Create an empty file."""
    if not args:
        print("touch: missing operand")
        return
    with open(args[0], "w") as f:
        pass


def read_file(args):
    """Display the content of a file."""
    if not args:
        print("cat: missing operand")
        return
    try:
        with open(args[0], "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"cat: {args[0]}: No such file or directory")


def copy_file(args):
    """Copy files or directories."""
    if len(args) < 2:
        print("cp: missing file operand")
        return
    try:
        shutil.copy(args[0], args[1])
    except FileNotFoundError:
        print(f"cp: cannot stat '{args[0]}': No such file or directory")


def move_file(args):
    """Move files or directories."""
    if len(args) < 2:
        print("mv: missing file operand")
        return
    try:
        shutil.move(args[0], args[1])
    except FileNotFoundError:
        print(f"mv: cannot stat '{args[0]}': No such file or directory")


def display_help(args):
    """Display help information for each command."""
    help_text = """
    Supported commands:
    - ls [options] [path]: List directory contents.
    - cd [path]: Change the current directory.
    - pwd: Print the current working directory.
    - mkdir [directory]: Create a new directory.
    - rmdir [directory]: Remove a directory.
    - rm [file]: Remove a file.
    - touch [file]: Create an empty file.
    - cat [file]: Display file content.
    - cp [source] [destination]: Copy files or directories.
    - mv [source] [destination]: Move files or directories.
    - exit: Exit the CLI.
    Options for ls:
    - -a: Show all files including hidden.
    - -l: Long format listing.
    - -I: Ignore hidden files.
    """
    print(help_text)


def execute_command(command_input):
    """Parse and execute commands, handling chaining and errors."""
    commands = {
        "ls": list_directory,
        "cd": change_directory,
        "pwd": print_working_directory,
        "mkdir": make_directory,
        "rmdir": remove_directory,
        "rm": remove_file,
        "touch": create_file,
        "cat": read_file,
        "cp": copy_file,
        "mv": move_file,
        "help": display_help,
    }

    # Split commands by chaining symbols like ';'
    command_chain = command_input.split(";")
    for command in command_chain:
        parts = command.strip().split()
        if not parts:
            continue

        command_name, *args = parts
        if command_name == "exit":
            sys.exit(0)
        elif command_name in commands:
            try:
                commands[command_name](args)
            except Exception as e:
                print(f"Error executing {command_name}: {e}")
        else:
            print(f"{command_name}: command not found")


def main():
    """Main loop to run the CLI with command history and enhancements."""
    print("Welcome to the Python CLI. Type 'help' for a list of commands.")
    while True:
        try:
            command_input = input(f"{os.getcwd()}$ ").strip()
            if command_input:
                readline.add_history(command_input)
                execute_command(command_input)
        except KeyboardInterrupt:
            print("\nExiting CLI")
            break


if __name__ == "__main__":
    main()
