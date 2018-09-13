# Import modules
import os, sys
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN;" + os.environ['PATH'])
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSPY27""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27;" + os.environ['PATH'])
import socket
import struct
import time
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

# Set Simulation Path. if on laptop
# LoadScenario = "SimplifiedSystem"
# ClauseName = "5.2.5.11 Frequency Response_report"
# ProgramPath = "C:/NEOEN/P_SimulationScripts/"
# GridInfoPath = "C:/NEOEN/NEM_files/"
# HuaweiModelPath = "C:/NEOEN/Huawei_models/"
# OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
# FigurePath = "C:/NEOEN/R_Results/"

# Set Simulation Path. if on desktop
LoadScenario = "SimplifiedSystem"
ClauseName = "5.2.5.11 Frequency Response_report"
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

Disturbance_Load_Amount = range(0, 400, 50)
# Initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name +".raw")
psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
#psspy.addmodellibrary(GridInfoPath + 'dsusr.dll')
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
#psspy.addmodellibrary(GridInfoPath + 'GEWTG34.dll')
#psspy.addmodellibrary(GridInfoPath + 'SMAPPC_B111_34_IVF111.dll')
#psspy.addmodellibrary(GridInfoPath + 'SMASC_C135_34_IVF111.dll')
psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])

for i in range(0, len(Disturbance_Load_Amount)):

    # re - initialize
    psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
    psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
    psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
    psspy.load_data_3(600, r"""1""", [_i, _i, _i, _i, _i], [300, 20, _f, _f, _f, _f])  # apply assumption load
    psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])
    for t_var in range(1, 500):
        psspy.change_var(t_var, 0)

    psspy.bus_frequency_channel([1, 400], r"""System frequency""")
    psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
    psspy.voltage_channel([3, -1, -1, 400], r"""WDs SF POC Voltage Mag.""")
    psspy.branch_p_and_q_channel([4, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
    ierr = psspy.machine_array_channel([7, 2, 101], r"""1""", r"""Pelec 101""")
    ierr = psspy.machine_array_channel([8, 3, 101], r"""1""", r"""Qelec 101""")
    [ierr, var_ppc_conp] = psspy.mdlind(101, '1', 'EXC', 'CON')
    [ierr, var_ppc_setp] = psspy.mdlind(101, '1', 'EXC', 'VAR')
    [ierr, var_ppc_mode] = psspy.mdlind(101, '1', 'EXC', 'ICON')
    [ierr, var_inv_con] = psspy.mdlind(101, '1', 'GEN', 'CON')
    [ierr, var_inv_var] = psspy.mdlind(101, '1', 'GEN', 'VAR')

    # convert load , do not change
    psspy.cong(0)

    # start simulation
    psspy.strt_2([0, 0], OutputFilePath)
    psspy.run(0, 1, 10000, 20, 0)
    psspy.load_data_3(600, r"""1""", [_i, _i, _i, _i, _i], [Disturbance_Load_Amount[i], _f, _f, _f, _f, _f])
    psspy.run(0, 10, 10000, 20, 0)
    psspy.load_data_3(600, r"""1""", [_i, _i, _i, _i, _i], [300, _f, _f, _f, _f, _f])
    psspy.run(0, 200, 10000, 20, 0)

    # start draw curves
    # new folder if necessary
    GraphPath = FigurePath + ClauseName
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

    for t_terminate_point in range(0, len(chandata[4])):
        if chandata[4][t_terminate_point] < 1:
            break

    GraphFileName = str(round(50 * (1 + freq_data[t_terminate_point - 50]), 1))

    CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
    CurrentAx[0][0].plot(chandata['time'][0:min(len(chandata[2]) - 1, t_terminate_point + 50)],
                         chandata[2][0:min(len(chandata[2]) - 1, t_terminate_point + 50)]);
    CurrentAx[1][0].plot(chandata['time'][0:min(len(chandata[2]) - 1, t_terminate_point + 50)],
                         50 * (1 + freq_data[0:min(len(chandata[1]) - 1, t_terminate_point + 50)]));
    CurrentAx[0][1].plot(chandata['time'][0:min(len(chandata[2]) - 1, t_terminate_point + 50)],
                         chandata[4][0:min(len(chandata[4]) - 1, t_terminate_point + 50)]);
    CurrentAx[1][1].plot(chandata['time'][0:min(len(chandata[2]) - 1, t_terminate_point + 50)],
                         chandata[5][0:min(len(chandata[5]) - 1, t_terminate_point + 50)]);

    CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

    CurrentAx[0][0].set_xlim(2, 60)
    CurrentAx[1][0].set_xlim(2, 60)
    CurrentAx[0][1].set_xlim(2, 60)
    CurrentAx[1][1].set_xlim(2, 60)

    CurrentAx[0][0].set_ylim([0.8, 1.2])

    value_top = 52;
    value_bottom = 48;

    ##        if max(50*freq_data+50)>50.1:
    ##            value_top=max(50*freq_data+50)+1;
    ##            value_bottom=49;

    ##        if min(50*freq_data+50)<49.9:
    ##            value_top=51;
    ##            value_bottom=min(50*freq_data+50)-1;

    ##        value_top=55
    ##        value_bottom=45
    CurrentAx[1][0].set_ylim(bottom=value_bottom, top=value_top)
    CurrentAx[0][1].set_ylim([-5, 500])
    CurrentAx[1][1].set_ylim([-200, 200])

    CurrentAx[0][0].set_xlabel(r"""Time/s""")
    CurrentAx[1][0].set_xlabel(r"""Time/s""")
    CurrentAx[0][1].set_xlabel(r"""Time/s""")
    CurrentAx[1][1].set_xlabel(r"""Time/s""")

    CurrentAx[0][0].set_ylabel(r"""Voltage/PU""")
    CurrentAx[1][0].set_ylabel(r"""Frequency/Hz""")
    CurrentAx[0][1].set_ylabel(r"""Power/MW""")
    CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

    CurrentAx[0][0].set_title(r"""Inverter Terminal Voltage""")
    CurrentAx[1][0].set_title(r"""System Frequency""")
    CurrentAx[0][1].set_title(r"""WDs SF Active Power Output""")
    CurrentAx[1][1].set_title(r"""WDs SF Reactive Power Output""")

    save_figure_name = GraphPath + "/" + str(Disturbance_Load_Amount[i])+ 'Frequency Reponse (Overfrequency Derating).png'
    ##        save_figure_name=GraphPath+"/"+'Frequency Control'+'.png'
    CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
    plt.close(CurrentFig)

raw_input("Press enter to exit...")
redirect.reset()
