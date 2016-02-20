from distutils.core import setup, Extension

setup(name="pledge", version="0.1",
      ext_modules=[Extension("pledge", ["pledge.c"])])
