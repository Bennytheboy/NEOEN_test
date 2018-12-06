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

test_name = 'Voltage_disturbance'
# psse_csv_name ='5.2.5.4_Vol_distPSSE Voltage Disturbance'+'.csv'
# pscad_csv_name = ''+'.csv'
time_psse = []
P_inv_psse = []
Q_inv_psse = []
U_inv_psse = []
P_poc_psse = []
Q_poc_psse = []
U_poc_psse = []


#[TIME, FREQ, V_INV, V_POC, P_INV, P_POC, Q_INV, Q_POC]),
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/BM_Voltage_Dist/' + 'PSSE Voltage Disturbance.csv', 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(0, len(FileData)):
    time_psse.append(numpy.round(float(FileData[t_entry][0]),4))
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

with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test05_VD/VoltageDisturbance_0_01.txt') as f1:
    lines1 = f1.readlines()
    time_pscad      = [float(line.split()[0]) for line in lines1]
    F_sys_pscad = [float(line.split()[1]) for line in lines1]
    U_poc_pscad = [float(line.split()[2]) for line in lines1]
    P_inv_pscad = [float(line.split()[3]) for line in lines1]
    Q_inv_pscad = [float(line.split()[8]) for line in lines1]
    U_inv_pscad = [float(line.split()[10]) for line in lines1]
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test05_VD/VoltageDisturbance_0_02.txt') as f2:
    lines2 = f2.readlines()
    Q_poc_pscad = [float(line.split()[9]) for line in lines2]
with open('F:/PosDoc Projects/11_Industrial Projects/HuaWei/PSCAD_DATA/Test05_VD/VoltageDisturbance_0_03.txt') as f3:
    lines3 = f3.readlines()
    P_poc_pscad = [float(line.split()[2]) for line in lines3]

TIME_PSCAD_start_index = (numpy.abs(time_pscad)).argmin()
TIME_PSCAD_end_index = (numpy.abs(time_pscad)).argmax()

t_TIME_PSCAD = time_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index]
t_P_POC_PSCAD = P_poc_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];
t_P_INV_PSCAD = P_inv_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];
t_Q_POC_PSCAD = Q_poc_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];
t_Q_INV_PSCAD = Q_inv_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];
t_V_POC_PSCAD = U_poc_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];
t_V_INV_PSCAD = U_inv_pscad[TIME_PSCAD_start_index:TIME_PSCAD_end_index];

TIME_PSSE_start_index = (numpy.abs(time_psse)).argmin()
TIME_PSSE_end_index = (numpy.abs(time_psse)).argmax()

t_TIME_PSSE = time_psse[TIME_PSSE_start_index:TIME_PSSE_end_index]
t_P_POC_PSSE = P_poc_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];
t_P_INV_PSSE = P_inv_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];
t_Q_POC_PSSE = Q_poc_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];
t_Q_INV_PSSE = Q_inv_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];
t_V_POC_PSSE = U_poc_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];
t_V_INV_PSSE = U_inv_psse[TIME_PSSE_start_index:TIME_PSSE_end_index];


# set figure preference
mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['axes.grid'] = 'on'
mpl.rcParams['font.size'] = 18
mpl.rcParams['lines.linewidth'] = 3.0
mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'small'

CurrentFig, CurrentAx = plt.subplots(3, 2, sharex=False, figsize=(20, 20))
CurrentAx[0][0].plot(t_TIME_PSCAD, t_V_INV_PSCAD, '--', alpha=0.8, linewidth=3.0);
CurrentAx[1][0].plot(t_TIME_PSCAD, t_P_INV_PSCAD, '--', alpha=0.8, linewidth=3.0);
CurrentAx[2][0].plot(t_TIME_PSCAD, t_Q_INV_PSCAD, '--', alpha=0.8, linewidth=3.0);
CurrentAx[0][1].plot(t_TIME_PSCAD, t_V_POC_PSCAD, '--', alpha=0.8, linewidth=3.0);
CurrentAx[1][1].plot(t_TIME_PSCAD, t_P_POC_PSCAD, '--', alpha=0.8, linewidth=3.0);
CurrentAx[2][1].plot(t_TIME_PSCAD, t_Q_POC_PSCAD, '--', alpha=0.8, linewidth=3.0);

