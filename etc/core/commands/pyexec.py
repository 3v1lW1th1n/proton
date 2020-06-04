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

DESCRIPTION = "Eval some python code."

def autocomplete(shell, line, text, state):
    return None

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "pyexec %s" to eval the specified python code.' % (shell.colors.colorize("CODE", shell.colors.BOLD)))
    shell.print_plain("")

def execute(shell, cmd):
	splitted = cmd.split()
	if len(splitted) > 1:
		code = " ".join(cmd.split(" ")[1:])
		w = os.environ['OLDPWD']
		os.chdir(w)
		
		exec(code)
		
		g = os.environ['HOME']
		os.chdir(g + "/proton")
	else:
		help(shell)
