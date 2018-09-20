# Import modules
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

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.
# if on laptop
LoadScenario = "SummerPeakLoad"
ClauseName = "5.2.5.5 Contingency Response_reclose"
ProgramPath = "C:/NEOEN/P_SimulationScripts/"
GridInfoPath = "C:/NEOEN/NEM_files/"
HuaweiModelPath = "C:/NEOEN/Huawei_models/"
OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
FigurePath = "C:/NEOEN/R_Results/"

# if on desktop
# LoadScenario = "SummerPeakLoad"
# ClauseName = "5.2.5.5 Contingency Response_reclose"
# ProgramPath = "F:/NEOEN/P_SimulationScripts/"
# GridInfoPath = "F:/NEOEN/NEM_files/"
# HuaweiModelPath = "F:/NEOEN/Huawei_models/"
# OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
# FigurePath = "F:/NEOEN/R_Results/"

if LoadScenario == "SummerPeakLoad":
    file_name = "SummerHi-20171219-153047-34-SystemNormal_all"
if LoadScenario == "SummerLowLoad":
    file_name = "SummerLo-20171226-043047-34-SystemNormal_all"
if LoadScenario == "SimplifiedSystem":
    file_name = "NEOEN Western Downs Solar Farm_C3WV_mod_T"

Bus_Name = []
Bus_List = []
Bus_Vol = []

# Initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name +".raw")
psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(GridInfoPath + 'dsusr.dll')
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
psspy.addmodellibrary(GridInfoPath + 'GEWTG34.dll')
psspy.addmodellibrary(GridInfoPath + 'SMAPPC_B111_34_IVF111.dll')
psspy.addmodellibrary(GridInfoPath + 'SMASC_C135_34_IVF111.dll')

psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])


# re - initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")

psspy.dscn(30531)
psspy.dscn(36530)
psspy.dscn(37530)
psspy.dscn(50030)  # add for Clenergy project

psspy.machine_data_2(30531, r"""12""", [0, _i, _i, _i, _i, _i],
                     [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(37530, r"""12""", [0, _i, _i, _i, _i, _i],
                     [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [100, _f, 60, -40, 120, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [100, _f, 60, -40, 120, _f,120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [100, _f, 60, -40, 120, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [100, _f, 60, -40, 120, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(100, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, 5, _f, 132, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(100, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, _f, 5, 132, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
#                       _f])  # be careful, partial active power = not enough solar irraidance.
psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])
t_q = 0.569
psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 5, 0.5)
psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 6, -0.5)
psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 13, -t_q)
psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 14, t_q)
psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 13, -t_q)
psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 14, t_q)
psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 13, -t_q)
psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 14, t_q)
psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 13, -t_q)
psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 14, t_q)
psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 23, 0.001)  # QV droop deadband
psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 24, 0.4)  # QV droop
psspy.change_plmod_icon(101, r"""1""", r"""GPMPPC""", 4, 2)  # kVar control =0, PF control = 1, Droop Control = 2, Voltage Control = 3
psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 10, 1.0)

for t_var in range(0, 9000):
    psspy.change_var(t_var, 0)
