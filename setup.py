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

from distutils.core import setup
setup(name='perfbucket',
      version='0.1',
      author = 'David Strauss',
      author_email = 'david@davidstrauss.net',
      maintainer = 'David Strauss',
      maintainer_email = 'david@davidstrauss.net',
      url = 'http://github.com/davidstrauss/perfbucket',
      install_requires = ['pycassa', 'phpserialize', 'pyinotify'],
      packages = ['perfbucket'],
      data_files = [('/etc/init.d', ['perfbucket-watcher'])],
      scripts = ['bin/perfbucket']
      )
