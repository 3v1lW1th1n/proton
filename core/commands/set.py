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

import os

DESCRIPTION = "Set a variable for the current module."

def autocomplete(shell, line, text, state):

    env = shell.plugins[shell.state]
    if len(line.split()) > 1:
        optionname = line.split()[1]
        if optionname in [x.name for x in env.options.options if not x.hidden]:
            option = [x for x in env.options.options if x.name == optionname][0]
            options = []
            if option.boolean:
                options = [x for x in ['true', 'false'] if x.upper().startswith(text.upper())]
            if option.file:
                options = filepaths(text)
            if option.implant:
                pass
            if option.enum:
                options = [x for x in option.enum if x.upper().startswith(text.upper())]
            if options:
                return options[state]

    options = [x.name + " " for x in env.options.options if x.name.upper().startswith(text.upper()) and not x.hidden]
    options += [x.alias + " " for x in env.options.options if x.alias.upper().startswith(text.upper()) and not x.hidden and x.alias]

    try:
        return options[state]
    except:
        return None

def filepaths(text):
    import readline
    everything = readline.get_line_buffer()
    cursor_idx = readline.get_begidx()
    idx = 0
    for chunk in everything.split(" "):
        fullpath = chunk
        idx += len(chunk) + 1
        if idx > cursor_idx:
            break

    if os.path.isfile(fullpath):
        return None
    if "/" in fullpath:
        d = os.path.dirname(fullpath)
    else:
        d = "."

    res = []
    for candidate in os.listdir(d):
        if not candidate.startswith(text):
            continue
        if os.path.isdir(d+os.path.sep+candidate):
            res.append(candidate + os.path.sep)
        else:
            res.append(candidate + " ")
    return res

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "set %s" to set the value for the specified option.' % (shell.colors.colorize("OPTION VALUE", shell.colors.BOLD)))
    shell.print_plain("")

def execute(shell, cmd):
    env = shell.plugins[shell.state]

    splitted = cmd.split()
    if len(splitted) > 1:
        key = splitted[1].upper()

        value = env.options.get(key)
        if value != None:

            # if it's >2, we set the third argument
            if len(splitted) > 2:
                value = cmd.split(None, 2)[2]
                if not env.options.set(key, value):
                    shell.print_error("Invalid value!")
                    return

            shell.print_info("%s ==> %s" % (key, value))
        else:
            shell.print_error("Option is not found!")
    else:
        help(shell)
