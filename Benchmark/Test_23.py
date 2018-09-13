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

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.
LoadScenario = "SimplifiedSystem"
ClauseName = "Test 23"
testName = "Test 23_Vinv_P1_Q0.1"
ProgramPath = "F:/NEOEN/P_SimulationScripts/"
GridInfoPath = "F:/NEOEN/NEM_files/"
HuaweiModelPath = "F:/NEOEN/Huawei_models/"
OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
FigurePath = "F:/NEOEN/R_Results/"

if LoadScenario == "SummerPeakLoad":
        file_name = "SummerHi-20171219-153047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SummerLowLoad":
        file_name = "SummerLo-20171226-043047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SimplifiedSystem":
        file_name = "NEOEN Western Downs Solar Farm_C3WV_mod"


#########################################   Read Input List #######################################

# Active Power Setpoint
S = 100.00   # in MVA
ActivePowerSetpoint = 1  # in p.u
ReactivePowerSetpoint = 0.1  # in P.u.
vref= 0.95
#vref = numpy.arange(0.6, 1.4, 0.02)

# Initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name +".raw")
psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])
psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [ActivePowerSetpoint * S, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                      _f])
psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint  * S, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                      _f])
psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S , _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                      _f])
psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [ActivePowerSetpoint * S, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, ReactivePowerSetpoint * S, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                     [_f, _f, _f, ReactivePowerSetpoint * S, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                      _f])
# psspy.machine_chng_2(101,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f,_f,_f, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(102,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f,_f,_f, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(103,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f,_f,_f, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(104,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f, 10.8,_f, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(104,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f,_f, 10.8, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(103,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f, 10.8, 10.8, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(102,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f,_f, 10.8, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(101,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f, 10.8, 10.8, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
# psspy.machine_chng_2(102,r"""1""",[_i,_i,_i,_i,_i,_i],[ 108.0,_f, 10.8,_f, 120.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])
psspy.add_plant_model(600, r"""1""", 6, r"""SEXS""", 0, "", 0, [], [], 6, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 1, 0.1)
psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 2, 10.0)
psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 3, 200.0)
psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 4, 0.05)
psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 6, 2.5)
psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 1, 0.9)
psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 2, 1)

for t_var in range(1, 9000):
    psspy.change_var(t_var, 0)

