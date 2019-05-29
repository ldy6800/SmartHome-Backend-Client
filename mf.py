import py_compile
import sys
import os

py_compile.compile(sys.argv[1])

os.system("cp ./__pycache__/" + sys.argv[1].split('.')[0] + ".cpython-35.pyc ./sub.pyc")
print("cp ./__pycache__/" + sys.argv[1].split('.')[0] + ".cpython-35.pyc ./sub.pyc")
os.system("chmod 0700 ./sub.pyc")
print("chmod 0700 ./sub.pyc")

