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
FigurePath = "F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/"
TestName = "Voltage_Dist"

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
psspy.plant_chng_3(1000,0,_i,[ 1.045,_f])
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[0.300,_f, 0.001,0.004,_f,_f,_f,_f])
psspy.machine_data_2(500, r"""1""", [_i, _i, _i, _i, _i, _i],[85, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.two_winding_chng_5(700,800,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,800,_i,_i,1,_i,_i,_i],[_f,_f,_f, 1.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""SS-TF-1""",
r"""YNYN0""")
psspy.machine_chng_2(500,r"""1""",[_i,_i,_i,_i,_i,_i],[_f, 0.0, 0.0, 0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])

psspy.fnsl([0,0,0,1,0,0,99,0])

# convert load , do not change
psspy.cong(0)
psspy.bus_frequency_channel([1,1000],r"""System frequency""")
ierr=psspy.machine_array_channel([2,4,500],r"""1""",r"""Inverter Terminal Voltage""")
ierr=psspy.voltage_channel([3,-1,-1,800],r"""WISF PoC Voltage""")
psspy.branch_p_and_q_channel([4,-1,-1,800,900],r"""1""",[r"""P Injection""",r"""Q Injection"""])
psspy.branch_p_and_q_channel([6,-1,-1,500,600],r"""1""",[r"""Pelec Inverter""",r"""Pelec Inverter"""])
# ierr=psspy.machine_array_channel([6,2,500],r"""1""",r"""Pelec Inverter""")
# ierr=psspy.machine_array_channel([7,3,500],r"""1""",r"""Qelec Inverter""")
[ierr, var_ppc_conp] = psspy.mdlind(500, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(500, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(500, '1', 'EXC', 'ICON')
[ierr, var_inv1_con] = psspy.mdlind(500, '1', 'GEN', 'CON')
[ierr, var_inv1_var]=  psspy.mdlind(500,'1','GEN','VAR')
[ierr, var_inv1_mod]=  psspy.mdlind(500,'1','GEN','ICON')

# psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",26, 0.85)
# # psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",27, 1.15)
# psspy.change_con(var_ppc_conp+1, 0.01)  #Proportional gain of reactive power PI controller 0.001 0.05
# psspy.change_con(var_ppc_conp+2, 0.05)  # Integral gain of reactive power PI controller 0.015  0.4
# psspy.change_con(var_ppc_conp+23, 0.4)  # Integral gain of reactive power PI controller 0.015  0.4
# # psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",2, 0.002)
# # psspy.change_plmod_con(500,r"""1""",r"""GPMPPC""",3, 0.3)
# psspy.change_plmod_icon(500,r"""1""",r"""GPMPPC""",4,2)



psspy.strt_2([0,0], OutputFilePath)
psspy.run(0, 1, 1000,  1, 0)
psspy.change_var(var_ppc_setp+68,1.05)
psspy.change_var(var_ppc_setp+10,85)
# psspy.change_var(var_ppc_setp+11,0)

psspy.run(0, 10, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 0.90/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 15, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 20, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 0.80/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 25, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 30, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 0.70/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 35, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 40, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.15/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 41, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 50, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.25/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 51, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 60, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.35/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
psspy.run(0, 61, 1000,  1, 0)
psspy.two_winding_chng_5(900,950,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,900,_i,_i,0,_i,_i,_i],[_f,_f,_f, 1.05/1.05,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0,70,1000,1,0)


GraphPath=FigurePath+ClauseName+ TestName+'/'
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

numpy.savetxt(GraphPath+'PSSE Voltage Disturbance.csv', numpy.transpose([TIME,FREQ,V_INV,V_POC,P_INV,P_POC,Q_INV,Q_POC]), delimiter=',')


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

CurrentAx[0][0].set_ylim([0, 200])
CurrentAx[1][0].set_ylim([-60, 80])
CurrentAx[2][0].set_ylim([0.6, 1.4])
CurrentAx[0][1].set_ylim([-5, 300])
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
CurrentAx[0][1].legend([r"""WISF P Injection"""])
CurrentAx[1][1].legend([r"""WISF Q Injection"""])
CurrentAx[2][1].legend([r"""WISF PoC Voltage"""])
# CurrentAx[2][1].legend([r"""WDSF PoC Voltage"""])

save_figure_name = GraphPath + "/" +TestName  + '_.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)