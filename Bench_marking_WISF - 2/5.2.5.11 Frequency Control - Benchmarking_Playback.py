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
ClauseName="Benchmarking"
ProgramPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/P_SimulationProgram/"
GridInfoPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/"+"D_"+LoadScenario+"/"
HuaweiModelPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/D_HuaweiModels/"
OutputFilePath=ProgramPath+"SimulationOutput4_pb.outx"
FigurePath = "F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results_2/"
TestName = "Frequency_resp"


if LoadScenario=="SummerPeakLoad":
    file_name="SummerHi-20171219-153047-34-SystemNormal"
if LoadScenario=="SummerLowLoad":
    file_name="SummerLowNormal-20161225-040047"
if LoadScenario=="SimplifiedSystem":
    file_name="WISF_1.05_pb_2"


# Initialize
# Initialize
psspy.case(GridInfoPath+file_name+".sav")
# psspy.rstr(GridInfoPath+file_name+".snp")
psspy.resq(GridInfoPath  + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath  + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath+'HWS2000_psse34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_PPC_V13_34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_SB_V7.dll')
psspy.addmodellibrary(r"""F:\PosDoc Projects\11_Industrial Projects\HuaWei\WISF\D_SimplifiedSystem\plbvfu1_v33.dll""")
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[0.3,_f, 0.001,0.004,_f,_f,_f,_f])
psspy.plant_chng_3(500,0,_i,[ 1.05,_f])
psspy.plant_chng_3(1000,0,_i,[ 1.045,_f])
psspy.machine_data_2(500, r"""1""", [_i, _i, _i, _i, _i, _i],[85, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.two_winding_chng_5(700,800,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,800,_i,_i,1,_i,_i,_i],[_f,_f,_f, 1.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""SS-TF-1""",
r"""YNYN0""")
psspy.machine_chng_2(500,r"""1""",[_i,_i,_i,_i,_i,_i],[_f,0.0,0,0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.load_data_3(1000,r"""1""",[_i,_i,_i,_i,_i],[1000,20,_f,_f,_f,_f])	# apply assumption load
psspy.fnsl([0,0,0,1,1,1,99,0])

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

ierr=psspy.var_channel([8,var_ppc_setp+68],"Voltage Setpoint")
ierr=psspy.var_channel([9,var_ppc_setp+10],"Active Power Setpoint")

#
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
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 9, [40320, 40340, 40350, 40970, 40980, 40990, 41050, 41071, 41120], 0, [], 0,
           [])
psspy.conl(1, 0, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.bsys(0, 0, [0.4, 500.], 0, [], 0, [], 0, [], 0, [])

psspy.strt_2([0,0], OutputFilePath)
psspy.run(0, 1, 10000,  20, 0)
psspy.change_var(var_ppc_setp + 68, 1.05)
psspy.change_var(var_ppc_setp+10,85)
# psspy.run(0, 5, 10000,  20, 0)
# # psspy.load_data_3(1000,r"""1""",[_i,_i,_i,_i,_i],[ 550,_f,_f,_f,_f,_f])
# psspy.run(0, 15, 10000,  20, 0)
# # psspy.load_data_3(1000,r"""1""",[_i,_i,_i,_i,_i],[ 950,_f,_f,_f,_f,_f])
psspy.run(0, 25, 10000,  20, 0)
# psspy.load_data_3(1000,r"""1""",[_i,_i,_i,_i,_i],[ 800,_f,_f,_f,_f,_f])
# psspy.run(0, 60, 10000,  20, 0)


# start draw curves
# new folder if necessary
GraphPath=FigurePath+ClauseName + TestName+'/'
if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()
freq_data=numpy.array(chandata[1])

# set figure preference
mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['axes.grid']='on'

mpl.rcParams['font.size'] = 24

mpl.rcParams['lines.linewidth'] = 3.0

mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'small'

for t_terminate_point in range(0,len(chandata[4])):
    if chandata[4][t_terminate_point]<1:
        break

GraphFileName=str(round(50*(1+freq_data[t_terminate_point-50]),1))

CurrentFig, CurrentAx = plt.subplots(2,2,sharex=False, figsize=(20,15));
CurrentAx[0][0].plot(chandata['time'][0:min(len(chandata[2])-1,t_terminate_point+50)],chandata[2][0:min(len(chandata[2])-1,t_terminate_point+50)]);
CurrentAx[1][0].plot(chandata['time'][0:min(len(chandata[2])-1,t_terminate_point+50)],50*(1+freq_data[0:min(len(chandata[1])-1,t_terminate_point+50)]));
CurrentAx[0][1].plot(chandata['time'][0:min(len(chandata[2])-1,t_terminate_point+50)],chandata[4][0:min(len(chandata[4])-1,t_terminate_point+50)]);
CurrentAx[1][1].plot(chandata['time'][0:min(len(chandata[2])-1,t_terminate_point+50)],chandata[5][0:min(len(chandata[5])-1,t_terminate_point+50)]);

CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

CurrentAx[0][0].set_xlim([0,25])
CurrentAx[1][0].set_xlim([0,25])
CurrentAx[0][1].set_xlim([0,25])
CurrentAx[1][1].set_xlim([0,25])

CurrentAx[0][0].set_ylim([0.8,1.2])

value_top=55;
value_bottom=45;

CurrentAx[1][0].set_ylim(bottom=value_bottom, top=value_top)
CurrentAx[0][1].set_ylim([-5,120])
CurrentAx[1][1].set_ylim([-50,50])

CurrentAx[0][0].set_xlabel(r"""Time/s""")
CurrentAx[1][0].set_xlabel(r"""Time/s""")
CurrentAx[0][1].set_xlabel(r"""Time/s""")
CurrentAx[1][1].set_xlabel(r"""Time/s""")

CurrentAx[0][0].set_ylabel(r"""Votlage/PU""")
CurrentAx[1][0].set_ylabel(r"""Frequency/Hz""")
CurrentAx[0][1].set_ylabel(r"""Power/MW""")
CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

CurrentAx[0][0].legend([r"""Inverter Terminal Voltage"""])
CurrentAx[1][0].legend([r"""System Frequency"""])
CurrentAx[0][1].legend([r"""WISF P Output"""])
CurrentAx[1][1].legend([r"""WISF Q Output"""])

save_figure_name=GraphPath + "/" +TestName + '-2' + '.png'
CurrentFig.savefig(save_figure_name,format='png',dpi=150,bbox_inches='tight')
plt.close(CurrentFig)

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

numpy.savetxt(GraphPath+"/"+'PSSE Frequency Control_2.csv', numpy.transpose([TIME,FREQ,V_INV,V_POC,P_INV,P_POC,Q_INV,Q_POC,V_SET,P_SET]), delimiter=',')

raw_input("Press enter to exit...")
redirect.reset()

