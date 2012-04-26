# This file is part of perfbucket.
#
# perfbucket is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# perfbucket is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with perfbucket.  If not, see <http://www.gnu.org/licenses/>.

import phpserialize
import json
import storage

import sys
import pprint

def analyze_profiling_result(base_name):
    data = None
    with open(base_name + ".xhprof_testing") as f:
        data = phpserialize.load(f)

    metadata = None
    with open(base_name + ".json") as f:
        metadata = json.load(f)

    storage.save_profiling_result(data, metadata)

    pprint.pprint(data)
    pprint.pprint(metadata)

if __name__ == '__main__':
    analyze_profiling_result(sys.argv[1])
