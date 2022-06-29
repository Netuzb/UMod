"""Initial entrypoint"""

import sys
import getpass
import os

if getpass.getuser() == "root" and "--root" not in " ".join(sys.argv):
    print("!" * 30)
    print("NEVER EVER RUN USERBOT FROM ROOT")
    print("THIS IS THE THREAD FOR NOT ONLY YOUR DATA, ")
    print("BUT ALSO FOR YOUR DEVICE ITSELF!")
    print("!" * 30)
    print()
    print("TYPE force_insecure TO IGNORE THIS WARNING")
    print("TYPE ANYTHING ELSE TO EXIT:")
    if input("> ").lower() != "force_insecure":
        sys.exit(1)

if sys.version_info < (3, 8, 0):
    print("Error: you must use at least Python version 3.8.0")  # pragma: no cover
elif __package__ != "friendly-telegram":  # In case they did python __main__.py
    print(
        "Error: you cannot run this as a script; you must execute as a package"
    )  # pragma: no cover
else:
    from . import log

    log.init()
    try:
        from . import main
    except ModuleNotFoundError:  # pragma: no cover
        print(
            "Error: you have not installed all dependencies correctly.\n"
            "Attempting dependencies installation... Just wait."
        )

        os.popen("pip3 install -r requirements.txt").read()  # skipcq: BAN-B605, BAN-B607

        try:
            from . import main
        except ModuleNotFoundError:
            print(
                "Error while installing dependencies. Please, do this manually!\n"
                "pip3 install -r requirements.txt"
            )

            sys.exit(1)

    if __name__ == "__main__":
        main.main()  # Execute main function