[ierr, var_ppc_conp] = psspy.mdlind(101, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(101, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(101, '1', 'EXC', 'ICON')
[ierr, var_inv_con] = psspy.mdlind(101, '1', 'GEN', 'CON')
[ierr, var_inv_var] = psspy.mdlind(101, '1', 'GEN', 'VAR')
[ierr, var_inv_stt] = psspy.mdlind(101, '1', 'GEN', 'STATE')
psspy.bus_frequency_channel([1, 400], r"""System frequency""")
psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
#psspy.machine_array_channel([2, 4, 101],r"""1""", r"""Inverter Voltage Mag.""")
psspy.voltage_channel([3, -1, -1, 400], r"""WD SF POC Voltage Mag.""")
psspy.branch_p_and_q_channel([4, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
ierr = psspy.machine_array_channel([7, 2, 101], r"""1""", r"""Pelec 101""")
ierr = psspy.machine_array_channel([8, 3, 101], r"""1""", r"""Qelec 101""")

psspy.cong(0)
psspy.conl(0, 1, 1, [0, 0], [0.0, 0.0, 0.1, 0.0])
psspy.conl(0, 1, 2, [0, 0], [0.0, 0.0, 0.1, 0.0])
psspy.conl(0, 1, 3, [0, 0], [0.0, 0.0, 0.1, 0.0])
psspy.ordr(1)
psspy.fact()
psspy.tysl(1)
psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 1, 0.9)
psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 2, 1)
# start simulation
psspy.strt_2([0, 0], OutputFilePath)
psspy.run(0, 1, 1000, 1, 0)
psspy.run(0, 5, 1000, 1, 0)
psspy.two_winding_chng_5(500,46660,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,500,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,_f, vref,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 10, 1000, 1, 0)
psspy.two_winding_chng_5(500,46660,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,500,_i,_i,0,_i,_i,_i],[_f,_f,_f,_f,_f,_f, 1,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

psspy.run(0, 15, 1000, 1, 0)

# start draw curves
# new folder if necessary
GraphPath = FigurePath + ClauseName  + '/' + testName
if not os.path.exists(GraphPath):
    os.makedirs(GraphPath)

# read data curves
chnfobj = dyntools.CHNF(OutputFilePath)
short_title, chanid, chandata = chnfobj.get_data()
freq_data = numpy.array(chandata[1])

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

CurrentFig, CurrentAx = plt.subplots(3, 2, sharex=False, figsize=(20, 15));
CurrentAx[0][0].plot(chandata['time'], chandata[7]);
CurrentAx[1][0].plot(chandata['time'], chandata[8]);
CurrentAx[2][0].plot(chandata['time'], chandata[2]);
CurrentAx[0][1].plot(chandata['time'], chandata[4]);
CurrentAx[1][1].plot(chandata['time'], chandata[5]);
CurrentAx[2][1].plot(chandata['time'], chandata[3]);

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

CurrentAx[0][0].set_ylim([0, 1.3])
CurrentAx[1][0].set_ylim([-0.5, 0.5])
CurrentAx[2][0].set_ylim([0.85, 1.1])
CurrentAx[0][1].set_ylim([-5, 550])
CurrentAx[1][1].set_ylim([-300, 300])
CurrentAx[2][1].set_ylim([0.9, 1.1])

CurrentAx[0][0].set_xlabel(r"""Time/s""")
CurrentAx[1][0].set_xlabel(r"""Time/s""")
CurrentAx[2][0].set_xlabel(r"""Time/s""")
CurrentAx[0][1].set_xlabel(r"""Time/s""")
CurrentAx[1][1].set_xlabel(r"""Time/s""")
CurrentAx[2][1].set_xlabel(r"""Time/s""")

CurrentAx[0][0].set_ylabel(r"""Pgen/PU""")
CurrentAx[1][0].set_ylabel(r"""Qgen/PU""")
CurrentAx[1][0].set_ylabel(r"""Eterm/PU""")
CurrentAx[0][1].set_ylabel(r"""P_Poc/MW""")
CurrentAx[1][1].set_ylabel(r"""Q_Poc/MVar""")
CurrentAx[2][1].set_ylabel(r"""U_Poc/PU""")

CurrentAx[0][0].set_title(r"""Inverter P_gen""")
CurrentAx[1][0].set_title(r"""Inverter Q_gen""")
CurrentAx[2][0].set_title(r"""Inverter E_terminal""")
CurrentAx[0][1].set_title(r"""WDs SF Active Power Output""")
CurrentAx[1][1].set_title(r"""WDs SF Reactive Power Output""")
CurrentAx[2][1].set_title(r"""WDs SF PoC Voltage""")

save_figure_name = GraphPath + "/" + testName +  '-' + '.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)

###  save a scv file for each graph  ###
t_data = numpy.array(chandata['time']);
p_gen_data = numpy.array(chandata[7]);
q_gen_data = numpy.array(chandata[8]);
V_inv_data = numpy.array(chandata[2]);
P_Poc_data = numpy.array(chandata[4]);
Q_Poc_data = numpy.array(chandata[5]);
V_poc_data = numpy.array(chandata[3]);
ResultFile = open(GraphPath + "/" + testName +  '-' + '.csv', 'w');
ResultFile.write('time, P_gen, Q_gen, inverter_V, P_injection, Q_injection, POC_V')
ResultFile.write('\n')
for t in range(0, len(t_data)):
    ResultFile.write(
        str(t_data[t]) + ',' + str(p_gen_data[t]) + ','+ str(q_gen_data[t]) + ',' +
        str(V_inv_data[t]) + ',' + str(P_Poc_data[t]) + ',' + str(Q_Poc_data[t]) + ',' + str(V_poc_data[t]) + ',')
    ResultFile.write('\n')
ResultFile.close()


raw_input("Press enter to exit...")
redirect.reset()