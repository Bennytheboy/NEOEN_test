# File:"C:\Users\chang\Desktop\02 Full System - Copy\01 Summer 2016-17 high SN\5.2.5.12 Network Transfer Capacity.py", generated on THU, APR 12 2018   9:31, release 32.02.04
import os, sys

sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN;" + os.environ['PATH'])
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSPY27""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27;" + os.environ['PATH'])
import socket
import struct
import time
import psse34
import psspy
import redirect
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import dyntools
import csv
from datetime import date
import shutil
FigurePath = "F:/NEOEN/R_Results/123456789/"
shutil.rmtree(FigurePath)