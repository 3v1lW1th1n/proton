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

DESCRIPTION = "Write output to a file."

def autocomplete(shell, line, text, state):
    options = filepaths(text)
    return options[state]

def help(shell):
    shell.print_plain("")
    shell.print_plain('Use "spool on" to turn spooling on and spool to /tmp/proton.spool.')
    shell.print_plain('Use "spool %s" to turn spooling on and spool to the specified file.' % (shell.colors.colorize("FILEPATH", shell.colors.BOLD)))
    shell.print_plain('Use "spool off" to turn spooling off and save spool file.')
    shell.print_plain("")

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

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        option = splitted[1]
        if option == 'on':
            shell.spool = '/tmp/proton.spool'
            shell.spoolstatus = True
            shell.print_info("Spooling: %s" % ("on" if shell.spoolstatus else "off"))
            shell.print_status("Spooling to /tmp/proton.spool...")
        elif option == 'off':
            if shell.spool:
                shell.spoolstatus = False
                shell.print_status("Spooling: %s" % ("on" if shell.spoolstatus else "off"))
        else:
            shell.spool = option
            shell.spoolstatus = True
            shell.print_info("Spooling: %s" % ("on" if shell.spoolstatus else "off"))
            shell.print_status("Spooling to "+option+"...")
    else:
        help(shell)
