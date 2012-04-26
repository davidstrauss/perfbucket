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

import storage
import uuid
import phpserialize
import sys

def get_xhprof_data(request_uuid):
    details = storage.get_profiling_details(request_uuid)
    return phpserialize.dumps(details["data"])

if __name__ == '__main__':
    print(get_xhprof_data(uuid.UUID(sys.argv[1])))
