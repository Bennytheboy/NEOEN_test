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
# on laptop
# LoadScenario="SimplifiedSystem"
# ClauseName="Benchmarking"
# ProgramPath="C:/WISF/P_SimulationProgram/"
# GridInfoPath="C:/WISF/"+"D_"+LoadScenario+"/"
# HuaweiModelPath="C:/WISF/D_HuaweiModels/"
# OutputFilePath=ProgramPath+"SimulationOutput4.outx"
# FigurePath="C:/WISF/R_Results/"
# TestName ="5.2.5.5_contingency"

# on desktop
LoadScenario="SimplifiedSystem"
ClauseName="Benchmarking"
ProgramPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/P_SimulationProgram/"
GridInfoPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/"+"D_"+LoadScenario+"/"
HuaweiModelPath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/D_HuaweiModels/"
OutputFilePath=ProgramPath+"SimulationOutput4.outx"
FigurePath="F:/PosDoc Projects/11_Industrial Projects/HuaWei/WISF/R_Results/"
TestName ="5.2.5.5_contingency"

if LoadScenario=="SummerPeakLoad":
    file_name="SummerHi-20171219-153047-34-SystemNormal"
if LoadScenario=="SummerLowLoad":
    file_name="SummerLowNormal-20161225-040047"
if LoadScenario=="SimplifiedSystem":
    file_name="WISF_ADD"


