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
ClauseName = "5.2.5.4 Voltage Response"
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
ActivePowerSetpoint = range(0, 101, 50)
ReactivePowerSetpoint = [-40, 60]
vref = numpy.arange(0.7, 1.3, 0.05)

# Initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])

for i in range(0, len(ActivePowerSetpoint)):
    for j in range(0, len(ReactivePowerSetpoint)):
        for k in range(0, len(vref)):
            # re - initialize
            psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
            psspy.resq(GridInfoPath + LoadScenario + "/" + file_name + ".seq")
            psspy.dyre_new([1, 1, 1, 1], GridInfoPath + LoadScenario + "/" + file_name + ".dyr", "", "", "")
            psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [ActivePowerSetpoint[i] , _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f])
            psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, ReactivePowerSetpoint[j] , _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f, _f])
            psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, _f, ReactivePowerSetpoint[j], 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f,
                                  _f])
            psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [ActivePowerSetpoint[i], _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f])
            psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, ReactivePowerSetpoint[j], _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f, _f])
            psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, _f, ReactivePowerSetpoint[j], 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f,
                                  _f])
            psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [ActivePowerSetpoint[i] , _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f])
            psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, ReactivePowerSetpoint[j], _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f, _f])
            psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, _f, ReactivePowerSetpoint[j], 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f,
                                  _f])
            psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [ActivePowerSetpoint[i], _f, _f, _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f])
            psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, ReactivePowerSetpoint[j], _f, 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f, _f])
            psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [_f, _f, _f, ReactivePowerSetpoint[j], 120, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                  _f,
                                  _f])
            psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])

            # convert load , do not change
            psspy.cong(0)
            psspy.conl(0, 1, 1, [0, 0], [0.0, 0.0, 0.1, 0.0])
            psspy.conl(0, 1, 2, [0, 0], [0.0, 0.0, 0.1, 0.0])
            psspy.conl(0, 1, 3, [0, 0], [0.0, 0.0, 0.1, 0.0])
            psspy.ordr(0)
            psspy.fact()
            psspy.tysl(0)

            # psspy.add_plant_model(600, r"""1""", 6, r"""SEXS""", 0, "", 0, [], [], 6, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            # psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 1, 0.1)
            # psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 2, 10.0)
            # psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 3, 50.0)
            # psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 4, 0.05)
            # psspy.change_plmod_con(600, r"""1""", r"""SEXS""", 6, 2.5)
            psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 1, 0.9)
            psspy.change_plmod_con(600, r"""1""", r"""GENCLS""", 2, 1)
            # tune the controllers
            t_q=0.569
            psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 5, 0.5)
            psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 5, -0.5)
            psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 13, -t_q)
            psspy.change_plmod_con(101, r"""1""", r"""HWS2000""", 14, t_q)
            psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 13, -t_q)
            psspy.change_plmod_con(102, r"""1""", r"""HWS2000""", 14, t_q)
            psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 13, -t_q)
            psspy.change_plmod_con(103, r"""1""", r"""HWS2000""", 14, t_q)
            psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 13, -t_q)
            psspy.change_plmod_con(104, r"""1""", r"""HWS2000""", 14, t_q)
            psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 23, 0.001)  # QV droop deadband
            psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 24, 0.004)  # QV droop
            psspy.change_plmod_icon(101, r"""1""", r"""GPMPPC""", 4, 2)   # kVar control =0, PF control = 1, Droop Control = 2, Voltage Control = 3
            psspy.change_plmod_con(101, r"""1""", r"""GPMPPC""", 10, 1.0)

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
            psspy.voltage_channel([3, -1, -1, 400], r"""WD SF POC Voltage Mag.""")
            psspy.branch_p_and_q_channel([4, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
            psspy.branch_p_and_q_channel([6, -1, -1, 101, 111], r"""1""", [r"""P Injection""", r"""Q Injection"""])
            # psspy.machine_array_channel([7, 2, 101], r"""1""", r"""Pelec 100""")
            # psspy.machine_array_channel([8, 3, 101], r"""1""", r"""Qelec 100""")
 #           ierr = psspy.state_channel([9, var_inv_stt + 6], r"""Inverter Voltage Measurement""")

            # start simulation
            psspy.strt_2([0, 0], OutputFilePath)
            psspy.run(0, 1, 1000, 1, 0)
            psspy.run(0, 5, 1000, 1, 0)
            psspy.two_winding_chng_5(500, 46660, r"""1""", [_i, _i, _i, _i, _i, _i, _i, _i, 500, _i, _i, 0, _i, _i, _i],
                                     [_f, _f, _f, _f, _f, _f, vref[k], _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                      _f], [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], "", "")
            psspy.run(0, 20, 1000, 1, 0)

                        # start draw curves
                        # new folder if necessary
            if ActivePowerSetpoint[i] == 0:
                PName = r"""P = 0%""";
            if ActivePowerSetpoint[i] == 50:
                PName = r"""P = 50%""";
            if ActivePowerSetpoint[i] == 100:
                PName = r"""P = 100%""";
            if ReactivePowerSetpoint[j] == 60:
                QName = r"""Q = Max"""
            if ReactivePowerSetpoint[j] == -40:
                QName = r"""Q = Min"""

            GraphPath = FigurePath + ClauseName + '/' + PName + ' ' + QName
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
            mpl.rcParams['legend.loc'] = 'lower center'
            mpl.rcParams['legend.numpoints'] = 3
            mpl.rcParams['legend.fontsize'] = 'small'

            v_inv_u = 1.4
            v_inv_l = 0.4
            v_poc_u = 1.4
            v_poc_l = 0.4
            p_inv_u = 150
            p_inv_l = -50
            p_poc_u = 450
            p_poc_l = -100
            q_inv_u = 80
            q_inv_l = -80
            q_poc_u = 300
            q_poc_l = -300


            major_ticks_v     = numpy.arange(v_inv_l, v_inv_u, 0.2)
            minor_ticks_v     = numpy.arange(v_inv_l, v_inv_u, 0.05)
            major_ticks_p_inv = numpy.arange(p_inv_l, p_inv_u, 50)
            minor_ticks_p_inv = numpy.arange(p_inv_l, p_inv_u, 25)
            major_ticks_q_inv = numpy.arange(q_inv_l, q_inv_u, 20)
            minor_ticks_q_inv = numpy.arange(q_inv_l, q_inv_u, 10)

            major_ticks_p_poc = numpy.arange(p_poc_l, p_poc_u, 150)
            minor_ticks_p_poc = numpy.arange(p_poc_l, p_poc_u, 50)
            major_ticks_q_poc = numpy.arange(q_poc_l, q_poc_u, 100)
            minor_ticks_q_poc = numpy.arange(q_poc_l, q_poc_u, 50)


            CurrentFig, CurrentAx = plt.subplots(2, 3, sharex=False, figsize=(20, 15));
            CurrentAx[0][0].plot(chandata['time'], chandata[2]);
            ##            CurrentAx[0][0].plot(chandata['time'],chandata[9],linestyle='--',color='coral');
            CurrentAx[0][1].plot(chandata['time'], chandata[6]);
            CurrentAx[0][2].plot(chandata['time'], chandata[7]);
            CurrentAx[1][0].plot(chandata['time'], chandata[3]);
            CurrentAx[1][1].plot(chandata['time'], chandata[4]);
            CurrentAx[1][2].plot(chandata['time'], chandata[5]);

            CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
            CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
            CurrentAx[0][2].tick_params(axis='both', which='both', labelsize=24)
            CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
            CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)
            CurrentAx[1][2].tick_params(axis='both', which='both', labelsize=24)

            CurrentAx[0][0].set_xlim([0, 30])
            CurrentAx[0][1].set_xlim([0, 30])
            CurrentAx[0][2].set_xlim([0, 30])
            CurrentAx[1][0].set_xlim([0, 30])
            CurrentAx[1][1].set_xlim([0, 30])
            CurrentAx[1][2].set_xlim([0, 30])

            CurrentAx[0][0].set_ylim([v_inv_l, v_inv_u])
            CurrentAx[0][1].set_ylim([p_inv_l, p_inv_u])
            CurrentAx[0][2].set_ylim([q_inv_l, q_inv_u])
            CurrentAx[1][0].set_ylim([v_poc_l, v_poc_u])
            CurrentAx[1][1].set_ylim([p_poc_l, p_poc_u])
            CurrentAx[1][2].set_ylim([q_poc_l, q_poc_u])

            CurrentAx[0][0].set_xlabel(r"""Time/s""")
            CurrentAx[0][1].set_xlabel(r"""Time/s""")
            CurrentAx[0][2].set_xlabel(r"""Time/s""")
            CurrentAx[1][0].set_xlabel(r"""Time/s""")
            CurrentAx[1][1].set_xlabel(r"""Time/s""")
            CurrentAx[1][2].set_xlabel(r"""Time/s""")

            CurrentAx[0][0].set_ylabel(r"""Votlage/PU""")
            CurrentAx[0][1].set_ylabel(r"""Power/MW""")
            CurrentAx[0][2].set_ylabel(r"""Power/MVar""")
            CurrentAx[1][0].set_ylabel(r"""Votlage/PU""")
            CurrentAx[1][1].set_ylabel(r"""Power/MW""")
            CurrentAx[1][2].set_ylabel(r"""Power/MVar""")

            CurrentAx[0][0].legend(["Inverter Terminal Voltage"])
            CurrentAx[0][1].legend(["Inverter P Output"])
            CurrentAx[0][2].legend(["Inverter Q Output"])
            CurrentAx[1][0].legend(["WDSF PoC Voltage"])
            CurrentAx[1][1].legend(["WDSF P Output"])
            CurrentAx[1][2].legend(["WDSF Q Output"])

            # CurrentAx[0][0].set_xticks(major_ticks_v)
            # CurrentAx[0][0].set_xticks(minor_ticks_v, minor=True)
            CurrentAx[0][0].set_yticks(major_ticks_v)
            CurrentAx[0][0].set_yticks(minor_ticks_v, minor=True)
            CurrentAx[0][0].grid(which='minor', alpha=0.4)
            CurrentAx[0][0].grid(which='major', alpha=0.8)

            CurrentAx[1][0].set_yticks(major_ticks_v)
            CurrentAx[1][0].set_yticks(minor_ticks_v, minor=True)
            CurrentAx[1][0].grid(which='minor', alpha=0.4)
            CurrentAx[1][0].grid(which='major', alpha=0.8)

            CurrentAx[0][1].set_yticks(major_ticks_p_inv)
            CurrentAx[0][1].set_yticks(minor_ticks_p_inv, minor=True)
            CurrentAx[0][1].grid(which='minor', alpha=0.4)
            CurrentAx[0][1].grid(which='major', alpha=0.8)

            CurrentAx[1][1].set_yticks(major_ticks_p_poc)
            CurrentAx[1][1].set_yticks(minor_ticks_p_poc, minor=True)
            CurrentAx[1][1].grid(which='minor', alpha=0.4)
            CurrentAx[1][1].grid(which='major', alpha=0.8)

            CurrentAx[0][2].set_yticks(major_ticks_q_inv)
            CurrentAx[0][2].set_yticks(minor_ticks_q_inv, minor=True)
            CurrentAx[0][2].grid(which='minor', alpha=0.4)
            CurrentAx[0][2].grid(which='major', alpha=0.8)

            CurrentAx[1][2].set_yticks(major_ticks_q_poc)
            CurrentAx[1][2].set_yticks(minor_ticks_q_poc, minor=True)
            CurrentAx[1][2].grid(which='minor', alpha=0.4)
            CurrentAx[1][2].grid(which='major', alpha=0.8)

            disturbance_hi = max(0, max(chandata[2][5010:6000]) - 1);
            disturbance_lo = max(0, 1 - min(chandata[2][5010:6000]));
            if disturbance_hi > disturbance_lo:
                disturbance = 1 + disturbance_hi
            else:
                disturbance = 1 - disturbance_lo

            save_figure_name = GraphPath + "/" + 'P=' + str(ActivePowerSetpoint[i]) + ' Q=' + str(
                ReactivePowerSetpoint[j]) + ' V=' + str(round(disturbance, 2)) + '.png'
            CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
            plt.close(CurrentFig)
            ### save a scv file for each graph ###
            t_data=numpy.array(chandata['time'])

            V_inv_data=numpy.array(chandata[2])
            P_inv_data=numpy.array(chandata[6])
            Q_inv_data=numpy.array(chandata[7])
            V_poc_data=numpy.array(chandata[3])
            P_POC_data=numpy.array(chandata[4])
            Q_POC_data=numpy.array(chandata[5])

            ResultFile = open(GraphPath + "/" + 'P=' + str(ActivePowerSetpoint[i]) + ' Q=' + str(
                ReactivePowerSetpoint[j]) + ' V=' + str(round(disturbance, 2)) + '.csv', 'w');
            ResultFile.write('time, inverter_V, POC_V, P_inv, P_injection, Q_inv, Q_injection')
            ResultFile.write('\n')
            for t in range(0, len(t_data)):
                ResultFile.write(str(t_data[t]) + ','+str(V_inv_data[t]) +',' +str(V_poc_data[t])+
                                 ',' + str(P_inv_data[t]) + ',' +str(P_POC_data[t])+ ','+ str(Q_inv_data[t])+ ','+ str(Q_POC_data[t])+',')
                ResultFile.write('\n')
            ResultFile.close()



raw_input("Press enter to exit...")
redirect.reset()
