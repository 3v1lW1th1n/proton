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

DESCRIPTION = "Unset a variable for the current module."

def autocomplete(shell, line, text, state):

    # todo, here we can provide some defaults for bools/enums? i.e. True/False
    if len(line.split()) > 2:
        return None

    env = shell.plugins[shell.state]
    options = [x.name + " " for x in env.options.options if x.name.upper().startswith(text.upper()) and not x.hidden]
    options += [x.alias + " " for x in env.options.options if x.alias.upper().startswith(text.upper()) and not x.hidden and x.alias]

    try:
        return options[state]
    except:
        return None

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "unset %s" to unset the value for the specified option.' % (shell.colors.colorize("OPTION", shell.colors.BOLD)))
    shell.print_plain("")

def execute(shell, cmd):
    env = shell.plugins[shell.state]

    splitted = cmd.split()
    if len(splitted) > 1:
        key = splitted[1].upper()

        value = env.options.get(key)
        if value != None:

            value = ""
            if not env.options.set(key, value):
                shell.print_error("Option is not found!")
                return

            shell.print_info("%s ==> %s" % (key, value))
        else:
            shell.print_error("Unrecognized option!")
            
    else:
        help(shell)
