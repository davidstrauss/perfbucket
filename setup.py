from distutils.core import setup
setup(name='perfbucket',
      version='0.1',
      author = 'David Strauss',
      author_email = 'david@davidstrauss.net',
      maintainer = 'David Strauss',
      maintainer_email = 'david@davidstrauss.net',
      url = 'http://github.com/davidstrauss/perfbucket',
      install_requires = ['pycassa', 'phpserialize'],
      packages=['perfbucket'],
      )