# Initialize
psspy.case(GridInfoPath+file_name+".sav")
# psspy.rstr(GridInfoPath+file_name+".snp")
psspy.resq(GridInfoPath  + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath  + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath+'HWS2000_psse34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_PPC_V13_34.dll')
psspy.addmodellibrary(HuaweiModelPath+'MOD_GPM_SB_V7.dll')
psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[0.300,_f, 0.001,0.004,_f,_f,_f,_f])
psspy.two_winding_chng_5(700,800,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,800,_i,_i,1,_i,_i,_i],[_f,_f,_f, 1.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],r"""WI_MAINTX1""","")
psspy.machine_data_2(500, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [120, _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
psspy.machine_chng_2(500,r"""1""",[_i,_i,_i,_i,_i,_i],[_f,0.0,0.0,0.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f])
psspy.plant_chng_3(500,0,_i,[ 1.05,_f])
psspy.plant_chng_3(1000,0,_i,[ 1.05,_f])
psspy.fnsl([0, 0, 0, 1, 1, 1, 99, 0])

psspy.bus_frequency_channel([1, 1000], r"""System frequency""")
psspy.voltage_channel([2, -1, -1, 500], r"""Inverter Voltage Mag.""")
psspy.voltage_channel([3, -1, -1, 800], r"""WISF POC Voltage Mag.""")
psspy.branch_p_and_q_channel([4, -1, -1, 800, 900], r"""1""", [r"""P Injection""", r"""Q Injection"""])
ierr = psspy.machine_array_channel([6, 2, 500], r"""1""", r"""Pelec Inverter""")
ierr = psspy.machine_array_channel([7, 3, 500], r"""1""", r"""Qelec Inverter""")

[ierr, var_ppc_conp] = psspy.mdlind(500, '1', 'EXC', 'CON')
[ierr, var_ppc_setp] = psspy.mdlind(500, '1', 'EXC', 'VAR')
[ierr, var_ppc_mode] = psspy.mdlind(500, '1', 'EXC', 'ICON')
[ierr, var_inv1_con] = psspy.mdlind(500, '1', 'GEN', 'CON')
[ierr, var_inv1_var]=  psspy.mdlind(500,'1','GEN','VAR')
[ierr, var_inv1_mod]=  psspy.mdlind(500,'1','GEN','ICON')


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
psspy.bsys(1, 0, [0.0, 0.0], 0, [], 9, [40320, 40340, 40350, 40970, 40980, 40990, 41050, 41071, 41120], 0, [], 0, [])
psspy.conl(1, 0, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, -306.02, 303.0])
psspy.ordr(0)
psspy.fact()
psspy.tysl(0)
psspy.bsys(0, 0, [0.4, 500.], 0, [], 0, [], 0, [], 0, [])

# start simulation
psspy.strt_2([0, 0], OutputFilePath)
psspy.run(0, 0.5, 1000, 1, 0)
psspy.change_var(var_ppc_setp + 68, 1.05)
psspy.change_var(var_ppc_setp + 10, 100)
psspy.run(0, 1, 1000, 1, 0)
psspy.change_var(var_ppc_setp + 68, 1.05)
psspy.run(0, 3, 1000, 1, 0)

########################  START LINE FAULT SIMULATION #########################
TimeShift = 0;

for fault_type in range(1, 5):
    for i in range(0, 4):
        if i == 0:
            psspy.branch_chng_3(400, 950, r"""1""", [_i, _i, _i, _i, _i, _i],
                                [_f, 0.204585 * 0.001, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "")
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [0.198244 * 0.00001, _f, _f, _f, _f, _f, _f, _f])
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [_f, 0.818340 * 0.00001, _f, _f, _f, _f, _f, _f])
            fault_time = 0.120
        if i == 1:
            psspy.branch_chng_3(400, 950, r"""1""", [_i, _i, _i, _i, _i, _i],
                                [_f, 0.204585 * 0.33, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "")
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [0.198244 * 0.33, _f, _f, _f, _f, _f, _f, _f])
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [_f, 0.818340 * 0.33, _f, _f, _f, _f, _f, _f])
            fault_time = 0.720
        if i == 2:
            psspy.branch_chng_3(400, 950, r"""1""", [_i, _i, _i, _i, _i, _i],
                                [_f, 0.204585 * 1, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "")
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [0.198244 * 1, _f, _f, _f, _f, _f, _f, _f])
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [_f, 0.818340 * 1, _f, _f, _f, _f, _f, _f])
            fault_time = 0.720
        if i == 3:
            psspy.branch_chng_3(400, 950, r"""1""", [_i, _i, _i, _i, _i, _i],
                                [_f, 0.204585 * 3, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "")
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [0.198244 * 3, _f, _f, _f, _f, _f, _f, _f])
            psspy.seq_branch_data_3(400, 950, r"""1""", _i, [_f, 0.818340 * 3, _f, _f, _f, _f, _f, _f])
            fault_time = 0.720

        psspy.run(0, 5 + TimeShift, 1000, 1, 0)
        if fault_type == 1 :  # three phase
            fault_name = 'ThreePhase'
            psspy.dist_bus_fault(400, 1, 66.0, [0.0, -0.2E+10])
            # fault_time = 0.120

        if fault_type == 2:  # single phase
            psspy.dist_scmu_fault_2([0, 0, 1, 400, _i], [0.0001, 0.0001, 0.0, 0.0])
            fault_name = 'SinglePhase'
            fault_time = 0.720

        if fault_type == 3:  # phase to phase
            psspy.dist_scmu_fault_2([0, 0, 2, 400, _i], [0.0001, 0.0001, 999.0, 999.0])
            fault_name = 'TwoPhase'
            fault_time = 0.720

        if fault_type == 4:  # phase to phase to ground
            psspy.dist_scmu_fault_2([0, 0, 2, 400, _i], [0.0001, 0.0, 0.0001, 0.0])
            fault_name = 'TwoPhaseGround'
            fault_time = 0.720

        psspy.run(0, 5.0 + fault_time + TimeShift, 1000, 1, 0)
        psspy.dist_clear_fault(1)
        psspy.run(0, 10.000 + TimeShift, 1000, 1, 0)

        TimeShift = TimeShift + 5

        GraphPath = FigurePath + ClauseName + fault_name + '/'
        if not os.path.exists(GraphPath):
            os.makedirs(GraphPath)

        # read data curves
        chnfobj = dyntools.CHNF(OutputFilePath)
        short_title, chanid, chandata = chnfobj.get_data()

        TIME = []
        FREQ = []
        V_INV = []
        V_POC = []
        P_INV = []
        P_POC = []
        Q_INV = []
        Q_POC = []

        TIME = numpy.array(chandata['time'])
        FREQ = numpy.array(chandata[1])
        V_INV = numpy.array(chandata[2])
        V_POC = numpy.array(chandata[3])
        P_INV = numpy.array(chandata[6]) * 100
        P_POC = numpy.array(chandata[4])
        Q_INV = numpy.array(chandata[7]) * 100
        Q_POC = numpy.array(chandata[5])

        numpy.savetxt(GraphPath + fault_name +TestName+ 'PSSE Fault.csv', numpy.transpose([TIME, FREQ, V_INV, V_POC, P_INV, P_POC, Q_INV, Q_POC]),
                      delimiter=',')

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

        CurrentAx[0][0].set_ylim([0, 120])
        CurrentAx[1][0].set_ylim([-60, 80])
        CurrentAx[2][0].set_ylim([0.0, 1.4])
        CurrentAx[0][1].set_ylim([-5, 200])
        CurrentAx[1][1].set_ylim([-100, 120])
        CurrentAx[2][1].set_ylim([0.0, 1.4])

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

        save_figure_name = GraphPath +TestName+ fault_name + '-' + '.png'
        CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
        plt.close(CurrentFig)
