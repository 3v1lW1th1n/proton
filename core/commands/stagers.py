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

DESCRIPTION = "Show stagers information."

def autocomplete(shell, line, text, state):
    pass

def help(shell):
    shell.print_plain("")
    shell.print_info('Use "stagers %s" to display a stager.' % shell.colors.colorize("STAGER_ID", [shell.colors.BOLD]))
    shell.print_info('Use "stagers -o %s" to print a stager\'s options.' % shell.colors.colorize("STAGER_ID", [shell.colors.BOLD]))
    shell.print_info('Use "stagers -k %s" to kill a stager.' % shell.colors.colorize("STAGER_ID", [shell.colors.BOLD]))
    shell.print_plain("")

def print_all_payloads(shell):
    if len(shell.stagers) == 0 or len([stager for keypair in [endpoint for port,endpoint in shell.stagers.items()] for endpoint, stager in keypair.items() if not stager.killed]) == 0:
        shell.print_error("No active stagers yet!")
        return

    shell.print_plain("")

    formats = "    {0:<4}{1:<16}{2:<6}{3:<10}{4:<20}"

    shell.print_plain(formats.format("ID", "IP", "PORT", "ENDPOINT", "TYPE"))
    shell.print_plain(formats.format("--", "--", "-"*4, "-"*8, "-"*4))

    for stager in sorted([stager for keypair in [endpoint for port,endpoint in shell.stagers.items()] for endpoint, stager in keypair.items() if not stager.killed], key=lambda s:s.payload.id):
        payload = stager.get_payload_data().decode()
        shell.print_plain(formats.format(stager.payload.id, stager.hostname, stager.port, stager.endpoint, stager.module))
        
    shell.print_plain("")

def print_payload(shell, id):
    for port in shell.stagers:
        for endpoint in shell.stagers[port]:
            stager = shell.stagers[port][endpoint]

            if str(stager.payload.id) == id and not stager.killed:
                payload = stager.get_payload_data().decode()
                shell.print_command(f"{payload}")
                return

    shell.print_error(f"Stager is not found!")

def print_listener_options(shell, id):
    for port in shell.stagers:
        for endpoint in shell.stagers[port]:
            stager = shell.stagers[port][endpoint]
            if str(stager.payload.id) != id:
                continue

            maxlen = 0
            for option in stager.options.options:
                if option.hidden:
                    continue

                if len(option.name) > maxlen: maxlen = len(option.name)

            formats = '    {{0:<{0}}}{{1:<20}}{{2:<8}}{{3:<16}}'.format(maxlen+3)

            shell.print_plain("")
            shell.print_plain(formats.format("NAME", "VALUE", "REQ", "DESCRIPTION"))
            shell.print_plain(formats.format("----","-----", "---", "-----------"))

            for option in stager.options.options:

                if option.hidden:
                    continue

                prettybool = "yes" if option.required else "no"
                value = str(option.value)[0:16] + "..." if len(str(option.value)) > 16 else str(option.value)
                shell.print_plain(formats.format(option.name, value, prettybool, option.description))

            shell.print_plain("")
            return

    shell.print_error(f"Stager is not found!")

def kill_listener(shell, id):
    import os
    for port in shell.stagers:
        for endpoint in shell.stagers[port]:
            stager = shell.stagers[port][endpoint]

            if str(stager.payload.id) == id and not stager.killed:
                sessions = [session for skey, session in shell.sessions.items() if int(session.stager.payload.id) == int(id) and not session.killed]
                if len(sessions) > 0:

                    shell.print_warning("Warning: This stager still has live zombies attached:")
                    shell.print_plain("   Zombie IDs: " + ", ".join([str(s.id) for s in sessions]))
                    shell.print_warning("If this stager dies, then they will die.")

                    try:
                        import readline
                        old_prompt = shell.prompt
                        old_clean_prompt = shell.clean_prompt
                        readline.set_completer(None)
                        shell.prompt = '\033[1;77m'+'[?]'+'\033[0m'+' Continue? (y/n): '
                        shell.clean_prompt = shell.prompt
                        option = shell.get_command(shell.prompt)

                        if shell.spool:
                            shell.spool_log(shell.prompt, option)

                        if option.lower() == 'y':
                            for session in sessions:
                                # they die anyways, they shouldn't have to suffer
                                session.kill()

                            stager.killed = True
                            del shell.stagers[port][endpoint]
                            if not shell.stagers[port]:
                                server = shell.servers[port]
                                server.http.shutdown()
                                server.http.socket.close()
                                server.http.server_close()
                                del shell.servers[port]
                                del shell.stagers[port]


                            shell.print_good("Stager %s: Killed!" % id)
                            return
                        else:
                            return

                    except KeyboardInterrupt:
                        shell.print_plain(shell.clean_prompt)
                        return
                    finally:
                        shell.prompt = old_prompt
                        shell.clean_prompt = old_clean_prompt

                else:
                    stager.killed = True
                    del shell.stagers[port][endpoint]
                    if not shell.stagers[port]:
                        server = shell.servers[port]
                        server.http.shutdown()
                        server.http.socket.close()
                        server.http.server_close()
                        del shell.servers[port]
                        del shell.stagers[port]

                    shell.print_good("Stager %s: Killed!" % id)
                    return

    shell.print_error("Stager is not found!")


def execute(shell, cmd):

    splitted = cmd.split()

    if len(splitted) > 1:
        id = splitted[-1]
        if len(splitted) > 2:
            flag = splitted[1]
            if flag == "-k":
                kill_listener(shell, id)
                return
            elif flag == "-o":
                print_listener_options(shell, id)
                return
            else:
                shell.print_error("Unrecognized option!")
                return
        else:
            print_payload(shell, id)
            return

    print_all_payloads(shell)
