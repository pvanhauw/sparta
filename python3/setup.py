#!/usr/local/bin/python

# copy SPARTA src/libsparta.so and sparta.py to system dirs

import sys
import io
import os
import re
from distutils.core import setup, Extension
# from loguru import logger as log

instructions = """
Syntax: python install.py [-h] [libdir] [pydir]
        libdir = target dir for src/libsparta.so, default = /usr/local/lib
        pydir = target dir for sparta.py, default = Python site-packages dir
"""



# if (len(sys.argv) > 1 and sys.argv[1] == "-h") or len(sys.argv) > 3:
#     print(instructions)
#     sys.exit()

# if len(sys.argv) >= 2:
#     libdir = sys.argv[1]
# else:
#     libdir = "/usr/local/lib"

# if len(sys.argv) == 3:
#     pydir = sys.argv[2]
# else:
#     pydir = ""

# # copy C lib to libdir if it exists
# # warn if not in LD_LIBRARY_PATH or LD_LIBRARY_PATH is undefined

# if not os.path.isdir(libdir):
#     print("ERROR: libdir %s does not exist" % libdir)
#     sys.exit()

# if "LD_LIBRARY_PATH" not in os.environ:
#     print("WARNING: LD_LIBRARY_PATH undefined, cannot check libdir %s" % libdir)
# else:
#     libpaths = os.environ["LD_LIBRARY_PATH"].split(":")
#     if libdir not in libpaths:
#         print("WARNING: libdir %s not in LD_LIBRARY_PATH" % libdir)

# str = "cp ../src/libsparta.so %s" % libdir
# print(str)
# outstr = subprocess.getoutput(str)
# if len(outstr.strip()):
#     print(outstr)

# # copy sparta.py to pydir if it exists
# # if pydir not specified, install in site-packages via distutils setup()

# if pydir:
#     if not os.path.isdir(pydir):
#         print("ERROR: pydir %s does not exist" % pydir)
#         sys.exit()
#     str = "cp ../python/sparta.py %s" % pydir
#     print(str)
#     outstr = subprocess.getoutput(str)
#     if len(outstr.strip()):
#         print(outstr)
#     sys.exit()

print("installing sparta.py in Python site-packages dir")

# os.chdir("../python")  # in case invoked via make in src dir

def read(*names, **kwargs):
    """
    Read file text content.

    :param names: Some path
    :type names: variable length arguments
    :param kwargs: Some option
    :type kwargs: keyworded variable arguments
    :return: file content
    :rtype: stream
    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """
    Find version string.

    :param file_paths: Some paths
    :type file_paths: path-like objects
    :return: version string.
    :rtype: string
    :raises RuntimeError: Unable to find version string

    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


cwd = os.path.abspath(os.path.dirname(__file__))
# spartaLib = os.path.join(cwd, "../build/src/libsparta.so")
spartaLib = os.path.join("libsparta.so")

with open("requirements.txt", "r") as fh:
    dependencies = [l.strip() for l in fh]


module1 = Extension('demo',
                    sources = ['demo.c'])

print(spartaLib)
print(spartaLib)
print(spartaLib)
# log(spartaLib)

# sys.argv = ["setup.py", "install"]  # as if had run "python setup.py install"
version = find_version("sparta", "__init__.py")
# version="7Jan2022"
setup(
    name="sparta",
    version=version,
    author="Steve Plimpton",
    author_email="sjplimp@sandia.gov",
    url="http://sparta.sandia.gov",
    description="SPARTA DSMC library",
    # py_modules=["sparta"],
    packages=["sparta"],
    # description="Debrisk Uncertainties Quantification Tool Kit.",
    # long_description=long_description,
    # author="R.Tech",
    # license="",
    # packages=["duq", "duq.atdbcnes", "duq.post"],
    # package_data={"data": ["old/*.txt",]},
    # data_files=["requirements.txt"],
    # entry_points={"console_scripts": ["xcompare = duq.comparaisonXlsx:xcompare", "duq = duq.inputParser:main", "qwark = duq.debriskSimulationReport:main", "rubber = duq.estimatorForceMultipleOfX:main",]},
    # tests_require=tests_require,
    # install_requires=dependencies,
    # zip_safe=False,
    # python_requires=">=3.7",
    # extras_require={"testing": tests_require},
    # setup_requires=["pytest-runner",],
    # package_data={'': [spartaLib]},
        package_data={
        # If any package contains *.so, include them:
        "": ["*.so",],
    }
)
