# Import modules
import os,sys
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN;"+ os.environ['PATH'])
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSPY27""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27;"+ os.environ['PATH'])
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

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

S = 100.00   # in MVA
ActivePowerSetpoint = 1  # in p.u

# Set Simulation Path.  laptop
# LoadScenario="SummerPeakLoad"
# ClauseName="5.2.5.14 Active Power Control_Ramp_8"
# ProgramPath = "C:/NEOEN/P_SimulationScripts/"
# GridInfoPath = "C:/NEOEN/NEM_files/"
# HuaweiModelPath = "C:/NEOEN/Huawei_models/"
# OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
# FigurePath = "C:/NEOEN/R_Results/"

# desktop
LoadScenario="SummerPeakLoad"
ClauseName="5.2.5.14 Active Power Control_Ramp_8"
ProgramPath = "F:/NEOEN/P_SimulationScripts/"
GridInfoPath = "F:/NEOEN/NEM_files/"
HuaweiModelPath = "F:/NEOEN/Huawei_models/"
OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
FigurePath = "F:/NEOEN/R_Results/"

if LoadScenario == "SummerPeakLoad":
        file_name = "SummerHi-20171219-153047-34-SystemNormal_all"
if LoadScenario == "SummerLowLoad":
        file_name = "SummerLo-20171226-043047-34-SystemNormal_all"
if LoadScenario == "SimplifiedSystem":
        file_name = "NEOEN Western Downs Solar Farm_C3WV_mod"

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
[ierr, var_ppc_conp] = psspy.mdlind(101, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(101, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(101, '1', 'EXC', 'ICON')
[ierr, var_inv_con] = psspy.mdlind(101, '1', 'GEN', 'CON')
[ierr, var_inv_var]=psspy.mdlind(101,'1','GEN','VAR')

psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[1.000,_f, 0.001,0.004,_f,_f,_f,_f])

psspy.dscn(30531)
psspy.dscn(36530)
psspy.dscn(37530)
psspy.machine_data_2(30531,r"""12""",[0,_i,_i,_i,_i,_i],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
psspy.machine_data_2(37530,r"""12""",[0,_i,_i,_i,_i,_i],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])

psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S+5, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
#                       _f])
psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S+5, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
#                       _f])
psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S , _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
# psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
#                      [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
#                       _f])
psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])

psspy.fdns([1,0,0,1,0,0,99,0])
psspy.plmod_status(30531,r"""1""",1,0)
psspy.plmod_status(30531,r"""1""",6,0)
psspy.plmod_status(30531,r"""1""",7,0)
psspy.plmod_status(37530,r"""1""",1,0)
psspy.plmod_status(37530,r"""1""",6,0)
psspy.plmod_status(37530,r"""1""",7,0)


# psspy.change_plmod_con(101,r"""1""",r"""GPMPPC""",10, 0.45)
# psspy.change_plmod_con(101,r"""1""",r"""GPMPPC""",28, 20000.)
# psspy.change_plmod_con(101,r"""1""",r"""GPMPPC""",29, 8000.0)
# psspy.change_plmod_icon(101,r"""1""",r"""GPMPPC""",4,3)
# psspy.change_plmod_icon(101,r"""1""",r"""HWS2000""",1,2)

psspy.bus_frequency_channel([1,400],r"""System frequency""")
psspy.voltage_channel([2,-1,-1,101],r"""Inverter Voltage Mag.""")
psspy.voltage_channel([3,-1,-1,400],r"""NEOEN SF POC Voltage Mag.""")
psspy.branch_p_and_q_channel([4,-1,-1,400,46660],r"""1""",[r"""P Injection""",r"""Q Injection"""])
ierr=psspy.machine_array_channel([7,2,101],r"""1""",r"""Pelec 101""")
ierr=psspy.machine_array_channel([8,3,101],r"""1""",r"""Qelec 101""")
ierr=psspy.machine_array_channel([9,2,102],r"""1""",r"""Pelec 102""")
ierr=psspy.machine_array_channel([10,3,102],r"""1""",r"""Qelec 102""")
ierr=psspy.machine_array_channel([11,2,103],r"""1""",r"""Pelec 103""")
ierr=psspy.machine_array_channel([12,3,103],r"""1""",r"""Qelec 103""")
ierr=psspy.machine_array_channel([13,2,104],r"""1""",r"""Pelec 104""")
ierr=psspy.machine_array_channel([14,3,104],r"""1""",r"""Qelec 104""")
psspy.var_channel([15,var_ppc_setp+10],r"""Active Power Setpoint""")


