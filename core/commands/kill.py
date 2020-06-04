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

DESCRIPTION = "Kill a zombie or all zombies."

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "kill %s" to kill the specified zombie.' % (shell.colors.colorize("ZOMBIE_ID", shell.colors.BOLD)))
    shell.print_info('Use "kill all" to kill all active zombies.')
    shell.print_info('Use "kill dead" to kill all dead zombies.')
    shell.print_plain("")

def kill_zombie(shell, id):
    formats = "    {0:<5}{1:<10}{2:<20}{3:<40}"

    if not id.isdigit() and id.lower() not in ["all", "dead"]:
        shell.print_error("Not a valid argument to kill: %s!" % id)
        return

    if id.lower() == "all":
        [session.kill() for skey, session in shell.sessions.items() if session.killed == False]

    elif id.lower() == "dead":
        [session.kill() for skey, session in shell.sessions.items() if session.status == 0 and session.killed == False]

    else:
        [session.kill() for skey, session in shell.sessions.items() if session.id == int(id) and session.killed == False]

    if id.lower() == "all":
        shell.print_good("All Zombies Killed!")
    elif id.lower() == "dead":
        shell.print_good("Dead Zombies Killed!")

    shell.play_sound('KILL')

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        id = splitted[1]
        kill_zombie(shell, id)
        return

    help(shell)
