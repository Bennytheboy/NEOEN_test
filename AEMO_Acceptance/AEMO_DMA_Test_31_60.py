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
from math import sqrt

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.
LoadScenario = "AEMO_Accept_simulation"
ClauseName = "Test 31-Test60"
ProgramPath = "F:/NEOEN/AEMO model acceptance testing/"
GridInfoPath = "F:/NEOEN/AEMO model acceptance testing/"
HuaweiModelPath = "F:/NEOEN/AEMO model acceptance testing/"

FigurePath = "F:/NEOEN/AEMO model acceptance testing/R_Results/AEMO_simulation"

if LoadScenario == "SummerPeakLoad":
        file_name = "SummerHi-20171219-153047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SummerLowLoad":
        file_name = "SummerLo-20171226-043047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SimplifiedSystem":
        file_name = "NEOEN Western Downs Solar Farm_C3WV_mod"
if LoadScenario == "AEMO_Accept_simulation":
        file_name = "NEOEN AEMO testing"

#########################################   Read Input List #######################################

# Active Power Setpoint
S = 100.00   # in MVA
ActivePowerSetpoint = [1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                       0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                       1.00, 1.00, 1.00, 1.00, 1.00, 1.00,
                       1.00, 1.00, 1.00, 0.05, 0.05, 0.05,
                       1.00, 1.00, 1.00, 0.05, 0.05, 0.05] # in p.u
ReactivePowerSetpoint = [0.0, 0.3, -0.3, 0.0, 0.3, -0.3,
                         0.0, 0.3, -0.3, 0.0, 0.3, -0.3,
                         0.0, 0.3, -0.3, 0.0, 0.3, -0.3,
                         0.0, 0.3, -0.3, 0.0, 0.3, -0.3,
                         0.0, 0.3, -0.3, 0.0, 0.3, -0.3]  # in P.u.
SCR_31_60 = [5, 5, 5, 3, 3, 3,
             5, 5, 5, 3, 3, 3,
             5, 5, 5, 3, 3, 3,
             3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3]
GXR_31_60 = [3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3,
             10, 10, 10, 10, 10, 10,
             3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3]
fault_time = 0.50  #seconds
u_dip = 0.7
d = 1
step_size = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
             2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
             2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
             1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
             2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
             # ms
acc_factor = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
              0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
