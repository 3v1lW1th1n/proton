#!/usr/bin/env python3

#            ---------------------------------------------------
#                             Proton Framework              
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

DESCRIPTION = "Show help information."

def autocomplete(shell, line, text, state):

    # should never go this big...
    if len(line.split()) > 2:
        return None

    options = [x + " " for x in shell.actions if x.startswith(text)]

    try:
        return options[state]
    except:
        return None


def help(shell):
    shell.print_plain("")
    shell.print_info('Use "help %s" to find more info about a command.' %
                      shell.colors.colorize("COMMAND", [shell.colors.BOLD]))
    shell.print_plain("")

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) == 1:
        return help_all(shell)

    if len(splitted) > 1:
        return help_command(shell, splitted[1])


def help_command(shell, command):
    command = command
    if command not in shell.actions:
        shell.print_error("Unrecognized command!")
        return

    shell.actions[command].help(shell)


def help_all(shell):
    formats = '    {0:<12}{1:<16}'

    shell.print_plain("")
    shell.print_plain(formats.format("COMMAND", "DESCRIPTION"))
    shell.print_plain(formats.format("-------", "-----------"))

    for key, env in sorted(shell.actions.items()):
        if getattr(env, "hidden_command", False):
            continue
        shell.print_plain(formats.format(key, env.DESCRIPTION))

    shell.print_plain("")
    shell.print_info('Use "help %s" to find more info about a command.' %
                      shell.colors.colorize("COMMAND", [shell.colors.BOLD]))
    shell.print_plain("")
