#!/usr/bin/env python3

# Copyright (C) 2016 Sylvia van Os <iamsylvie@openmailbox.org>
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

import shlex

from os import access, environ, listdir, pathsep, X_OK
from os.path import isfile, join
from subprocess import Popen

from pext_base import ModuleBase
from pext_helpers import Action


class Module(ModuleBase):
    def init(self, settings, q):
        self.q = q

        self._get_entries()

    def _get_entries(self):
        executables = []

        for path in environ['PATH'].split(pathsep):
            for executable in listdir(path):
                fullname = join(path, executable)
                if isfile(fullname) and access(fullname, X_OK):
                    executables.append(executable)

        self.q.put([Action.replace_command_list, sorted(executables)])
        self.q.put([Action.replace_entry_list, sorted(executables)])

    def stop(self):
        pass

    def selection_made(self, selection):
        if len(selection) == 1:
            Popen(shlex.split(selection[0]["value"]))
            self.q.put([Action.close])

    def process_response(self, response):
        pass
