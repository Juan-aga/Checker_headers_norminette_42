import os
import argparse
import subprocess
import shutil

class colors:
    fail = '\033[91m'
    ok = '\033[92m'
    purple = '\033[95m'
    cyan = '\033[96m'
    yellow = '\033[93m'
    reset = '\033[0m'

def headernorm(path: str = os.getcwd(), norminette:bool = False, headers:bool = False):
    """
    This function recives 3 optional parameters:
        - path (str):       Path to check, by default the current directory.
        - norm (bool):      Show full norminette information if True, by default is False.
        - headers (bool):   Show full users headers information if True, by default is False.
    """
    checked = {}
    users = set({})
    extensions = [".c", ".h"]
    ft_clear()
    ft_create_separator("Checking files")
    for files in ft_list_files(path, extensions):
        checked[files] = ft_check_header(files)
        checked = ft_check_norm(files, checked)
    users, checked, norm_errors, head_errors = ft_fill_users(users, checked)
    ft_check_report(len(checked), norm_errors, head_errors, path)
    if headers or head_errors:
        ft_headers_log(checked, headers)
    if norminette or norm_errors:
        ft_norm_log(checked, norminette)
    ft_headers_report(len(users), len(checked), head_errors, users)
    ft_norm_report(len(checked), norm_errors)

def ft_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-p",
            "--path",
            help="PATH to check, by default the current directory.",
            default = os.getcwd()
            )
    parser.add_argument(
            "-n",
            "--norm",
            help="show full norminette information.",
            action="store_true"
            )
    parser.add_argument(
            "-he",
            "--headers",
            help="Show full users headers information.",
            action="store_true"
            )
    return parser.parse_args()

def ft_clear():
    so = os.name
    if so == 'nt':
        cmd = "cls"
    else:
        cmd = "clear"
    subprocess.call(cmd, shell=True)

def ft_create_separator(msg):
    size = os.get_terminal_size()[0]
    separator = "-" * size
    string = f'|{colors.purple}{msg.center(size - 2)}{colors.cyan}|'
    separator = colors.cyan + separator + "\n" + string + "\n" + separator + colors.reset
    print(separator)

def ft_list_files(path, extensions):
    try:
        directory = os.listdir(path)
    except:
        print(f'{colors.fail}No valid path: {path}{colors.reset}')
        exit()
    for check in directory:
        files = os.path.join(path, check)
        if os.path.isdir(files):
            for new_file in ft_list_files(files, extensions):
                yield new_file
        elif os.path.isfile(files) and os.path.splitext(files)[1] in extensions:
            yield files
        else:
            continue

def ft_check_header(files):
    try:
        with open(files, 'r') as f:
            line = f.readlines()
            by = line[5].split()[2]
            created = line[7].split()[5]
            updated = line[8].split()[5]
        return {'By': by, 'Created': created, 'Updated': updated, 'Error': None}
    except:
        return {'Error': f"Error checking header in file: {files}"}

def ft_check_norm(files, checked):
    try:
        execute = f"norminette {files}"
        norminette = subprocess.run(execute, shell=True, capture_output=True, text=True)
        checked[files]['Norm'] = norminette
        checked[files]['Error norm'] = None
        return checked
    except:
        checked[files]['Error norm'] += f"Error checking norminette in file: {files}"
        checked[files]['Norm'] = None
        return checked

def ft_fill_users(users, checked):
    norm_errors = 0
    head_errors = 0
    for files, data in checked.items():
        if not data['Error']:
            users.add(data['By'])
            users.add(data['Created'])
            users.add(data['Updated'])
        else:
            head_errors += 1
        if data['Error norm'] or "Error" in data['Norm'].stdout:
            norm_errors += 1
    return users, checked, norm_errors, head_errors

def ft_check_report(files, norm_error, header_error, path):
    if not files:
        print(f'{colors.fail}No .h or .c files to check in {path}.{colors.reset}')
        exit()
    print(f'{colors.ok}Checked {files} files.{colors.reset}')
    if norm_error or header_error:
        if header_error:
            print(f'{colors.fail}{header_error} of {files} files failed to check headers.{colors.reset}')
        else:
            print(f'{colors.ok}Can check the headers of the {files} files.{colors.reset}')
        if norm_error:
            print(f'{colors.fail}{norm_error} of {files} files have error with the norm.{colors.reset}')
        else:
            print(f'{colors.ok}Norm ok in the {files} files.{color.reset}')

def ft_headers_report(len_users, len_checked, errors, users):
    ft_create_separator("Headers")
    if not len_users < 2:
        print(f'{colors.yellow}It is ok if it was created by a group of {len_users} users: {colors.ok}{", ".join(list(users))}{colors.reset}')
    elif len_users:
        print(f'{colors.ok}All the {len_checked} files was edited by: {"".join(list(users))}{colors.reset}')
    else:
        print(f'{colors.fail}No headers to check.{colors.reset}')

def ft_norm_report(len_checked, errors):
    ft_create_separator("Norminette")
    if not errors:
        print(f"{colors.ok}All the {len_checked} files are OK with norminette{colors.reset}")
    else:
        print(f'{colors.fail}Norminette errors in {errors} of {len_checked} files.{colors.reset}')

def ft_headers_log(checked, headers):
    ft_create_separator("Headers logs")
    for files, data in checked.items():
        if data['Error']:
            print(f"{colors.fail}{data['Error']}{colors.reset}")
        elif headers:
            if data['By'] == data['Created'] and data['By'] == data['Updated']:
                color = colors.ok
            else:
                color = colors.yellow
            print(f"{color}File: {files}\tBy: {data['By']}, Created: {data['Created']}, Updated: {data['Updated']}{colors.reset}")

def ft_norm_log(checked, norm):
    ft_create_separator("Norminette logs:")
    for files, data in checked.items():
        if not data['Norm']:
            print(f"{colors.fail}{data['Error norm']}{colors.reset}")
        elif "Error" in data['Norm'].stdout:
            if not "!" in data['Norm'].stdout:
                print(f'{colors.fail}{files}{colors.reset}')
            print(f"{colors.fail}{data['Norm'].stdout}{colors.reset}")
        elif norm:
            print(f"{colors.ok}{data['Norm'].stdout}{colors.reset}")

if __name__ == "__main__":
    args = ft_parser()
    headernorm(args.path, args.norm, args.headers)
