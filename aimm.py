import cli, sys
from cli import aimmApp

PROGRAM_NAME = "aimm"
WEBSITE = "https://aimodels.org"
API_SERVER = "https://ai-models-web-backend-nyotuddeyq-ue.a.run.app"
GITHUB_REPO = "visioninit/aimm"
VERSION = "0.5.0"


def init():
    for arg in sys.argv:
        if (' --version') in arg or (' -v') in arg:
            print(f"AIMM Version: {VERSION}")
            sys.exit(0)
        elif (' --licenses') in arg:
            if '--verbose' in sys.argv:
                aimmApp.show_licenses(verbose=True)
                sys.exit(0)
            else:
                aimmApp.show_licenses()
                sys.exit(0)
        elif (' --check-update') in arg:
            aimmApp.check_for_updates(GITHUB_REPO, VERSION)
            sys.exit(0)
    if len(sys.argv) == 1 or sys.argv[1] == "--help": # if no arguments are passed or if the first argument is "--help", print help
        aimmApp.show_help(PROGRAM_NAME)
    else:
        aimmApp.app()


# if this file is run directly, run init()
if __name__ == "__main__":
    init()
