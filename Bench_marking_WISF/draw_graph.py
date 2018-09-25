# Import modules
import glob, os, sys, math, csv, time, logging, traceback, exceptions
import shutil
WorkingFolder = os.getcwd()

PSSE_LOCATION = r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN"
sys.path.append(PSSE_LOCATION)
os.environ['PATH'] = os.environ['path'] + ';' + PSSE_LOCATION

PSSE_LOCATION = r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27"
sys.path.append(PSSE_LOCATION)
os.environ['PATH'] = os.environ['path'] + ';' + PSSE_LOCATION

import socket
import struct

# import psse34
# import psspy
import redirect
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import dyntools


time_psse = []
P_inv_psse = []
Q_inv_psse = []
U_inv_psse = []
P_poc_psse = []
Q_poc_psse = []
U_poc_psse = []

#[TIME, FREQ, V_INV, V_POC, P_INV, P_POC, Q_INV, Q_POC]),
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results/Benchmarking/' + "5.2.5.5_contingencyPSSE Fault.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(0, len(FileData)):
    time_psse.append(float(FileData[t_entry][0]))
    U_inv_psse.append(float(FileData[t_entry][2]))
    U_poc_psse.append(float(FileData[t_entry][3]))
    P_inv_psse.append(float(FileData[t_entry][4]))
    P_poc_psse.append(float(FileData[t_entry][5]))
    Q_inv_psse.append(float(FileData[t_entry][6]))
    Q_poc_psse.append(float(FileData[t_entry][7]))

time_psse = numpy.array(time_psse)
P_inv_psse = numpy.array(P_inv_psse)
Q_inv_psse = numpy.array(Q_inv_psse)
U_inv_psse = numpy.array(U_inv_psse)
P_poc_psse = numpy.array(P_poc_psse)
Q_poc_psse = numpy.array(Q_poc_psse)
U_poc_psse = numpy.array(U_poc_psse)


time_pscad = []
P_inv_pscad = []
Q_inv_pscad = []
U_inv_pscad = []
P_poc_pscad = []
Q_poc_pscad = []
U_poc_pscad = []

#[TIME, FREQ, V_INV, V_POC, P_INV, P_POC, Q_INV, Q_POC]),
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results/Benchmarking/' + "PSCAD-Contingency.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)-1):
    time_pscad.append(numpy.round(float(FileData[t_entry][0]),4))
    U_inv_pscad.append(float(FileData[t_entry][13]))
    U_poc_pscad.append(float(FileData[t_entry][11]))
    P_inv_pscad.append(float(FileData[t_entry][5]))
    P_poc_pscad.append(float(FileData[t_entry][1]))
    Q_inv_pscad.append(float(FileData[t_entry][9]))
    Q_poc_pscad.append(float(FileData[t_entry][8]))

time_pscad = numpy.array(time_pscad)
P_inv_pscad = numpy.array(P_inv_pscad)
Q_inv_pscad = numpy.array(Q_inv_pscad)
U_inv_pscad = numpy.array(U_inv_pscad)
P_poc_pscad = numpy.array(P_poc_pscad)
Q_poc_pscad = numpy.array(Q_poc_pscad)
U_poc_pscad = numpy.array(U_poc_pscad)

# set figure preference
mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['axes.grid'] = 'on'

mpl.rcParams['font.size'] = 22

mpl.rcParams['lines.linewidth'] = 3.0

mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'small'
mpl.rcParams['legend.loc'] = 'lower right'

CurrentFig, CurrentAx = plt.subplots(3, 2, sharex=False, figsize=(20, 15))

CurrentAx[0][0].plot(time,P_inv_pscad*1760,color='green',linestyle='--')
CurrentAx[0][0].plot(time, P_inv_psse)

CurrentAx[1][0].plot(time,Q_inv_pscad*1760,color='green',linestyle='--')
CurrentAx[1][0].plot(time, Q_inv_psse)

CurrentAx[2][0].plot(time,U_inv_pscad,color='green',linestyle='--')
CurrentAx[2][0].plot(time, U_inv_psse)

CurrentAx[0][1].plot(time,P_poc_pscad,color='green',linestyle='--');
CurrentAx[0][1].plot(time, P_poc_psse)

CurrentAx[1][1].plot(time,Q_poc_pscad,color='green',linestyle='--');
CurrentAx[1][1].plot(time, Q_poc_psse)

CurrentAx[2][1].plot(time,U_poc_pscad,color='green',linestyle='--');
CurrentAx[2][1].plot(time, U_poc_psse)

CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[2][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[2][1].tick_params(axis='both', which='both', labelsize=24)

CurrentAx[0][0].set_xlim(left=0)
CurrentAx[1][0].set_xlim(left=0)
CurrentAx[2][0].set_xlim(left=0)
CurrentAx[0][1].set_xlim(left=0)
CurrentAx[1][1].set_xlim(left=0)
CurrentAx[2][1].set_xlim(left=0)

CurrentAx[0][0].set_ylim([0, 120])
CurrentAx[1][0].set_ylim([-60, 80])
CurrentAx[2][0].set_ylim([0.0, 1.4])
CurrentAx[0][1].set_ylim([-5, 100])
CurrentAx[1][1].set_ylim([-100, 120])
CurrentAx[2][1].set_ylim([0.0, 1.4])

# CurrentAx[0][0].set_xlabel(r"""Time/s""")
# CurrentAx[1][0].set_xlabel(r"""Time/s""")
CurrentAx[2][0].set_xlabel(r"""Time/s""")
# CurrentAx[0][1].set_xlabel(r"""Time/s""")
# CurrentAx[1][1].set_xlabel(r"""Time/s""")
CurrentAx[2][1].set_xlabel(r"""Time/s""")

CurrentAx[0][0].set_ylabel(r"""P/MW""")
CurrentAx[1][0].set_ylabel(r"""Q/MVar""")
CurrentAx[2][0].set_ylabel(r"""U/PU""")
# CurrentAx[0][1].set_ylabel(r"""P_Poc/MW""")
# CurrentAx[1][1].set_ylabel(r"""Q_Poc/MVar""")
# CurrentAx[2][1].set_ylabel(r"""U_Poc/PU""")

CurrentAx[0][0].legend([r"""Inverter P_gen"""])
CurrentAx[1][0].legend([r"""Inverter Q_gen"""])
CurrentAx[2][0].legend([r"""Inverter E_terminal"""])
CurrentAx[0][1].legend([r"""WISF PoC P_setpoint""","""WISF P Injection"""])
CurrentAx[1][1].legend([r"""WISF Q Injection"""])
CurrentAx[2][1].legend([r"""WISF PoC Voltage"""])
# CurrentAx[2][1].legend([r"""WDSF PoC Voltage"""])

save_figure_name = 'F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results/Benchmarking/' + '5.2.5.5_contingencyPSSE Fault.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)
raw_input("Press enter to exit...")
redirect.reset()
