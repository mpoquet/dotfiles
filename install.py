#!/usr/bin/env nix-shell
#!nix-shell -i python3
"""Dotfiles installation script.

Usage:
  install.py [--no-interactive] [(--quiet | --debug)]
  install.py --version

Options:
  -h --help             Show this screen.
  -n --no-interactive   Prompt before overwrite.
  -q --quiet            Decrease verbosity.
  --debug               Increase verbosity.
"""
import docopt
import logging
import os
import sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    From https://stackoverflow.com/a/3041990.
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():
    args = docopt.docopt(__doc__)

    # Logging
    log_fmt = '%(levelname)s:%(message)s'
    log_level = logging.INFO
    if args["--quiet"] == True:
        log_level = logging.WARN
    elif args["--debug"] == True:
        log_level = logging.DEBUG
    logging.basicConfig(format=log_fmt, level=log_level)

    prompt_on_overwrite = not args['--no-interactive']

    install(prompt_on_overwrite)

def install(prompt_on_overwrite=False):
    m = dict()

    # Git
    m["gitconfig"] = "~/.gitconfig"
    m["cgvgrc"] = "~/.cgvgrc"

    for src, dst in m.items():
        install_link(src, dst, prompt_on_overwrite)

def install_link(src, dst, prompt_on_overwrite=False):
    dst = os.path.expanduser(dst)

    # Create destination directory if needed.
    dst_dir = os.path.dirname(dst)
    os.makedirs(dst_dir, exist_ok=True)

    # Prompt on overwrite if needed.
    logging.debug('{} exists? {}'.format(dst, os.path.lexists(dst)))
    if prompt_on_overwrite and os.path.lexists(dst):
        if not query_yes_no(f"Overwrite {dst}?", "no"):
            return

    if os.path.lexists(dst):
        logging.debug(f"Removing {dst}")
        os.unlink(dst)

    src = os.path.realpath(src)
    dst = os.path.realpath(dst)
    logging.info(f'{src} -> {dst}')

    logging.debug(f"Symlinking {src} -> {dst}")
    os.symlink(src, dst)

if __name__ == '__main__':
    main()
