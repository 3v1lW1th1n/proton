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

DESCRIPTION = "Show current module options."

def autocomplete(shell, line, text, state):
    return None

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "options -a" for advanced options.')
    shell.print_plain("")

def execute(shell, cmd):
    env = shell.plugins[shell.state]

    # dynamically set format length
    maxlen = 0
    for option in env.options.options:
        if option.advanced and " -a" not in cmd:
            continue

        if option.hidden:
            continue

        if len(option.name) > maxlen: maxlen = len(option.name)

    formats = '    {{0:<{0}}}{{1:<20}}{{2:<8}}{{3:<16}}'.format(maxlen+3)

    shell.print_plain("")
    shell.print_plain(formats.format("NAME", "VALUE", "REQ", "DESCRIPTION"))
    shell.print_plain(formats.format("----","-----", "---", "-----------"))

    for option in env.options.options:
        if option.advanced and " -a" not in cmd:
            continue

        if option.hidden:
            continue

        prettybool = "yes" if option.required else "no"
        value = str(option.value)[0:16] + "..." if len(str(option.value)) > 16 else str(option.value)
        shell.print_plain(formats.format(option.name, value, prettybool, option.description))
        
    shell.print_plain("")