CurrentAx[0][0].plot(t_TIME_PSSE, t_V_INV_PSSE, '--', alpha=0.8, linewidth=3.0)
CurrentAx[1][0].plot(t_TIME_PSSE, t_P_INV_PSSE, '--', alpha=0.8, linewidth=3.0)
CurrentAx[2][0].plot(t_TIME_PSSE, t_Q_INV_PSSE, '--', alpha=0.8, linewidth=3.0)
# CurrentAx[0][1].plot(t_TIME_PSSE, t_V_SET_PSSE,color='orange',linestyle='--')
CurrentAx[0][1].plot(t_TIME_PSSE, t_V_POC_PSSE, '--', alpha=0.8, linewidth=3.0)
# CurrentAx[1][1].plot(t_TIME_PSSE, t_P_SET_PSSE,color='green',linestyle='--')
CurrentAx[1][1].plot(t_TIME_PSSE, t_P_POC_PSSE, '--', alpha=0.8, linewidth=3.0)
CurrentAx[2][1].plot(t_TIME_PSSE, t_Q_POC_PSSE, '--', alpha=0.8, linewidth=3.0)

CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=18)
CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=18)
CurrentAx[2][0].tick_params(axis='both', which='both', labelsize=18)
CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=18)
CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=18)
CurrentAx[2][1].tick_params(axis='both', which='both', labelsize=18)

t_start = 59
t_end = 69

CurrentAx[0][0].set_xlim([t_start, t_end])
CurrentAx[1][0].set_xlim([t_start, t_end])
CurrentAx[2][0].set_xlim([t_start, t_end])
CurrentAx[0][1].set_xlim([t_start, t_end])
CurrentAx[1][1].set_xlim([t_start, t_end])
CurrentAx[2][1].set_xlim([t_start, t_end])

CurrentAx[0][0].set_ylim([0.9, 1.4])
CurrentAx[0][1].set_ylim([0.9, 1.4])
CurrentAx[1][0].set_ylim([0, 150])
CurrentAx[1][1].set_ylim([0, 150])
# CurrentAx[1][1].set_yticks([0, 150])
CurrentAx[2][0].set_ylim([-10, 10])
CurrentAx[2][1].set_ylim([-150, 150])
# CurrentAx[2][1].set_yticks([-200, -150, -110.6, -50, 0, 50, 110.6, 150, 200])

CurrentAx[0][0].set_xlabel(r"""TIME/s""")
CurrentAx[0][1].set_xlabel(r"""TIME/s""")
CurrentAx[0][0].set_ylabel(r"""Inverter Voltage /PU""")
CurrentAx[0][1].set_ylabel(r"""WISF POC Voltage/PU""")

CurrentAx[1][0].set_xlabel(r"""TIME/s""")
CurrentAx[1][1].set_xlabel(r"""TIME/s""")
CurrentAx[1][0].set_ylabel(r"""Inverter PGen / MW""")
CurrentAx[1][1].set_ylabel(r"""WISF PGen / MW""")

CurrentAx[2][0].set_xlabel(r"""TIME/s""")
CurrentAx[2][1].set_xlabel(r"""TIME/s""")
CurrentAx[2][0].set_ylabel(r"""Inverter QGen / MVar""")
CurrentAx[2][1].set_ylabel(r"""WISF QGen / MVar""")

CurrentAx[0][0].legend(["PSCAD", "PSSE"])
CurrentAx[1][0].legend(["PSCAD", "PSSE"])
CurrentAx[2][0].legend(["PSCAD", "PSSE"])
CurrentAx[0][1].legend(["PSCAD", "PSSE"])
CurrentAx[1][1].legend(["PSCAD", "PSSE"])
CurrentAx[2][1].legend(["PSCAD", "PSSE"])

save_figure_name = 'F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/rev1/' + '5.2.5.4_Voltage_dist_BM_psse_'+str(t_start)+'_.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)