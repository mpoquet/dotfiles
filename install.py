#!/usr/bin/env nix-shell
#!nix-shell -i python3
"""Dotfiles installation script.

Usage:
  install.py [--no-interactive] [(--quiet | --debug)]
  install.py --version

Options:
  -h --help             Show this screen.
  -n --no-interactive   Do NOT prompt before overwrite.
  -q --quiet            Decrease verbosity.
  --debug               Increase verbosity.
"""
import docopt
import logging
import os
import sys
from shutil import copyfile

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
    # Links
    m = dict()
    m["cgvgrc"] = "~/.cgvgrc"
    m["gitconfig"] = "~/.gitconfig"
    m["hexchat-colors.conf"] = "~/.config/hexchat/colors.conf"
    m["i3/config"] = "~/.config/i3/config"
    m["i3/i3status.conf"] = "~/.config/i3/i3status.conf"
    m["kitty/keymap.conf"] = "~/.config/kitty/keymap.conf"
    m["kitty/kitty.conf"] = "~/.config/kitty/kitty.conf"
    m["kitty/theme-dark.conf"] = "~/.config/kitty/theme-dark.conf"
    m["kitty/theme-light.conf"] = "~/.config/kitty/theme-light.conf"
    m["starship.toml"] = "~/.config/starship.toml"
    m["subl-preferences.json"] = "~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings"
    m["taskopenrc"] = "~/.taskopenrc"
    m["taskrc"] = "~/.taskrc"
    m["user-dirs.dirs"] = "~/.config/user-dirs.dirs"
    m["vimrc"] = "~/.vimrc"
    m["vimrc-bepo"] = "~/.vim/bepo-mapping"

    for src, dst in m.items():
        install_link(src, dst, prompt_on_overwrite)

    # Copies
    m = dict()
    m["llpp.conf"] = "~/.config/llpp.conf"

    for src, dst in m.items():
        install_link(src, dst, prompt_on_overwrite, True)

def install_link(src, dst, prompt_on_overwrite=False, copy=False):
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

    if copy:
        logging.debug(f"Copying {src} -> {dst}")
        copyfile(src, dst)
    else:
        logging.debug(f"Symlinking {src} -> {dst}")
        os.symlink(src, dst)

if __name__ == '__main__':
    main()
