
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
#LoadScenario = "SimplifiedSystem"
ClauseName = "5.2.5.3 Frequency Response_new"
ProgramPath = "F:/"
GridInfoPath = "F:/"
HuaweiModelPath = "F:/"
OutputFilePath = ProgramPath + "5.2.5.3_SimulationOutput_1.outx"
FigurePath = "F:/"



file_name = "NEOEN Western Downs Solar Farm_C3WV_mod"

Disturbance_Load_Amount = numpy.arange(100, 1300, 20)

# Initialize
psspy.read(0, GridInfoPath + file_name + ".raw")
psspy.resq(GridInfoPath + file_name + ".seq")
# psspy.addmodellibrary(GridInfoPath+'dsusr.dll')
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
# psspy.addmodellibrary(GridInfoPath+'GEWTG34.dll')
# psspy.addmodellibrary(GridInfoPath+'SMAPPC_B111_34_IVF111.dll')
# psspy.addmodellibrary(GridInfoPath+'SMASC_C135_34_IVF111.dll')
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])

for i in range(0, len(Disturbance_Load_Amount)):
    # re - initialize
    psspy.read(0, GridInfoPath + file_name + ".raw")
    psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
    psspy.change_plmod_icon(101, r"""1""", r"""HWS2000""", 1, 2)
    psspy.change_plmod_icon(102, r"""1""", r"""HWS2000""", 1, 2)
    psspy.change_plmod_icon(103, r"""1""", r"""HWS2000""", 1, 2)
    psspy.change_plmod_icon(104, r"""1""", r"""HWS2000""", 1, 2)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 45, 50.6)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 46, 600.0)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 47, 51.1)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 48, 120.0)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 49, 52.1)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 51, 53.1)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 53, 54.0)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 55, 49.4)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 56, 600.0)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 57, 48.9)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 58, 120.0)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 59, 46.9)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 61, 45.9)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 63, 44.9)
    psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 65, 43.9)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 45, 50.6)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 46, 600.0)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 47, 51.1)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 48, 120.0)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 49, 52.1)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 51, 53.1)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 53, 54.0)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 55, 49.4)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 56, 600.0)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 57, 48.9)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 58, 120.0)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 59, 46.9)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 61, 45.9)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 63, 44.9)
    psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 65, 43.9)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 45, 50.6)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 46, 600.0)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 47, 51.1)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 48, 120.0)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 49, 52.1)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 51, 53.1)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 53, 54.0)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 55, 49.4)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 56, 600.0)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 57, 48.9)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 58, 120.0)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 59, 46.9)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 61, 45.9)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 63, 44.9)
    psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 65, 43.9)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 45, 50.6)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 46, 600.0)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 47, 51.1)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 48, 120.0)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 49, 52.1)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 51, 53.1)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 53, 54.0)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 55, 49.4)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 56, 600.0)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 57, 48.9)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 58, 120.0)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 59, 46.9)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 61, 45.9)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 63, 44.9)
    psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 65, 43.9)
    #psspy.change_plmod_icon(101, r"""1""", r"""GPMPPC""", 8, 1)
    #psspy.add_plant_model(600, r"""1""", 6, r"""SEXS""", 0, "", 0, [], [], 6, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 1, 0.1)
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 2, 10.0)
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 3, 100.0)
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 4, 0.1)
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 5, -10.0)
    #psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 6, 10.0)
    psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 1, 0.9)
    psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 2, 1)
    psspy.resq(GridInfoPath + file_name + ".seq")
    psspy.load_data_3(600, r"""1""", [_i, _i, _i, _i, _i], [900, 20, _f, _f, _f, _f])  # apply assumption load
    psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])
    for t_var in range(1, 500):
        psspy.change_var(t_var, 0)

    psspy.bus_frequency_channel([1, 400], r"""System frequency""")
    psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
    psspy.voltage_channel([3, -1, -1, 400], r"""WD SF POC Voltage Mag.""")
    psspy.branch_p_and_q_channel([4, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
    ierr = psspy.machine_array_channel([7, 2, 101], r"""1""", r"""Pelec101""")
    ierr = psspy.machine_array_channel([8, 3, 101], r"""1""", r"""Qelec101""")
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
    #psspy.change_var(var_ppc_setp+10,400)
    #psspy.change_var(var_ppc_setp+11,160)
    psspy.run(0, 5, 10000, 20, 0)
    psspy.load_data_3(600, r"""1""", [_i, _i, _i, _i, _i], [Disturbance_Load_Amount[i], _f, _f, _f, _f, _f])
    ##        psspy.load_data_3(28670,r"""2""",[_i,_i,_i,_i,_i],[ Disturbance_Load_Amount[i],_f,_f,_f,_f,_f])
    ##        psspy.load_data_3(28670,r"""3""",[_i,_i,_i,_i,_i],[ Disturbance_Load_Amount[i],_f,_f,_f,_f,_f])

    ##        psspy.run(0, 60, 10000,  20, 0)
    ##        psspy.load_data_3(28670,r"""1""",[_i,_i,_i,_i,_i],[ 20,_f,_f,_f,_f,_f])
    ##        psspy.load_data_3(28670,r"""2""",[_i,_i,_i,_i,_i],[ 20,_f,_f,_f,_f,_f])
    ##        psspy.load_data_3(28670,r"""3""",[_i,_i,_i,_i,_i],[ 20,_f,_f,_f,_f,_f])

    psspy.run(0, 600.000, 10000, 20, 0)

    # start draw curves
    # new folder if necessary
    GraphPath = FigurePath + ClauseName
    if not os.path.exists(GraphPath):

              os.makedirs(GraphPath)

    # read data curves
    chnfobj = dyntools.CHNF(OutputFilePath)
    short_title, chanid, chandata = chnfobj.get_data()
    freq_data = numpy.array(chandata[1])
    p_data = numpy.array(chandata[7])
    q_data = numpy.array(chandata[8])
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
   # CurrentAx[0][1].plot(chandata['time'][0:min(len(chandata[2]) - 1, t_terminate_point + 50)],
    #                 chandata[4][0:min(len(chandata[4]) - 1, t_terminate_point + 50)]);
    CurrentAx[0][1].plot(chandata['time'][0:min(len(chandata[7]) - 1, t_terminate_point + 50)],
                        400 * ( p_data[0:min(len(chandata[7]) - 1, t_terminate_point + 50)]));
    CurrentAx[1][1].plot(chandata['time'][0:min(len(chandata[8]) - 1, t_terminate_point + 50)],
                         160 * (p_data[0:min(len(chandata[8]) - 1, t_terminate_point + 50)]));
    CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
    CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

    CurrentAx[0][0].set_xlim(left=2)
    CurrentAx[1][0].set_xlim(left=2)
    CurrentAx[0][1].set_xlim(left=2)
    CurrentAx[1][1].set_xlim(left=2)

    CurrentAx[0][0].set_ylim([0.8, 2.0])

    value_top = 52;
    value_bottom = 48;

    if max(50 * freq_data + 50) > 50.1:
        value_top = max(50 * freq_data + 50) + 1;
        value_bottom = 49;

    if min(50 * freq_data + 50) < 49.9:
        value_top = 51;
        value_bottom = min(50 * freq_data + 50) - 1;

##        value_top=55
##        value_bottom=45
    CurrentAx[1][0].set_ylim(bottom=value_bottom, top=value_top)
    CurrentAx[0][1].set_ylim([-5, 500])
    CurrentAx[1][1].set_ylim([-180, 180])

    CurrentAx[0][0].set_xlabel(r"""Time/s""")
    CurrentAx[1][0].set_xlabel(r"""Time/s""")
    CurrentAx[0][1].set_xlabel(r"""Time/s""")
    CurrentAx[1][1].set_xlabel(r"""Time/s""")

    CurrentAx[0][0].set_ylabel(r"""Votlage/PU""")
    CurrentAx[1][0].set_ylabel(r"""Frequency/Hz""")
    CurrentAx[0][1].set_ylabel(r"""Power/MW""")
    CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

    CurrentAx[0][0].set_title(r"""Inverter Terminal Voltage""")
    CurrentAx[1][0].set_title(r"""System Frequency""")
    CurrentAx[0][1].set_title(r"""WDSF Active Power Output""")
    CurrentAx[1][1].set_title(r"""WDSF Reactive Power Output""")

    save_figure_name = GraphPath + "/" + GraphFileName + ' Hz.png'
    ##        save_figure_name=GraphPath+"/"+'Frequency Control'+'.png'
    CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
    plt.close(CurrentFig)

raw_input("Press enter to exit...")
redirect.reset()
