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

DESCRIPTION = "Switch to a different module."

def autocomplete(shell, line, text, state):
    import readline
    everything = readline.get_line_buffer()
    cursor_idx = readline.get_begidx()
    idx = 0
    for chunk in everything.split(" "):
        fulltext = chunk
        idx += len(chunk) + 1
        if idx > cursor_idx:
            break
    prefix, suffix = fulltext.rsplit("/",maxsplit=1) if "/" in fulltext else ("",fulltext)
    if prefix:
        prefix += "/"

    options = []
    tmp = list(shell.plugins.keys())
    for plugin in shell.plugins:
        tmp.append(plugin.split("/")[-1])
    for plugin in tmp:
        if not plugin.startswith(fulltext):
            continue
        chunk = plugin[len(prefix):]
        if "/" in chunk:
            options.append(chunk.split("/")[0]+"/")
        else:
            options.append(chunk+" ")
    options = list(sorted(set(options)))
    try:
        return options[state]
    except:
        return None

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "use %s" to switch to the specified module.' % (shell.colors.colorize("MODULE", shell.colors.BOLD)))
    shell.print_plain("")

def modules(shell, module):
    for i in shell.plugins:
        if module == i.split('/')[-1]:
            return 0
    return 1
    
def execute(shell, cmd):
    splitted = cmd.split()

    if len(splitted) > 1:
        module = splitted[1]
        if modules(shell, module):
            shell.print_error("Module is not found!")
            return
        if "/" not in module:
            module = [k for k in shell.plugins if k.lower().split('/')[-1] == module.lower()][0]
        shell.previous = shell.state
        shell.state = module
        
    else:
        help(shell)
