#!/usr/bin/env python3

# Copyright (C) 2016 - 2017 Sylvia van Os <sylvia@hackerchick.me>
#
# Pext launcher module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import html
import shlex

from os import access, environ, listdir, pathsep, X_OK
from os.path import expanduser, isfile, join
from subprocess import Popen

from pext_base import ModuleBase
from pext_helpers import Action


class Module(ModuleBase):
    def init(self, settings, q):
        self.executables = []
        self.info_panels = {}
        self.context_menus = {}

        self.settings = settings
        self.q = q

        self._get_entries()

    def _get_entries(self):
        for path in environ['PATH'].split(pathsep):
            path = expanduser(path)
            try:
                for executable in listdir(path):
                    fullname = join(path, executable)
                    if isfile(fullname) and access(fullname, X_OK):
                        if not executable in self.executables:
                            self.executables.append(executable)
                            self.info_panels[executable] = "<b>{}</b>".format(html.escape(fullname))
                            self.context_menus[executable] = [fullname]
                        else:
                            self.info_panels[executable] += "<br/>{}".format(html.escape(fullname))
                            self.context_menus[executable].append(fullname)

            except OSError:
                pass

        self.executables.sort()
        self._set_entries()

    def _set_entries(self):
        self.q.put([Action.replace_command_list, self.executables])
        self.q.put([Action.replace_command_info_dict, self.info_panels])
        self.q.put([Action.replace_command_context_dict, self.context_menus])

    def stop(self):
        pass

    def selection_made(self, selection):
        if len(selection) == 0:
            self._set_entries()
        elif len(selection) == 1:
            command = shlex.split(selection[0]["value"])
            if self.settings['_api_version'] >= [0, 4, 0]:
                if selection[0]['context_option']:
                    command[0] = selection[0]['context_option']

            Popen(command)
            self.q.put([Action.close])

    def process_response(self, response):
        pass
