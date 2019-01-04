from __future__ import print_function
import os
import sys
import subprocess
try:                                        # Older Pythons lack this
    import urllib.request                   # We'll let them reach the Python
    from importlib.util import find_spec    # check anyway
except ImportError:
    pass
import platform
import webbrowser
import hashlib
import argparse
import shutil
import stat
import time
try:
    import pip
except ImportError:
    pip = None

REQS_DIR = "lib"
sys.path.insert(0, REQS_DIR)
REQS_TXT = "requirements.txt"

INTRO = ("==========================\n"
         "    PieBot - Launcher    \n"
         "==========================\n")

IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_64BIT = platform.machine().endswith("64")
INTERACTIVE_MODE = not len(sys.argv) > 1  # CLI flags = non-interactive
PYTHON_OK = sys.version_info >= (3, 5)

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="PieBot's launcher")
    parser.add_argument("--start", "-s",
                        help="Starts the bot",
                        action="store_true")
    parser.add_argument("--auto-restart",
                        help="Autorestarts the bot in case of issues",
                        action="store_true")
    parser.add_argument("--update-bot",
                        help="Updates bot (git)",
                        action="store_true")
    parser.add_argument("--update-reqs",
                        help="Updates requirements",
                        action="store_true")
    parser.add_argument("--repair",
                        help="Issues a git reset --hard",
                        action="store_true")
    return parser.parse_args()


def install_reqs():
    remove_reqs_readonly()
    interpreter = sys.executable

    if interpreter is None:
        print("Python interpreter not found.")
        return

    txt = REQS_TXT

    args = [
        interpreter, "-m",
        "pip", "install",
        "--upgrade",
        "--target", REQS_DIR,
        "-r", txt
    ]

    if IS_MAC: # --target is a problem on Homebrew. See PR #552
        args.remove("--target")
        args.remove(REQS_DIR)

    code = subprocess.call(args)

    if code == 0:
        print("\nRequirements setup completed.")
    else:
        print("\nAn error occurred and the requirements setup might "
              "not be completed. Consult the docs.\n")


def update_pip():
    interpreter = sys.executable

    if interpreter is None:
        print("Python interpreter not found.")
        return

    args = [
        interpreter, "-m",
        "pip", "install",
        "--upgrade", "pip"
    ]

    code = subprocess.call(args)

    if code == 0:
        print("\nPip has been updated.")
    else:
        print("\nAn error occurred and pip might not have been updated.")


def update_bot():
    try:
        code = subprocess.call(("git", "pull", "--ff-only"))
    except FileNotFoundError:
        print("\nError: Git not found. It's either not installed or not in "
              "the PATH environment variable like requested in the guide.")
        return
    if code == 0:
        print("\nPieBot has been updated")
    else:
        print("\nThe bot was unable to update properly. If this is caused by edits "
              "you have made to the code you can try the repair option from "
              "the Maintenance submenu")


def reset_bot(reqs=False, data=False, cogs=False, git_reset=False):
    if reqs:
        try:
            shutil.rmtree(REQS_DIR, onerror=remove_readonly)
            print("Installed local packages have been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove installed "
                  "requirements: {}".format(e))
    if data:
        try:
            shutil.rmtree("data", onerror=remove_readonly)
            print("'data' folder has been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove the 'data' folder: "
                  "{}".format(e))

    if cogs:
        try:
            shutil.rmtree("cogs", onerror=remove_readonly)
            print("'cogs' folder has been wiped.")
        except FileNotFoundError:
            pass
        except Exception as e:
            print("An error occurred when trying to remove the 'cogs' folder: "
                  "{}".format(e))

    if git_reset:
        code = subprocess.call(("git", "reset", "--hard"))
        if code == 0:
            print("Bot has been restored to the last local commit.")
        else:
            print("The repair has failed.")

def verify_requirements():
    sys.path_importer_cache = {} # I don't know if the cache reset has any side effect.
    basic = find_spec("discord") # Without it, the lib folder wouldn't be seen if it
    if not basic:                # didn't exist when the launcher was started
        return None
    else:
        return True


