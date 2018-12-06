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

import psse34
import psspy
import redirect
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import dyntools

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.
LoadScenario="SimplifiedSystem"
ClauseName="Benchmarking_vsetp_VP"
ProgramPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/P_SimulationProgram/"
GridInfoPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/"+"D_"+LoadScenario+"/"
HuaweiModelPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/D_HuaweiModels/"
OutputFilePath=ProgramPath+"SimulationOutput4.outx"
FigurePath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/"
TestName ="Voltage_setpoint"

if LoadScenario=="SummerPeakLoad":
    file_name="SummerHi-20171219-153047-34-SystemNormal"
if LoadScenario=="SummerLowLoad":
    file_name="SummerLowNormal-20161225-040047"
if LoadScenario=="SimplifiedSystem":
    file_name="WISF_1.05"


psspy.case(GridInfoPath+file_name+".sav")
psspy.resq(GridInfoPath  + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath  + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath+'HWS2000_psse34_V1.5.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_PPC_V13_34_V3.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_SB_V7.dll')
psspy.plant_chng_3(500,0,_i,[ 1.05,_f])
psspy.plant_chng_3(1000,0,_i,[ 1.045,_f])
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[0.300,_f, 0.001,0.004,_f,_f,_f,_f])
psspy.machine_data_2(500, r"""1""", [_i, _i, _i, _i, _i, _i],[85, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.two_winding_chng_5(700,800,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,800,_i,_i,1,_i,_i,_i],[_f,_f,_f, 1.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""SS-TF-1""",
r"""YNYN0""")
psspy.machine_chng_2(500,r"""1""",[_i,_i,_i,_i,_i,_i],[_f, 0.0, 0.0, 0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])

psspy.fnsl([0,0,0,1,0,0,99,0])

# convert load , do not change
psspy.cong(0)
psspy.change_plmod_icon(500,r"""1""",r"""GPMPPC""",1,20)   #ori=5
psspy.change_plmod_icon(500,r"""1""",r"""GPMPPC""",2,20)   #ori=5
psspy.change_plmod_icon(500,r"""1""",r"""GPMPPC""",3,50)   #ori=5
psspy.change_plmod_icon(500,r"""1""",r"""GPMPPC""",4,2)    #ori=3
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",23, 0.003)  #ori=0.003
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",24, 0.5)   # droop  ori=5%
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",2, 0.02)   #  proportional gain  ori=0.001
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",3, 0.25)   # integral gain  ori=0.15
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",5, 0.5)  #PPC reactive power UB   #ori=1
psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",6, -0.3)  #PPC reactive power LB   #ori=1

# psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",7, 0.01)  ##ramp up

# psspy.change_plmod_con(500,r"""1""",r"""HWS2000""",13,-0.46)
# psspy.change_plmod_con(500,r"""1""",r"""HWS2000""",14,0.46)


psspy.bus_frequency_channel([1,1000],r"""System frequency""")
ierr=psspy.machine_array_channel([2,4,500],r"""1""",r"""Inverter Terminal Voltage""")
ierr=psspy.voltage_channel([3,-1,-1,800],r"""WISF PoC Voltage""")
psspy.branch_p_and_q_channel([4,-1,-1,800,900],r"""1""",[r"""P Injection""",r"""Q Injection"""])
psspy.branch_p_and_q_channel([6,-1,-1,500,600],r"""1""",[r"""P inv""",r"""Q inv"""])
# ierr=psspy.machine_array_channel([6,2,500],r"""1""",r"""Pelec Inverter""")
# ierr=psspy.machine_array_channel([7,3,500],r"""1""",r"""Qelec Inverter""")
[ierr, var_ppc_conp] = psspy.mdlind(500, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(500, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(500, '1', 'EXC', 'ICON')
[ierr, var_inv1_con] = psspy.mdlind(500, '1', 'GEN', 'CON')
[ierr, var_inv1_var]=  psspy.mdlind(500,'1','GEN','VAR')
[ierr, var_inv1_mod]=  psspy.mdlind(500,'1','GEN','ICON')

ierr=psspy.var_channel([8,var_ppc_setp+68],"Voltage Setpoint")
ierr=psspy.var_channel([9,var_ppc_setp+10],"Active Power Setpoint")

#
# psspy.change_con(var_ppc_conp+1, pp_g)  #Proportional gain of reactive power PI controller 0.001 0.05
# psspy.change_con(var_ppc_conp+2, i_g)  # Integral gain of reactive power PI controller 0.015  0.4
# psspy.change_con(var_ppc_conp+23, 0.4)  # Integral gain of reactive power PI controller 0.015  0.4
# psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",2, 0.002)
# psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",3, 0.3)


# psspy.change_con(var_ppc_conp+4, 0.5)
# psspy.change_con(var_ppc_conp+5,-0.5)
# psspy.change_con(var_ppc_conp+22,0.005) #Voltage control deadband in p.u 0.003
# psspy.change_con(var_ppc_conp+23,0.50)  # Voltage control droop in %
#
# psspy.change_con(var_ppc_conp+27,20000) #Voltage control deadband in p.u 0.003
# psspy.change_con(var_ppc_conp+28,28000)  # Voltage control droop in %  5
# #
# psspy.change_con(var_ppc_conp+25,0.80)  #Voltage threshold for fault detection in p.u.
# psspy.change_con(var_ppc_conp+26,1.20)  #Voltage threshold for overV fault detection in p.u.

# psspy.change_con(var_ppc_conp+1,0.05)  #Proportional gain of reactive power PI controller 0.001
# psspy.change_con(var_ppc_conp+2,0.40)  # Integral gain of reactive power PI controller 0.015

# psspy.change_con(var_ppc_conp+9, 1.0)  #Reactive power inverters do not reduce active power

# psspy.change_con(var_inv1_con+15,0.85)	# Not Final #LVRT
# psspy.change_con(var_inv1_con+16,0.10)	# Not Final  #LVRT

# psspy.change_con(var_inv1_con+12,-0.35)	# Inverter Con, Looks good PQ curve Qmin -0.09
# psspy.change_con(var_inv1_con+13, 0.59)	# Inverter Con, Looks good PQ curve Qmax 0.46

# start simulation


psspy.strt_2([0,0], OutputFilePath)
psspy.run(0, 1, 1000,  1, 0)
psspy.change_var(var_ppc_setp+68, 1.05)
psspy.change_var(var_ppc_setp+10, 85)
psspy.run(0, 2,  1000,  1, 0)
psspy.change_var(var_ppc_setp+68, 1.03)
psspy.run(0, 5, 1000,  1, 0)
psspy.change_var(var_ppc_setp+68, 1.08)
psspy.run(0, 10, 1000,  1, 0)
psspy.change_var(var_ppc_setp+68, 1.03)
psspy.run(0, 15, 1000,  1, 0)

# psspy.change_var(var_ppc_setp+68,1.01)
# psspy.run(0, 35, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,0.985)
#
# psspy.run(0, 45, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.035)
# psspy.run(0, 55, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,0.985)
#
# psspy.run(0,65,1000,1,0)
# # psspy.change_var(var_ppc_setp+68,1.05)
# psspy.change_var(var_ppc_setp+10,80)
#
# psspy.run(0, 5,  1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.097)
# psspy.run(0, 15, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.05)
#
# psspy.run(0, 25, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.00)
# psspy.run(0, 35, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.025)
#
# psspy.run(0, 45, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.075)
# psspy.run(0, 55, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+68,1.025)
#
# psspy.run(0,65,1000,1,0)


GraphPath=FigurePath+ClauseName+'/'
if not os.path.exists(GraphPath):
    os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()

TIME=numpy.array(chandata['time'])
FREQ=numpy.array(chandata[1])
V_INV=numpy.array(chandata[2])
V_POC=numpy.array(chandata[3])
# P_INV=numpy.array(chandata[6])*96.8
P_INV=numpy.array(chandata[6])
P_POC=numpy.array(chandata[4])
# Q_INV=numpy.array(chandata[7])*96.8
Q_INV=numpy.array(chandata[7])
Q_POC=numpy.array(chandata[5])
V_SET=numpy.array(chandata[8])
P_SET=numpy.array(chandata[9])

numpy.savetxt(GraphPath +'PSSE Voltage Setpoint.csv', numpy.transpose([TIME,FREQ,V_INV,V_POC,P_INV,P_POC,Q_INV,Q_POC,V_SET,P_SET]), delimiter=',')

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

CurrentFig, CurrentAx = plt.subplots(3, 2, sharex=False, figsize=(20, 15));
CurrentAx[0][0].plot(chandata['time'], P_INV);
CurrentAx[1][0].plot(chandata['time'], Q_INV);
CurrentAx[2][0].plot(chandata['time'], V_INV);
# CurrentAx[0][1].plot(chandata['time'],P_SET,color='green',linestyle='--');
CurrentAx[0][1].plot(chandata['time'], P_POC);
CurrentAx[1][1].plot(chandata['time'], Q_POC);
CurrentAx[2][1].plot(chandata['time'],chandata[8],color='orange',linestyle='--');
CurrentAx[2][1].plot(chandata['time'], V_POC);

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

CurrentAx[0][0].set_ylim([-5, 100])
CurrentAx[1][0].set_ylim([-60, 80])
CurrentAx[2][0].set_ylim([0.8, 1.15])
CurrentAx[0][1].set_ylim([-5, 100])
CurrentAx[1][1].set_ylim([-60, 80])
CurrentAx[2][1].set_ylim([0.9, 1.15])

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
CurrentAx[0][1].legend([r"""WISF P Injection"""])
CurrentAx[1][1].legend([r"""WISF Q Injection"""])
CurrentAx[2][1].legend([r"""WISF PoC Voltage_setpoint""", r"""WISF PoC Voltage"""])
# CurrentAx[2][1].legend([r"""WDSF PoC Voltage"""])

# save_figure_name = GraphPath + "/" +TestName + '-'+str(pp_g)+'_' + str(i_g)+'_' + '.png'
save_figure_name = GraphPath + "/" +TestName +'_' + '.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)