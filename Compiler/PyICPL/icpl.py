from sys import argv
from os import system
from api import error

def command_help(arguments : list):
    print("- help\n- run [path]")

def command_run(arguments : list):
    if len(arguments) > 1:
        error("Too many values to unpack", "command", f"expected 1 got {len(arguments)}")
    elif arguments[0][-4:] != ".cpl":
        error("Your path must include the file and the extension", "command", ".cpl")
    system(f"python3 CPLinterpreter.py {arguments[0]}")

if __name__ == "__main__":
    if len(argv) == 1:
        error("You must specify a command", "command", "please follow this link : https://github.com/Bugxit/CPL-Development")
    if argv[1] not in ["help", "run"]:
        error("Command does not exist", "command", "please follow this link : https://github.com/Bugxit/CPL-Development")
    globals()["command_"+argv[1]](argv[2:])