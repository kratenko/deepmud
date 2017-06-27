import os
import sys

os.chdir("..")
print(os.path.dirname(os.path.realpath(__file__)))
print(__file__)

print(sys.path[0])
print(sys.path)
