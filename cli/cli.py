import argparse
from model.logger import Logger
from model import gskel

#gskel cli - commandline interface for gskel

parser = argparse.ArgumentParser(prog='gSkel')
parser.add_argument('-v', help='display version information and quit')

args = parser.parse_args()
print args
