import os
from fnmatch import fnmatch
def file():
    demo=list()
    print(os.getcwd())
    root="C:/Users/pamid/PycharmProjects/djagoproject/robot"
    for path, dirs, files in os.walk(root):
        for f in files:
            if f.endswith('.py'):
                 demo.append(f)
    print(demo)

file()