def is_git_installed():
    try:
        subprocess.call(["git", "--version"], stdout=subprocess.DEVNULL,
                                              stdin =subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    else:
        return True


def requirements_menu():
    clear_screen()
    while True:
        print(INTRO)
        print("Main requirements:\n")
        print("1. Install basic requirements")
        print("\n0. Go back")
        choice = user_choice()
        if choice == "1":
            install_reqs()
        elif choice == "0":
            break
        clear_screen()


def update_menu():
    clear_screen()
    while True:
        print(INTRO)
        reqs = verify_requirements()
        if reqs is None:
            status = "No requirements installed"
        elif reqs is False:
            status = "Basic requirements installed"
        print("Status: " + status + "\n")
        print("Update:\n")
        print("1. Update bot + requirements (recommended)")
        print("2. Update bot")
        print("3. Update requirements")
        print("4. Update pip (might require admin privileges)")
        print("\n0. Go back")
        choice = user_choice()
        if choice == "1":
            update_bot()
            print("Updating requirements...")
            reqs = verify_requirements()
            if reqs is not None:
                install_reqs()
            else:
                print("The requirements haven't been installed yet.")
            wait()
        elif choice == "2":
            update_bot()
            wait()
        elif choice == "3":
            reqs = verify_requirements()
            if reqs is not None:
                install_reqs()
            else:
                print("The requirements haven't been installed yet.")
            wait()
        elif choice == "4":
            update_pip()
            wait()
        elif choice == "0":
            break
        clear_screen()


def maintenance_menu():
    clear_screen()
    while True:
        print(INTRO)
        print("Maintenance:\n")
        print("1. Repair bot (discards code changes, keeps data intact)")
        print("2. Wipe 'data' folder (all settings, cogs' data...)")
        print("3. Wipe 'lib' folder (all local requirements / local installed"
              " python packages)")
        print("4. Factory reset")
        print("\n0. Go back")
        choice = user_choice()
        if choice == "1":
            print("Any code modification you have made will be lost. Data/"
                  "non-default cogs will be left intact. Are you sure?")
            if user_pick_yes_no():
                reset_bot(git_reset=True)
                wait()
        elif choice == "2":
            print("Are you sure? This will wipe the 'data' folder, which "
                  "contains all your settings and cogs' data.\nThe 'cogs' "
                  "folder, however, will be left intact.")
            if user_pick_yes_no():
                reset_bot(data=True)
                wait()
        elif choice == "3":
            reset_bot(reqs=True)
            wait()
        elif choice == "4":
            print("Are you sure? This will wipe ALL installations. "
                  "data.\nYou'll lose all your settings, cogs and any "
                  "modification you have made.\nThere is no going back.")
            if user_pick_yes_no():
                reset_bot(reqs=True, data=True, cogs=True, git_reset=True)
                wait()
        elif choice == "0":
            break
        clear_screen()


def run_bot(autorestart):
    interpreter = sys.executable

    if interpreter is None: # This should never happen
        raise RuntimeError("Couldn't find Python's interpreter")

    if verify_requirements() is None:
        print("You don't have the requirements to start the bot. "
              "Install them from the launcher.")
        if not INTERACTIVE_MODE:
            exit(1)

    cmd = (interpreter, "bot.py")

    while True:
        try:
            code = subprocess.call(cmd)
        except KeyboardInterrupt:
            code = 0
            break
        else:
            if code == 0:
                break
            elif code == 26:
                print("Restarting bot...")
                continue
            else:
                if not autorestart:
                    break

    print("Process has been terminated. Exit code: %d" % code)

    if INTERACTIVE_MODE:
        wait()


def clear_screen():
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")


def wait():
    if INTERACTIVE_MODE:
        input("Press enter to continue.")


def user_choice():
    return input("> ").lower().strip()


def user_pick_yes_no():
    choice = None
    yes = ("yes", "y")
    no = ("no", "n")
    while choice not in yes and choice not in no:
        choice = input("Yes/No > ").lower().strip()
    return choice in yes


def remove_readonly(func, path, excinfo):
    os.chmod(path, 0o755)
    func(path)


def remove_reqs_readonly():
    """Workaround for issue #569"""
    if not os.path.isdir(REQS_DIR):
        return
    os.chmod(REQS_DIR, 0o755)
    for root, dirs, files in os.walk(REQS_DIR):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o755)


