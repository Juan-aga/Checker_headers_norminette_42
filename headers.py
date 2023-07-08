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

def main():
    args = ft_parser()
    checked = {}
    global extensions
    users = set({})
    extensions = [".c", ".h"]
    norm_errors = 0
    for files in ft_list_files(args.path):
        checked[files] = ft_check_header(files)
        checked = ft_check_norm(files, checked)

    for files, data in checked.items():
        if not data['Error']:
            users.add(data['By'])
            users.add(data['Created'])
            users.add(data['Updated'])
            norm_errors += data['Norm'].returncode
            if args.headers:
                if data['By'] == data['Created'] and data['By'] == data['Updated']:
                    color = colors.ok
                else:
                    color = colors.yellow
                print(f"{color}File: {files}\tBy: {data['By']}, Created: {data['Created']}, Updated: {data['Updated']}{colors.reset}")
#            if data['Norm'].returncode:
#                for norm in data['Norm'].stdout.split("\n")[1:]:
#                    print(norm)
        else:
            print(f"{colors.fail}{data['Error']}{colors.reset}")
#            if data['Norm']:
#                print(data['Norm'].stdout)
        if args.norm:
            print(data['Norm'].stdout)
    if not len(users) < 2:
        print(f'{colors.yellow}Users: {len(users)}{colors.reset}')
    elif len(users):
        print(f'{colors.ok}All files were edited by: {"".join(list(users))}{colors.reset}')
    if not norm_errors and len(users):
        print(f"{colors.ok}Norminette OK{colors.reset}")
    elif not args.norm:
        for files, data in checked.items():
#            if data['Norm'].returncode:
            if "Error" in data['Norm'].stdout:
                if not "!" in data['Norm'].stdout:
                    print(f'{colors.fail}{files}{colors.reset}')
                print(f"{colors.fail}{data['Norm'].stdout}{colors.reset}")

    print(f'{colors.cyan}',"*" * os.get_terminal_size()[0],f'{colors.reset}')
    print("Checked:", len(checked))

def ft_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        help="Path to check, by default the current directory.",
        default = os.getcwd()
        )
    parser.add_argument(
        "-n",
        "--norm",
        help="show full norminette information.",
        action="store_true"
        )
    parser.add_argument(
        "-c",
        "--headers",
        help="Show full users headers information.",
        action="store_true"
        )
    return parser.parse_args()

def ft_list_files(path):
    directory = os.listdir(path)
    for check in directory:
        files = os.path.join(path, check)
        if os.path.isdir(files):
            for new_file in ft_list_files(files):
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
#    print("check norm file:", files)
    try:
        execute = f"norminette {files}"
        norminette = subprocess.run(execute, shell=True, capture_output=True, text=True)
        checked[files]['Norm'] = norminette
        return checked
    except:
#        print("Failed norm in file:", files)
#       return {'Error': "Norm"}
        checked[files]['Error'] += f"Error checking norminette in file: {files}"
        checked[files]['Norm'] = None
        return checked
#    else:
#        return None

if __name__ == "__main__":
    main()