# convert load , do not change
psspy.cong(0)
psspy.bsys(0,0,[0.0, 500.],1,[7],0,[],0,[],0,[])
psspy.bsys(0,0,[0.0, 500.],1,[7],0,[],0,[],0,[])
psspy.conl(0,0,1,[0,0],[ 91.27, 19.36,-126.88, 188.43])
psspy.conl(0,0,2,[0,0],[ 91.27, 19.36,-126.88, 188.43])
psspy.bsys(1,0,[0.0,0.0],0,[],6,[37600,37601,37602,37580,37584,38588],0,[],0,[])
psspy.conl(1,0,2,[0,0],[ 52.75, 58.13, 5.97, 95.52])
psspy.bsys(1,0,[0.0,0.0],0,[],1,[21790],0,[],0,[])
psspy.conl(1,0,2,[0,0],[ 86.63, 25.19, -378.97, 347.97])
psspy.bsys(1,0,[0.0,0.0],0,[],1,[45082],0,[],0,[])
psspy.conl(1,0,2,[0,0],[ 51.36, 59.32,-228.04, 254.01])
psspy.bsys(1,0,[0.0,0.0],0,[],9,[40320,40340,40350,40970,40980,40990,41050,41071,41120],0,[],0,[])
psspy.conl(1,0,2,[0,0],[ 100.0,0.0,0.0, 100.0])
psspy.conl(0,1,2,[0,0],[ 100.0,0.0,-306.02, 303.0])
psspy.conl(0,1,3,[0,0],[ 100.0,0.0,-306.02, 303.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.bsys(0,0,[ 0.4, 500.],0,[],0,[],0,[],0,[])

psspy.change_plmod_con(101,r"""1""",r"""GPMPPC""",16, 8.0)
psspy.change_plmod_icon(101,r"""1""",r"""GPMPPC""",10,1)


# start simulation
psspy.strt_2([0, 0], OutputFilePath)
psspy.run(0, 1, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,400)
#psspy.change_var(var_ppc_setp+11,0)
psspy.run(0, 10, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,350)
psspy.run(0, 20, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,300)
psspy.run(0, 30, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,250)
psspy.run(0, 40, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,200)
psspy.run(0, 50, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,150)
psspy.run(0, 60, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,100)
psspy.run(0, 70, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,50)
psspy.run(0, 80, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,400)
psspy.run(0, 110, 1000,  1, 0)
psspy.change_var(var_ppc_setp+10,50)
psspy.run(0, 140, 1000,  1, 0)


# start draw curves
# new folder if necessary
GraphPath=FigurePath+ClauseName
if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()

# set figure preference
mpl.rcParams['grid.color'] = 'k'
mpl.rcParams['grid.linestyle'] = ':'
mpl.rcParams['grid.linewidth'] = 0.5
mpl.rcParams['axes.grid']='on'

mpl.rcParams['font.size'] = 24

mpl.rcParams['lines.linewidth'] = 3.0

mpl.rcParams['legend.fancybox'] = True
mpl.rcParams['legend.loc'] = 'lower center'
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'medium'

CurrentFig, CurrentAx = plt.subplots(1,1,sharex=False, figsize=(20,8));
CurrentAx.plot(chandata['time'],chandata[4]);
CurrentAx.plot(chandata['time'],chandata[15],color='coral',linestyle='--');
CurrentAx.legend(['Active Power Generated','Active Limitation Commanded'])
CurrentAx.set_ylim([-10,410])
CurrentAx.set_xlabel('Time/s')
CurrentAx.set_ylabel('Power/MW')

save_figure_name=GraphPath+'/'+'Active Power Control.png'
CurrentFig.savefig(save_figure_name,format='png',dpi=150,bbox_inches='tight')
plt.close(CurrentFig)

raw_input("Press enter to exit...")
redirect.reset()
