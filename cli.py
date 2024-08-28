import os
import shutil
import sys

def list_directory(args):
    """List the contents of the directory."""
    path = '.' if not args else args[0]
    show_all = '-a' in args
    long_format = '-l' in args
    ignore_hidden = '-I' in args

    try:
        files = os.listdir(path)
        if ignore_hidden:
            files = [f for f in files if not f.startswith('.')]
        if not show_all:
            files = [f for f in files if not f.startswith('.')]
        if long_format:
            for file in files:
                print(f"{file} - {os.stat(file)}")
        else:
            print(' '.join(files))
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory")

def change_directory(args):
    """Change the current working directory."""
    if not args:
        print("cd: missing operand")
        return
    path = args[0]
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")

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
    with open(args[0], 'w') as f:
        pass

def read_file(args):
    """Display the content of a file."""
    if not args:
        print("cat: missing operand")
        return
    try:
        with open(args[0], 'r') as f:
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

def main():
    """Main loop to run the CLI."""
    commands = {
        'ls': list_directory,
        'cd': change_directory,
        'pwd': print_working_directory,
        'mkdir': make_directory,
        'rmdir': remove_directory,
        'rm': remove_file,
        'touch': create_file,
        'cat': read_file,
        'cp': copy_file,
        'mv': move_file,
    }

    while True:
        try:
            command_input = input(f"{os.getcwd()}$ ").strip().split()
            if not command_input:
                continue

            command, *args = command_input
            if command == 'exit':
                break
            if command in commands:
                commands[command](args)
            else:
                print(f"{command}: command not found")
        except KeyboardInterrupt:
            print("\nExiting CLI")
            break

if __name__ == "__main__":
    main()
