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

DESCRIPTION = "Show repeating jobs information."

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "repeat %s" to display the set options of a repeating job.' % shell.colors.colorize("JOB_ID", [shell.colors.BOLD]))
    shell.print_info('Use "repeat -k %s" to kill a repeating job.' % shell.colors.colorize("JOB_ID", [shell.colors.BOLD]))
    shell.print_info('Use "repeat -K" to kill all repeating jobs.')
    shell.print_plain("")

def print_repeatjob(shell, id):
    if id in shell.repeatjobs:
        formats = "    {0:<15}{1:<15}"
        shell.print_plain("")
        shell.print_plain(formats.format("OPTION", "VALUE"))
        shell.print_plain(formats.format("-"*6, "-"*5))
        for o in shell.repeatjobs[id][6].options:
            if not o.hidden:
                shell.print_plain(formats.format(o.name, o.value))
        shell.print_plain("")
    else:
        shell.print_error("Repeating job '"+id+"' does not exist!")

def print_all_repeatjobs(shell):
    if not shell.repeatjobs:
        shell.print_error("No repeating jobs!")
        return

    formats = "    {0:<4}{1:<40}{2:<7}{3:<5}{4:<7}"

    shell.print_plain("")

    shell.print_plain(formats.format("ID", "NAME", "TTR", "CR", "TBR"))
    shell.print_plain(formats.format("-"*2, "-"*4, "-"*3, "-"*2, "-"*3))
    for rjob in shell.repeatjobs:
        rjobobj = shell.repeatjobs[rjob]
        shell.print_plain(formats.format(rjob, rjobobj[5], str(rjobobj[0]), str(rjobobj[1]-1), str(rjobobj[4])))

    shell.print_plain("")
    shell.print_plain('TTR = Time to repeat.')
    shell.print_plain('CR = Cycles remaining.')
    shell.print_plain('TBR = Time between requests.')
    shell.print_plain("")

def kill_repeatjob(shell, id):
    tmp = shell.repeatjobs
    if id in tmp:
        del tmp[id]
        shell.repeatjobs = tmp
        shell.print_good("Repeating job '"+id+"' has been deleted.")
    else:
        shell.print_error("Repeating job '"+id+"' does not exist.")

def killall_repeatjobs(shell):
    shell.repeatjobs = {}
    shell.print_good("All repeating jobs have been deleted.")

def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        id = splitted[-1]
        flag = splitted[1]
        if len(splitted) > 2:
            if flag == "-k":
                kill_repeatjob(shell, id)
                return
            else:
                shell.print_error("Unrecognized option!")
                return

        else:
            if flag == "-K":
                killall_repeatjobs(shell)
                return
            else:
                print_repeatjob(shell, id)
                return

    print_all_repeatjobs(shell)
