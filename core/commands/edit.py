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

DESCRIPTION = "Edit the current module."

def autocomplete(shell, line, text, state):
    return None

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "edit %s" to edit the current module\'s python file.' % (shell.colors.colorize("py/python", shell.colors.BOLD)))
    shell.print_info('Use "edit %s" to edit the current module\'s associated javascript file (if applicable).' % (shell.colors.colorize("js/javascript", shell.colors.BOLD)))
    shell.print_info('Use "edit %s" to edit the current module\'s associated vbscript file (if applicable).' % (shell.colors.colorize("vbs/vbscript", shell.colors.BOLD)))
    shell.print_plain("")

def execute(shell, cmd):
    import subprocess, os

    try:
        if not os.environ['EDITOR']:
            editor = 'vi'
        else:
            editor = os.environ['EDITOR']
    except KeyError:
        editor = 'vi'

    py_file = "modules/"+shell.state+".py"
    js_file = "data/"+shell.state+".js"
    vbs_file = "data/"+shell.state+".vbs"
    dropper_file = "data/"+shell.state+".dropper"

    splitted = cmd.split()

    if len(splitted) > 1:
        ftype = splitted[1].lower()
        if ftype == "py" or ftype == "python":
            file = py_file
        elif ftype == "js" or ftype == "javascript":
            file = js_file
        elif ftype == "vbs" or ftype == "vbscript":
            file = vbs_file
        elif ftype == "dropper":
            file = dropper_file
        else:
            return

        if os.path.isfile(file):
            editcmd = [editor, file]
        else:
            return
    else:
        editcmd = [editor, py_file]
    
    subprocess.call(editcmd)
    shell.run_command('load')
