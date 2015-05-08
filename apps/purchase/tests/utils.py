import os, sys

def load_fixture(filename):
    abs_name =  os.path.join(os.path.dirname(__file__), "fixtures", filename)
    return open(abs_name).read()