psspy.plmod_status(30531, r"""1""", 1, 0)
psspy.plmod_status(30531, r"""1""", 6, 0)
psspy.plmod_status(30531, r"""1""", 7, 0)
psspy.plmod_status(37530, r"""1""", 1, 0)
psspy.plmod_status(37530, r"""1""", 6, 0)
psspy.plmod_status(37530, r"""1""", 7, 0)
psspy.bus_frequency_channel([1, 400], r"""System frequency""")
psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
psspy.voltage_channel([3, -1, -1, 400], r"""WDs SF POC Voltage Mag.""")
psspy.branch_p_and_q_channel([4, -1, -1, 101, 111], r"""1""", [r"""P Injection""", r"""Q Injection"""])
# psspy.branch_p_and_q_channel([7, -1, -1, 101, 111], r"""1""", [r"""Pelec 101""", r"""Qelec 101"""])
# psspy.branch_p_and_q_channel([9, -1, -1, 102, 112], r"""1""", [r"""Pelec 102""", r"""Qelec 102"""])
# psspy.branch_p_and_q_channel([11, -1, -1, 103, 113], r"""1""", [r"""Pelec 103""", r"""Qelec 103"""])
# psspy.branch_p_and_q_channel([13, -1, -1, 104, 114], r"""1""", [r"""Pelec 104""", r"""Qelec 104"""])
[ierr, var_ppc_conp] = psspy.mdlind(101, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(101, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(101, '1', 'EXC', 'ICON')
[ierr, var_inv_con] = psspy.mdlind(101, '1', 'GEN', 'CON')
[ierr, var_inv_var] = psspy.mdlind(101, '1', 'GEN', 'VAR')

# convert load , do not change
psspy.cong(0)
psspy.bsys(0, 0, [0.0, 500.], 1, [7], 0, [], 0, [], 0, [])
psspy.bsys(0, 0, [0.0, 500.], 1, [7], 0, [], 0, [], 0, [])
psspy.conl(0, 0, 1, [0, 0], [91.27, 19.36, -126.88, 188.43])
psspy.conl(0, 0, 2, [0, 0], [91.27, 19.36, -126.88, 188.43])
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 6, [37600, 37601, 37602, 37580, 37584, 38588], 0, [], 0, [])
psspy.conl(1, 0, 2, [0, 0], [52.75, 58.13, 5.97, 95.52])
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 1, [21790], 0, [], 0, [])
psspy.conl(1, 0, 2, [0, 0], [86.63, 25.19, -378.97, 347.97])
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 1, [45082], 0, [], 0, [])
psspy.conl(1, 0, 2, [0, 0], [51.36, 59.32, -228.04, 254.01])
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 9, [40320, 40340, 40350, 40970, 40980, 40990, 41050, 41071, 41120], 0, [],
           0, [])
