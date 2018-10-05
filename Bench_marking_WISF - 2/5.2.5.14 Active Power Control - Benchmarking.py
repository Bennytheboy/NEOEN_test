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
ClauseName="BM_"
ProgramPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/P_SimulationProgram/"
GridInfoPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/"+"D_"+LoadScenario+"/"
HuaweiModelPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/D_HuaweiModels/"
OutputFilePath=ProgramPath+"SimulationOutput4.outx"
FigurePath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/"
TestName ="active Power_control"

if LoadScenario=="SummerPeakLoad":
    file_name="SummerHi-20171219-153047-34-SystemNormal"
if LoadScenario=="SummerLowLoad":
    file_name="SummerLowNormal-20161225-040047"
if LoadScenario=="SimplifiedSystem":
    file_name="WISF_1.05"


# Initialize
psspy.case(GridInfoPath+file_name+".sav")
# psspy.rstr(GridInfoPath+file_name+".snp")
psspy.resq(GridInfoPath  + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath  + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath+'HWS2000_psse34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_PPC_V13_34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_SB_V7.dll')
psspy.plant_chng_3(500,0,_i,[ 1.05,_f])
psspy.plant_chng_3(1000,0,_i,[ 1.047,_f])
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[0.300,_f, 0.001,0.004,_f,_f,_f,_f])
psspy.machine_data_2(500, r"""1""", [_i, _i, _i, _i, _i, _i],[87, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.two_winding_chng_5(700,800,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,800,_i,_i,1,_i,_i,_i],[_f,_f,_f, 1.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""SS-TF-1""",
r"""YNYN0""")
psspy.machine_chng_2(500,r"""1""",[_i,_i,_i,_i,_i,_i],[_f,0.0,0,0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])

psspy.fnsl([0,0,0,1,0,0,99,0])


# convert load , do not change
psspy.cong(0)
psspy.bus_frequency_channel([1,1000],r"""System frequency""")
ierr=psspy.machine_array_channel([2,4,500],r"""1""",r"""Inverter Terminal Voltage""")
ierr=psspy.voltage_channel([3,-1,-1,800],r"""WISF PoC Voltage""")
psspy.branch_p_and_q_channel([4,-1,-1,800,900],r"""1""",[r"""P Injection""",r"""Q Injection"""])
psspy.branch_p_and_q_channel([6,-1,-1,500,600],r"""1""",[r"""P Injection""",r"""Q Injection"""])
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

# psspy.change_con(var_ppc_conp+1,0.05)
# psspy.change_con(var_ppc_conp+2,0.40)

# psspy.change_con(var_ppc_conp+9, 1.0)
# psspy.change_con(var_ppc_conp+4, 0.6)
# psspy.change_con(var_ppc_conp+5,-0.6)
# psspy.change_con(var_ppc_conp+22,0.001)
# psspy.change_con(var_ppc_conp+23,0.50)
#
# psspy.change_con(var_ppc_conp+25,0.80)
# psspy.change_con(var_ppc_conp+26,1.20)
#
# psspy.change_con(var_ppc_conp+1,0.05)
# psspy.change_con(var_ppc_conp+2,0.40)
#
# psspy.change_con(var_ppc_conp+9, 1.0)
#
# psspy.change_con(var_inv1_con+15,0.85)	# Not Final
# psspy.change_con(var_inv1_con+16,0.10)	# Not Final
#
# psspy.change_con(var_inv1_con+12,-0.35)	# Inverter Con, Looks good
# psspy.change_con(var_inv1_con+13, 0.59)	# Inverter Con, Looks good
#
# psspy.change_con(var_inv2_con+15,0.85)	# Not Final
# psspy.change_con(var_inv2_con+16,0.10)	# Not Final
#
# psspy.change_con(var_inv2_con+12,-0.35)	# Inverter Con, Looks good
# psspy.change_con(var_inv2_con+13, 0.59)	# Inverter Con, Looks good
#
# # start simulation


psspy.strt_2([0,0], OutputFilePath)
psspy.run(0, 1, 1000,  1, 0)
psspy.change_var(var_ppc_setp+68,1.05)
psspy.change_var(var_ppc_setp+10,85)

psspy.run(0,5,  1000,  1, 0)
psspy.change_var(var_ppc_setp+10,68)
psspy.run(0, 55, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,85)

psspy.run(0, 105, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+10,65)
# psspy.run(0, 130, 1000,  1, 0)
# psspy.change_var(var_ppc_setp+10,85)
#
# psspy.run(0,180,1000,1,0)


GraphPath=FigurePath+ClauseName + TestName+'/'
if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()

TIME=numpy.array(chandata['time'])
FREQ=numpy.array(chandata[1])
V_INV=numpy.array(chandata[2])
V_POC=numpy.array(chandata[3])
P_INV=numpy.array(chandata[6])
P_POC=numpy.array(chandata[4])
Q_INV=numpy.array(chandata[7])
Q_POC=numpy.array(chandata[5])
V_SET=numpy.array(chandata[8])
P_SET=numpy.array(chandata[9])

numpy.savetxt(GraphPath +'PSSE Active Power Setpoint.csv', numpy.transpose([TIME,FREQ,V_INV,V_POC,P_INV,P_POC,Q_INV,Q_POC,V_SET,P_SET]), delimiter=',')

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
CurrentAx[0][1].plot(chandata['time'],P_SET,color='green',linestyle='--');
CurrentAx[0][1].plot(chandata['time'], P_POC);
CurrentAx[1][1].plot(chandata['time'], Q_POC);
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

CurrentAx[0][0].set_ylim([0, 120])
CurrentAx[1][0].set_ylim([-60, 80])
CurrentAx[2][0].set_ylim([0.6, 1.4])
CurrentAx[0][1].set_ylim([-5, 100])
CurrentAx[1][1].set_ylim([-100, 120])
CurrentAx[2][1].set_ylim([0.6, 1.4])

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

save_figure_name = GraphPath + "/" +TestName + '-' + '.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)
# raw_input("Press enter to exit...")
# redirect.reset()