# Initialize
psspy.case(GridInfoPath  + file_name +".sav")
#psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name +".raw")
psspy.resq(GridInfoPath  + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')

z_g = [None]*30
r_g = [None]*30
x_g = [None]*30
r_f = [None]*30
z_f = [None]*30
x_f = [None]*30

for test_no in range(0, 30):
    # re - initialize
    psspy.case(GridInfoPath + file_name + ".sav")
    psspy.fdns([1, 0, 0, 1, 1, 1, 0, 0])
    psspy.resq(GridInfoPath + file_name + ".seq")
    psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [ActivePowerSetpoint[test_no] * S, _f, _f, _f, 100, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [_f, _f, ReactivePowerSetpoint[test_no] * S, _f, 100, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [_f, _f, _f, ReactivePowerSetpoint[test_no] * S, 100, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                          _f])
    psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i],
                                    [acc_factor[test_no], _f, 0.001 * step_size[test_no], 0.004, _f, _f, _f, _f])
    ## calculate impedance for POC and fault
    z_g[test_no] = 1/SCR_31_60[test_no]   # grid impedance
    r_g[test_no] = sqrt(z_g[test_no]**2/(GXR_31_60[test_no]**2+1))   #grid r
    x_g[test_no] = GXR_31_60[test_no]*r_g[test_no]   #grid_x
    z_f[test_no] = d*z_g[test_no]*u_dip/(1-u_dip)
    r_f[test_no] = sqrt(z_f[test_no]**2/10)
    x_f[test_no] = 3*r_f[test_no]
    psspy.branch_chng_3(400, 46660, r"""1""", [_i, _i, _i, _i, _i, _i],
                        [r_g[test_no], x_g[test_no], _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                        [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "")
    psspy.fdns([1, 0, 0, 1, 1, 1, 0, 0])
    psspy.bus_frequency_channel([1, 400], r"""System frequency""")
    # psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
    # psspy.voltage_channel([3, -1, -1, 400], r"""WD SF POC Voltage Mag.""")
    psspy.branch_p_and_q_channel([2, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
    # ierr = psspy.machine_array_channel([4, 2, 101], r"""1""", r"""Pelec 101""")
    # ierr = psspy.machine_array_channel([5, 3, 101], r"""1""", r"""Qelec 101""")
    psspy.branch_p_and_q_channel([4, -1,-1, 101, 201], r"""1""", [r"""101_P""", r"""101_Q"""])
    psspy.voltage_and_angle_channel([6, -1, -1, 101], [r"""Inverter Voltage Mag""", r"""Inverter Voltage Ang"""])
    psspy.voltage_and_angle_channel([8, -1, -1, 400], [r"""POC_Voltage Mag""", r"""POC Voltage Ang"""])

    psspy.cong(0)
    psspy.conl(0, 1, 1, [0, 0], [0.0, 0.0, 0.1, 0.0])
    psspy.conl(0, 1, 2, [0, 0], [0.0, 0.0, 0.1, 0.0])
    psspy.conl(0, 1, 3, [0, 0], [0.0, 0.0, 0.1, 0.0])
    psspy.ordr(1)
    psspy.fact()
    psspy.tysl(1)
    #psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 1, 8.0)
    OutputFilePath = ProgramPath + ClauseName + str(test_no)+"_Simulation.outx"
    # start simulation
    psspy.strt_2([0, 0], OutputFilePath)
    psspy.run(0, 2, 500, 1, 1)
    psspy.dist_branch_fault(400, 46660, r"""1""", 3, 275.0, [r_f[test_no], x_f[test_no]])
    test_name = 'Test_' + str(test_no+31)
    psspy.run(0, 2.0 + fault_time, 500, 1, 1)
    psspy.dist_clear_fault(1)
    psspy.run(0, 5, 500, 1, 1)

    # start draw curves
    # new folder if necessary
    GraphPath = FigurePath + ClauseName + '/'
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
    CurrentAx[0][0].plot(chandata['time'], chandata[6]);
    CurrentAx[1][0].plot(chandata['time'], chandata[4]);
    CurrentAx[2][0].plot(chandata['time'], chandata[5]);
    CurrentAx[0][1].plot(chandata['time'], chandata[8]);
    CurrentAx[1][1].plot(chandata['time'], chandata[2]);
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

    CurrentAx[0][0].set_ylim([-0.2, 1.3])
    CurrentAx[1][0].set_ylim([-10, 120])
    CurrentAx[2][0].set_ylim([-60, 60])
    CurrentAx[0][1].set_ylim([-0.2, 1.3])
    CurrentAx[1][1].set_ylim([-10, 120])
    CurrentAx[2][1].set_ylim([-60, 60])

    CurrentAx[0][0].set_xlabel(r"""Time/s""")
    CurrentAx[1][0].set_xlabel(r"""Time/s""")
    CurrentAx[2][0].set_xlabel(r"""Time/s""")
    CurrentAx[0][1].set_xlabel(r"""Time/s""")
    CurrentAx[1][1].set_xlabel(r"""Time/s""")
    CurrentAx[2][1].set_xlabel(r"""Time/s""")

    CurrentAx[0][0].set_ylabel(r"""Eterm/PU""")
    CurrentAx[1][0].set_ylabel(r"""Pgen/PU""")
    CurrentAx[1][0].set_ylabel(r"""Qgen/PU""")
    CurrentAx[0][1].set_ylabel(r"""U_Poc/PU""")
    CurrentAx[1][1].set_ylabel(r"""P_Poc/MW""")
    CurrentAx[2][1].set_ylabel(r"""Q_Poc/MVar""")

    CurrentAx[0][0].set_title(r"""Inverter E_terminal""")
    CurrentAx[1][0].set_title(r"""Inverter P_gen""")
    CurrentAx[2][0].set_title(r"""Inverter Q_gen""")
    CurrentAx[0][1].set_title(r"""WDs SF PoC Voltage""")
    CurrentAx[1][1].set_title(r"""WDs SF Active Power Output""")
    CurrentAx[2][1].set_title(r"""WDs SF Reactive Power Output""")

    save_figure_name = GraphPath + "/" + test_name +  '-' + '.png'
    CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
    plt.close(CurrentFig)

    ###  save a scv file for each graph  ###
    t_data = numpy.array(chandata['time']);
    p_gen_data = numpy.array(chandata[4]);
    q_gen_data = numpy.array(chandata[5]);
    V_inv_data = numpy.array(chandata[6]);
    P_Poc_data = numpy.array(chandata[2]);
    Q_Poc_data = numpy.array(chandata[3]);
    V_poc_data = numpy.array(chandata[8]);
    ResultFile = open(GraphPath + "/" + test_name +  '-' + '.csv', 'w');
    ResultFile.write('time, inverter_V, P_gen, Q_gen, POC_V,  P_injection, Q_injection,')
    ResultFile.write('\n')
    for t in range(0, len(t_data)):
        ResultFile.write(
            str(t_data[t]) + ',' + str(V_inv_data[t]) + ','+ str(p_gen_data[t]) + ','+ str(q_gen_data[t]) + ','
            + str(V_poc_data[t]) + ',' + str(P_Poc_data[t]) + ',' + str(Q_Poc_data[t]) + ',')
        ResultFile.write('\n')
    ResultFile.close()


raw_input("Press enter to exit...")
redirect.reset()