from functions.get_files_info import get_files_info


def print_call(working_dir, directory, label):
    # Show the exact call
    print(f'get_files_info("{working_dir}", "{directory}"):')
    print(f"Result for {label}:")

    result = get_files_info(working_dir, directory)

    if result.startswith("Error:"):
        # Error lines must be indented with 4 spaces
        print(f"    {result}")
    else:
        # Successful listings: indent each returned line with 2 spaces
        indented = "  " + result.replace("\n", "\n  ")
        print(indented)

    print()  # blank line between sections


if __name__ == "__main__":
    print_call("calculator", ".", "current directory")
    print_call("calculator", "pkg", "'pkg' directory")
    print_call("calculator", "/bin", "'/bin' directory")
    print_call("calculator", "../", "'../' directory")
