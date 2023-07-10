import os
import subprocess
import shutil

def installer_headernorm():
    file = "headers.py"
    shell_rc = None
    alias = "headernorm"
    src_dir = os.path.dirname(os.path.abspath(__file__))
    dst_dir = os.path.expanduser("~/headernorm")
    if not os.path.exists(dst_dir):
        try:
            os.makedirs(dst_dir)
        except:
            print(f'\033[91mFailed to create directory {dst_dir}\033[0m')
            exit()
    src_file = os.path.join(src_dir, file)
    dst_file = os.path.join(dst_dir,file)
    try:
        shutil.copyfile(src_file, dst_file)
    except:
        print(f'\033[91mFailed to copy file {file}\033[0m')
        exit()
    shell = os.environ.get("SHELL", "")
    if "bash" in shell:
        shell_rc = "~/.bashrc"
    elif "zsh" in shell:
        shell_rc = "~/.zshrc"
    else:
        print(f'\033[91mNo alias created.\033[0m')
        exit()
    if ft_check_alias(shell_rc, alias):
        print(f'\033[91mAlias {alias} is in use.\033[0m')
        exit()
    else:
        subprocess.call(f"echo 'alias {alias}=\"python3 {dst_file}\"' >> {shell_rc}", shell=True)
        print(f"\033[92mInstalled. Now you can use it with \"{alias}\"\n\033[93mRemember you have to run: \"source {shell_rc}\033[0m")

def ft_check_alias(file, alias):
    try:
        with open(os.path.expanduser(file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if f'alias {alias}' in line:
                    return True
        return False
    except:
        print(f'\033[91mFailed to read file {file}\033[0m')
        exit()

if __name__ == "__main__":
    installer_headernorm()