def calculate_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def create_fast_start_scripts():
    """Creates scripts for fast boot without going
    through the launcher"""
    interpreter = sys.executable
    if not interpreter:
        return

    call = "\"{}\" launcher.py".format(interpreter)
    start_bot = "{} --start".format(call)
    start_bot_autorestart = "{} --start --auto-restart".format(call)
    modified = False

    if IS_WINDOWS:
        ccd = "pushd %~dp0\n"
        pause = "\npause"
        ext = ".bat"
    else:
        ccd = 'cd "$(dirname "$0")"\n'
        pause = "\nread -rsp $'Press enter to continue...\\n'"
        if not IS_MAC:
            ext = ".sh"
        else:
            ext = ".command"

    start_bot             = ccd + start_bot             + pause
    start_bot_autorestart = ccd + start_bot_autorestart + pause

    files = {
        "start_bot"             + ext : start_bot,
        "start_bot_autorestart" + ext : start_bot_autorestart
    }

    if not IS_WINDOWS:
        files["start_launcher" + ext] = ccd + call

    for filename, content in files.items():
        if not os.path.isfile(filename):
            print("Creating {}... (fast start scripts)".format(filename))
            modified = True
            with open(filename, "w") as f:
                f.write(content)

    if not IS_WINDOWS and modified: # Let's make them executable on Unix
        for script in files:
            st = os.stat(script)
            os.chmod(script, st.st_mode | stat.S_IEXEC)


def main():
    print("Verifying git installation...")
    has_git = is_git_installed()
    is_git_installation = os.path.isdir(".git")
    if IS_WINDOWS:
        os.system("TITLE PieBot - Launcher")
    clear_screen()

    try:
        create_fast_start_scripts()
    except Exception as e:
        print("Failed making fast start scripts: {}\n".format(e))

    while True:
        print(INTRO)

        if not is_git_installation:
            print("WARNING: It doesn't look like the bot has been "
                  "installed with git.\nThis means that you won't "
                  "be able to update and some features won't be working.\n"
                  "A reinstallation is recommended. Follow the guide "
                  "properly this time.")

        if not has_git:
            print("WARNING: Git not found. This means that it's either not "
                  "installed or not in the PATH environment variable like "
                  "requested in the guide.\n")

        print("1. Run bot /w autorestart in case of issues")
        print("2. Run bot")
        print("3. Update")
        print("4. Install requirements")
        print("5. Maintenance (repair, reset...)")
        print("\n0. Quit")
        choice = user_choice()
        if choice == "1":
            run_bot(autorestart=True)
        elif choice == "2":
            run_bot(autorestart=False)
        elif choice == "3":
            update_menu()
        elif choice == "4":
            requirements_menu()
        elif choice == "5":
            maintenance_menu()
        elif choice == "0":
            break
        clear_screen()

args = parse_cli_arguments()

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    # Sets current directory to the script's
    os.chdir(dirname)
    if not PYTHON_OK:
        print("Python 3.5 or superior is needed. Install the required "
              "version.\nPress enter to continue.")
        if INTERACTIVE_MODE:
            wait()
        exit(1)
    if pip is None:
        print("The bot cannot work without the pip module. Please make sure to "
              "install Python without unchecking any option during the setup")
        wait()
        exit(1)
    if args.repair:
        reset_bot(git_reset=True)
    if args.update_bot:
        update_bot()
    if args.update_reqs:
        install_reqs()
    if INTERACTIVE_MODE:
        main()
    elif args.start:
        print("Starting PieBot...")
        run_bot(autorestart=args.auto_restart)