psspy.conl(1, 0, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.bsys(0, 0, [0.4, 500.], 0, [], 0, [], 0, [], 0, [])

# start simulation
psspy.strt_2([0,0], OutputFilePath)
psspy.run(0, 1, 1000, 1, 0)
psspy.run(0, 5, 1000, 1, 0)
psspy.dist_branch_fault(46523, 46660, '1', 1, 275.0, [0.00, -0.2E+10])
fault_name = 'ThreePhase'
psspy.run(0, 5.12, 1000, 1, 0)
psspy.dist_branch_trip(46523, 46660, '1')
psspy.run(0, 20.12, 1000, 1, 0)
psspy.dist_branch_close(46523,46660,r"""1""")
psspy.run(0, 20.22, 1000, 1, 0)
psspy.dist_branch_trip(46523, 46660, '1')
psspy.run(0, 30, 1000, 1, 0)

# start draw curves
# new folder if necessary
GraphPath = FigurePath + ClauseName + '/' + LoadScenario + '/' + fault_name
if not os.path.exists(GraphPath):
    os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()
# set figure preference
mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['axes.grid'] = 'on'

mpl.rcParams['font.size'] = 24

mpl.rcParams['lines.linewidth'] = 3.0

mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'small'


CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
CurrentAx[0][0].plot(chandata['time'], chandata[2]);
CurrentAx[1][0].plot(chandata['time'], chandata[3]);
CurrentAx[0][1].plot(chandata['time'], chandata[4]);
CurrentAx[1][1].plot(chandata['time'], chandata[5]);

CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

CurrentAx[0][0].set_xlim([4, 7])
CurrentAx[1][0].set_xlim([4, 7])
CurrentAx[0][1].set_xlim([4, 7])
CurrentAx[1][1].set_xlim([4, 7])

CurrentAx[0][0].set_ylim([0, 1.5])
CurrentAx[1][0].set_ylim([0, 1.5])
CurrentAx[0][1].set_ylim([-5, 120])
CurrentAx[1][1].set_ylim([-50, 100])

CurrentAx[0][0].set_xlabel(r"""Time/s""")
CurrentAx[1][0].set_xlabel(r"""Time/s""")
CurrentAx[0][1].set_xlabel(r"""Time/s""")
CurrentAx[1][1].set_xlabel(r"""Time/s""")

CurrentAx[0][0].set_ylabel(r"""Voltage/PU""")
CurrentAx[1][0].set_ylabel(r"""Voltage/PU""")
CurrentAx[0][1].set_ylabel(r"""Power/MW""")
CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

CurrentAx[0][0].legend(['Inverter Terminal Voltage'])
CurrentAx[1][0].legend(['WDSF PoC Voltage'])
CurrentAx[0][1].legend(['Inverter P Output'])
CurrentAx[1][1].legend(['Inverter Q Output'])

save_figure_name = GraphPath + "/" + '46660_46523_Reclose_3ph' + '.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)

# chnfobj = dyntools.CHNF(OutputFilePath)
# short_title, chanid, chandata = chnfobj.get_data()
# freq_data = numpy.array(chandata[1])
#
# # set figure preference
# mpl.rcParams['grid.color'] = 'k'
# mpl.rcParams['grid.linestyle'] = ':'
# mpl.rcParams['grid.linewidth'] = 0.5
# mpl.rcParams['axes.grid'] = 'on'
#
# mpl.rcParams['font.size'] = 24
#
# mpl.rcParams['lines.linewidth'] = 3.0
#
# mpl.rcParams['legend.fancybox'] = True
# mpl.rcParams['legend.numpoints'] = 3
# mpl.rcParams['legend.fontsize'] = 'small'
#
# CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
# CurrentAx[0][0].plot(chandata['time'], p_data_101)
# CurrentAx[1][0].plot(chandata['time'], p_data_102)
# CurrentAx[0][1].plot(chandata['time'], p_data_103)
# CurrentAx[1][1].plot(chandata['time'], p_data_104)
#
# CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)
#
# CurrentAx[0][0].set_xlim(left=4)
# CurrentAx[1][0].set_xlim(left=4)
# CurrentAx[0][1].set_xlim(left=4)
# CurrentAx[1][1].set_xlim(left=4)
#
# CurrentAx[0][0].set_ylim([-50, 200])
# CurrentAx[1][0].set_ylim([-50, 200])
# CurrentAx[0][1].set_ylim([-50, 200])
# CurrentAx[1][1].set_ylim([-50, 200])
#
# CurrentAx[0][0].set_xlabel(r"""Time/s""")
# CurrentAx[1][0].set_xlabel(r"""Time/s""")
# CurrentAx[0][1].set_xlabel(r"""Time/s""")
# CurrentAx[1][1].set_xlabel(r"""Time/s""")
#
# CurrentAx[0][0].set_ylabel(r"""Power/MW""")
# CurrentAx[1][0].set_ylabel(r"""Power/MW""")
# CurrentAx[0][1].set_ylabel(r"""Power/MW""")
# CurrentAx[1][1].set_ylabel(r"""Power/MW""")
#
# CurrentAx[0][0].set_title(r"""Inverter 101 P Output""")
# CurrentAx[1][0].set_title(r"""Inverter 102 P Output""")
# CurrentAx[0][1].set_title(r"""Inverter 103 P Output""")
# CurrentAx[1][1].set_title(r"""Inverter 104 P Output""")
#
# save_figure_name = GraphPath + "/" + EventName[i] + ' ' + str(Branch_Outage_List_Start[i]) + '-' + str(
#     Branch_Outage_List_End[i]) + '_P.png'
# CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
# plt.close(CurrentFig)
# ############### save Q graphs
# # read data curves
# chnfobj = dyntools.CHNF(OutputFilePath)
# short_title, chanid, chandata = chnfobj.get_data()
# freq_data = numpy.array(chandata[1])
#
# # set figure preference
# mpl.rcParams['grid.color'] = 'k'
# mpl.rcParams['grid.linestyle'] = ':'
# mpl.rcParams['grid.linewidth'] = 0.5
# mpl.rcParams['axes.grid'] = 'on'
#
# mpl.rcParams['font.size'] = 24
#
# mpl.rcParams['lines.linewidth'] = 3.0
#
# mpl.rcParams['legend.fancybox'] = True
# mpl.rcParams['legend.numpoints'] = 3
# mpl.rcParams['legend.fontsize'] = 'small'
#
# CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
# CurrentAx[0][0].plot(chandata['time'], q_data_101);
# CurrentAx[1][0].plot(chandata['time'], q_data_101);
# CurrentAx[0][1].plot(chandata['time'], q_data_101);
# CurrentAx[1][1].plot(chandata['time'], q_data_101);
#
# CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
# CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)
#
# CurrentAx[0][0].set_xlim(left=4)
# CurrentAx[1][0].set_xlim(left=4)
# CurrentAx[0][1].set_xlim(left=4)
# CurrentAx[1][1].set_xlim(left=4)
#
# CurrentAx[0][0].set_ylim([-100, 100])
# CurrentAx[1][0].set_ylim([-100, 100])
# CurrentAx[0][1].set_ylim([-100, 100])
# CurrentAx[1][1].set_ylim([-100, 100])
#
# CurrentAx[0][0].set_xlabel(r"""Time/s""")
# CurrentAx[1][0].set_xlabel(r"""Time/s""")
# CurrentAx[0][1].set_xlabel(r"""Time/s""")
# CurrentAx[1][1].set_xlabel(r"""Time/s""")
#
# CurrentAx[0][0].set_ylabel(r"""Power/MVR""")
# CurrentAx[1][0].set_ylabel(r"""Power/MVR""")
# CurrentAx[0][1].set_ylabel(r"""Power/MVR""")
# CurrentAx[1][1].set_ylabel(r"""Power/MVR""")
#
# CurrentAx[0][0].set_title(r"""Inverter 101 Q Output""")
# CurrentAx[1][0].set_title(r"""Inverter 102 Q Output""")
# CurrentAx[0][1].set_title(r"""Inverter 103 Q Output""")
# CurrentAx[1][1].set_title(r"""Inverter 104 Q Output""")
#
# save_figure_name = GraphPath + "/" + EventName[i] + ' ' + str(Branch_Outage_List_Start[i]) + '-' + str(
#     Branch_Outage_List_End[i]) + '_Q.png'
# CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
# plt.close(CurrentFig)



    # if Branch_kV[i] == 330 or Branch_kV[i] == 275:
    #     fault_time = 0.120
    # if Branch_kV[i] == 132:
    #     fault_time = 0.500

# if fault_type == 2:  # single phase, no path to ground, line-to-ground, breaker @ bus i,
#     psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 1, 1, 0, 0],
#                           [0.5, 0.0, 0.000001, 0.0, 0.0])
#     fault_name = 'SinglePhase'
#     if Branch_kV[i] == 330 or Branch_kV[i] == 275:
#         fault_time = 0.250
#     if Branch_kV[i] == 132:
#         fault_time = 0.720
#
# if fault_type == 3:  # phase to phase,  no path to ground, line-to-line-not to ground, breaker @ bus i, #line to ground=9999
#     psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 2, 1, 0, 0],
#                           [0.5, 9999.0, 9999.0, 0.0, 0.000001])
#     fault_name = 'TwoPhase'
#     if Branch_kV[i] == 330 or Branch_kV[i] == 275:
#         fault_time = 0.250
#     if Branch_kV[i] == 132:
#         fault_time = 0.720
#
# if fault_type == 4:  # phase to phase to ground  #line to line to ground, line to line
#     psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 2, 1, 0, 0],
#                           [0.5, 0.0, 0.000001, 0.0, 0.000001])
#     fault_name = 'TwoPhaseGround'
#     if Branch_kV[i] == 330 or Branch_kV[i] == 275:
#         fault_time = 0.250
#     if Branch_kV[i] == 132:
#         fault_time = 0.720

