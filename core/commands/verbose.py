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

DESCRIPTION = "Turn verbosity on/off."

def autocomplete(shell, line, text, state):
    return None

def help(shell):
    shell.print_plain("")
    shell.print_plain('Use "verbose on" to turn verbosity on.')
    shell.print_plain('Use "verbose off" to turn verbosity off.')
    shell.print_plain("")

def execute(shell, cmd):
    splitted = cmd.split()

    if len(splitted) > 1:
        sw = splitted[1].lower()
        if sw == "1" or sw == "true" or sw == "on":
            shell.verbose = True
            shell.print_info("Verbosity: %s" % ("on" if shell.verbose else "off"))
        if sw == "0" or sw == "false" or sw == "off":
            shell.verbose = False
            shell.print_info("Verbosity: %s" % ("on" if shell.verbose else "off"))
    else:
        help(shell)
