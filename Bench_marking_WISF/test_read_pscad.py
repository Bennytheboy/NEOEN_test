import matplotlib.pyplot as plt
import numpy as np

with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test01_3Phase0/Test01_3phase0_01.txt') as f1:
    lines1 = f1.readlines()
    Time      = [float(line.split()[0]) for line in lines1]
    Frequency = [float(line.split()[1]) for line in lines1]
    Vpoc = [float(line.split()[2]) for line in lines1]
    Pgen = [float(line.split()[3]) for line in lines1]
    Qgen = [float(line.split()[8]) for line in lines1]
    Eterm = [float(line.split()[10]) for line in lines1]
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test01_3Phase0/Test01_3phase0_02.txt') as f2:
    lines2 = f2.readlines()
    Qpoc = [float(line.split()[8]) for line in lines2]
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test01_3Phase0/Test01_3phase0_03.txt') as f3:
    lines3 = f3.readlines()
    Ppoc = [float(line.split()[2]) for line in lines3]

