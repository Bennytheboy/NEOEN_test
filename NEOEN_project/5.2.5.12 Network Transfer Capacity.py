# File:"C:\Users\chang\Desktop\02 Full System - Copy\01 Summer 2016-17 high SN\5.2.5.12 Network Transfer Capacity.py", generated on THU, APR 12 2018   9:31, release 32.02.04
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
import csv
from datetime import date
import shutil

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.  # CHANG: change path according to PC
today = date.today()
LoadScenario = "SummerPeakLoad"
ClauseName = "5.2.5.12 Impact on Network Capability"
ProgramPath = "F:/NEOEN/P_SimulationScripts/"
GridInfoPath = "F:/NEOEN/NEM_files/" + LoadScenario + "/"
HuaweiModelPath = "F:/NEOEN/Huawei_models/"
OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
FigurePath = "F:/NEOEN/R_Results/" + ClauseName + "/"

if LoadScenario == "SummerPeakLoad":
        file_name = "SummerHi-20171219-153047-34-SystemNormal_all"
if LoadScenario == "SummerLowLoad":
        file_name = "SummerLo-20171226-043047-34-SystemNormal_all"
if LoadScenario == "SimplifiedSystem":
        file_name = "NEOEN Western Downs Solar Farm_C3WV_mod"

#########################################   Read Input List #######################################
Bus_Nam = []
Bus_Num = []
Bus_Vol = []


if os.path.isfile(FigurePath):
   shutil.rmtree(FigurePath)

with open(ProgramPath + "BusNameList.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    Bus_Nam.append(FileData[t_entry][0]);
    Bus_Num.append(int(FileData[t_entry][1]));
    Bus_Vol.append(float(FileData[t_entry][2]));

Power_Flow_Monitor_Start = [];
Power_Flow_Monitor_End = [];
Power_Flow_Monitor_kV = [];
Power_Flow_Monitor_Type = [];  # LN=Line, TX=Transformer, GE=Generator, SH=Shunt, PL=P_Load, QL=Q_Load
Third_Bus_Record = [];  # Only for three-winding transformer
Equipment_ID = [];  # Only for three-winding transformer
with open(ProgramPath + "MonitorLine.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    i = int(FileData[t_entry][0]);
    j = int(FileData[t_entry][1]);
    if i < j:
        Power_Flow_Monitor_Start.append(i);
        Power_Flow_Monitor_End.append(j);
        Power_Flow_Monitor_kV.append(Bus_Vol[Bus_Num.index(i)]);
    if i > j:
        Power_Flow_Monitor_Start.append(j);
        Power_Flow_Monitor_End.append(i);
        Power_Flow_Monitor_kV.append(Bus_Vol[Bus_Num.index(i)]);
    Power_Flow_Monitor_Type.append('LN')
    Third_Bus_Record.append(0);
    Equipment_ID.append('0');

with open(ProgramPath + "MonitorTransformer.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    i = int(FileData[t_entry][0]);
    j = int(FileData[t_entry][1]);
    if i < j:
        Power_Flow_Monitor_Start.append(i);
        Power_Flow_Monitor_End.append(j);
        Power_Flow_Monitor_kV.append('NA');
    if i > j:
        Power_Flow_Monitor_Start.append(j);
        Power_Flow_Monitor_End.append(i);
        Power_Flow_Monitor_kV.append('NA');
    Third_Bus_Record.append(int(FileData[t_entry][2]));
    Equipment_ID.append(FileData[t_entry][3]);
    Power_Flow_Monitor_Type.append('TX')

Fault_Equipment_Start = Power_Flow_Monitor_Start[:];
Fault_Equipment_End = Power_Flow_Monitor_End[:];
Fault_Equipment_kV = Power_Flow_Monitor_kV[:];
Fault_Equipment_Type = Power_Flow_Monitor_Type[:];
with open(ProgramPath + "FaultSource.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    Fault_Equipment_Start.append(int(FileData[t_entry][0]))
    Fault_Equipment_End.append(int(FileData[t_entry][0]))
    Fault_Equipment_kV.append('NA')
    Fault_Equipment_Type.append(FileData[t_entry][1])

#########################################   Start Power Flow Analysis #######################################


Voltage_KV_Record = [[] for i in range(len(Bus_Num))]
Voltage_PU_Record = [[] for i in range(len(Bus_Num))]
P_Flow_Record = [[] for i in range(len(Power_Flow_Monitor_Start))];
S_Flow_Record = [[] for i in range(len(Power_Flow_Monitor_Start))];
Event_Name = [];
P_setpoint = [0, 100, 50, 0]  # CHANG: change this value according to your suggestion from 5.2.5.1 Reactive Power Capability
Q_max_setpoint = [0, 40, 40, 40]  # CHANG: sample : change this value according to your suggestion from 5.2.5.1 Reactive Power Capability
Q_min_setpoint = [0, -40, -40, -40]  # CHANG: sample :change this value according to your suggestion from 5.2.5.1 Reactive Power Capability
InverterCapacity = 120  # CHANG: sample :change this value according to your suggestion from 5.2.5.1 Reactive Power Capability

###### standard power variation
for i in range(0, len(P_setpoint)):
    psspy.read(0, GridInfoPath + file_name)
    ##        psspy.dscn(20022)   # eliminate negative power output by slack bus, does not need to consider outside NSW.

    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint[i], 0, Q_max_setpoint[i], Q_min_setpoint[i], InverterCapacity, 0, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f, _f, _f])
    psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint[i], 0, Q_max_setpoint[i], Q_min_setpoint[i], InverterCapacity, 0, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f, _f, _f])
    psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint[i], 0, Q_max_setpoint[i], Q_min_setpoint[i], InverterCapacity, 0, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f, _f, _f])
    psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint[i], 0, Q_max_setpoint[i], Q_min_setpoint[i], InverterCapacity, 0, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f, _f, _f])
    Event_Name.append('Output=' + str(4 * P_setpoint[i]) + 'MW' + ' ' + 'No Contingency')

    if i <= 1:
        psspy.fdns([1, 0, 0, 1, 1, 1, 99, 0])
    else:
        psspy.fdns([0, 0, 0, 1, 1, 1, 99, 0])

    # Branch Flow Data - Real
    for j in range(0, len(Power_Flow_Monitor_Start)):
        ibus = Power_Flow_Monitor_Start[j];
        jbus = Power_Flow_Monitor_End[j];
        kbus = Third_Bus_Record[j];  # for special three winding tf.
        circuit_id = Equipment_ID[j];  # for special three winding tf.

        rval1M = 0
        rval2M = 0
        rval3M = 0
        rval4M = 0
        rval5M = 0
        ierr, rval1M = psspy.brnmsc(ibus, jbus, '1', 'PCTMVA');
        ierr, rval2M = psspy.brnmsc(ibus, jbus, '2', 'PCTMVA');
        ierr, rval3M = psspy.brnmsc(ibus, jbus, '3', 'PCTMVA');
        ierr, rval4M = psspy.brnmsc(ibus, jbus, '4', 'PCTMVA');
        ierr, rval5M = psspy.wnddat(ibus, jbus, kbus, circuit_id, 'PCTMVA')
        if rval1M == None: rval1M = 0;
        if rval2M == None: rval2M = 0;
        if rval3M == None: rval3M = 0;
        if rval4M == None: rval4M = 0;
        if rval5M == None: rval5M = 0;
        S_Flow_Record[j].append(max([rval1M, rval2M, rval3M, rval4M, rval5M]))

        rval1 = 0;
        rval2 = 0;
        rval3 = 0;
        rval4 = 0;
        rval5 = 0;
        ierr, rval1 = psspy.brnmsc(ibus, jbus, '1', 'P')
        ierr, rval2 = psspy.brnmsc(ibus, jbus, '2', 'P')
        ierr, rval3 = psspy.brnmsc(ibus, jbus, '3', 'P')
        ierr, rval4 = psspy.brnmsc(ibus, jbus, '4', 'P')
        ierr, rval5 = psspy.wnddat(ibus, jbus, kbus, circuit_id, 'MVA')
        if rval1 == None: rval1 = 0;
        if rval2 == None: rval2 = 0;
        if rval3 == None: rval3 = 0;
        if rval4 == None: rval4 = 0;
        if rval5 == None: rval5 = 0;
        P_Flow_Record[j].append(rval1 + rval2 + rval3 + rval4 + rval5)

    for k in range(0, len(Bus_Num)):
        ierr, rval = psspy.busdat(Bus_Num[k], 'KV');
        Voltage_KV_Record[k].append(rval);
        ierr, rval = psspy.busdat(Bus_Num[k], 'PU');
        Voltage_PU_Record[k].append(rval);

    ###### N-1 Contingency
P_setpoint = 100  # CHANG: change this value according to your suggestion from 5.2.5.1 Reactive Power Capability
Q_max_setpoint = 40  # CHANG: change this value according to your suggestion from 5.2.5.1 Reactive Power Capability
Q_min_setpoint = -40  # CHANG: change this value according to your suggestion from 5.2.5.1 Reactive Power Capability

for i in range(0, len(Fault_Equipment_Start)):
    psspy.read(0, GridInfoPath + file_name)
    ##        psspy.dscn(20022)   # eliminate negative generation

    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint, 0, Q_max_setpoint, Q_min_setpoint, InverterCapacity, 0, _f, _f, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f])
    psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint, 0, Q_max_setpoint, Q_min_setpoint, InverterCapacity, 0, _f, _f, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f])
    psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint, 0, Q_max_setpoint, Q_min_setpoint, InverterCapacity, 0, _f, _f, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f])
    psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                         [P_setpoint, 0, Q_max_setpoint, Q_min_setpoint, InverterCapacity, 0, _f, _f, _f, _f, _f, _f,
                          _f, _f, _f, _f, _f])

    psspy.fdns([1, 0, 0, 1, 1, 1, 99, 0])
    if Fault_Equipment_Type[i] == 'LN':  # disconnect line
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Ln Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])] + ' to ' + Bus_Nam[Bus_Num.index(Fault_Equipment_End[i])])
        ierr = psspy.branch_chng_3(Fault_Equipment_Start[i], Fault_Equipment_End[i], r"""1""", [0, _i, _i, _i, _i, _i],
                                   [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                   [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], _s)
    if Fault_Equipment_Type[i] == 'TX' and Third_Bus_Record[i] == 0:  # disconnect 2-winding transformer
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Tx Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])] + ' to ' + Bus_Nam[Bus_Num.index(Fault_Equipment_End[i])])
        ierr, whatever = psspy.two_winding_chng_5(Fault_Equipment_Start[i], Fault_Equipment_End[i], r"""1""",
                                                  [0, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i],
                                                  [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                                   _f, _f, _f, _f], [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f],
                                                  _s, _s)
    if Fault_Equipment_Type[i] == 'TX' and Third_Bus_Record[i] != 0:  # disconnect 3-winding transformer
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Tx Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])] + ' to ' + Bus_Nam[Bus_Num.index(Fault_Equipment_End[i])] + ' ' +
                          Equipment_ID[i])
        ierr, whatever = psspy.three_wnd_imped_chng_4(Fault_Equipment_Start[i], Fault_Equipment_End[i],
                                                      Third_Bus_Record[i], Equipment_ID[i],
                                                      [_i, _i, _i, _i, _i, _i, _i, 0, _i, _i, _i, _i, _i],
                                                      [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                                                       _f], _s, _s)
    if Fault_Equipment_Type[i] == 'GE':  # disconnect generator
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Gen Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])])
        ierr = psspy.machine_chng_2(Fault_Equipment_Start[i], r"""1""", [0, _i, _i, _i, _i, _i],
                                    [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
    if Fault_Equipment_Type[i] == 'SH':  # disconnect switched shunt
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Shunt Capacitor Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])])
        ierr = psspy.switched_shunt_chng_3(Fault_Equipment_Start[i], [_i, _i, _i, _i, _i, _i, _i, _i, _i, _i, 0, _i],
                                           [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f], _s)
    if Fault_Equipment_Type[i] == 'QL':  # clearn Q Load
        Event_Name.append('Output=' + str(4 * P_setpoint) + 'MW' + ' ' + 'Shunt Capacitor Outage - ' + Bus_Nam[
            Bus_Num.index(Fault_Equipment_Start[i])])
        ierr = psspy.load_chng_5(Fault_Equipment_Start[i], r"""1""", [_i, _i, _i, _i, _i, _i, _i],
                                 [_f, 0, _f, 0, _f, 0, _f, _f])

    assert (ierr == 0)
    psspy.fdns([0, 0, 0, 1, 1, 0, 99, 0])

    for j in range(0, len(Power_Flow_Monitor_Start)):
        if Power_Flow_Monitor_Type[j] == 'SH' or Power_Flow_Monitor_Type[j] == 'GE' or Power_Flow_Monitor_Type[
            j] == 'QL':
            continue;
        ibus = Power_Flow_Monitor_Start[j];
        jbus = Power_Flow_Monitor_End[j];
        kbus = Third_Bus_Record[j];  # for special three winding tf.
        circuit_id = Equipment_ID[j];  # for special three winding tf.

        rval1M = 0;
        rval2M = 0;
        rval3M = 0;
        rval4M = 0;
        rval5M = 0
        ierr, rval1M = psspy.brnmsc(ibus, jbus, '1', 'PCTMVA');
        ierr, rval2M = psspy.brnmsc(ibus, jbus, '2', 'PCTMVA');
        ierr, rval3M = psspy.brnmsc(ibus, jbus, '3', 'PCTMVA');
        ierr, rval4M = psspy.brnmsc(ibus, jbus, '4', 'PCTMVA');
        ierr, rval5M = psspy.wnddat(ibus, jbus, kbus, circuit_id, 'PCTMVA')
        if rval1M == None: rval1M = 0;
        if rval2M == None: rval2M = 0;
        if rval3M == None: rval3M = 0;
        if rval4M == None: rval4M = 0;
        if rval5M == None: rval5M = 0;
        S_Flow_Record[j].append(max([rval1M, rval2M, rval3M, rval4M, rval5M]))

        rval1 = 0;
        rval2 = 0;
        rval3 = 0;
        rval4 = 0;
        rval5 = 0;
        ierr, rval1 = psspy.brnmsc(ibus, jbus, '1', 'P')
        ierr, rval2 = psspy.brnmsc(ibus, jbus, '2', 'P')
        ierr, rval3 = psspy.brnmsc(ibus, jbus, '3', 'P')
        ierr, rval4 = psspy.brnmsc(ibus, jbus, '4', 'P')
        ierr, rval5 = psspy.wnddat(ibus, jbus, kbus, circuit_id, 'MVA')
        if rval1 == None: rval1 = 0;
        if rval2 == None: rval2 = 0;
        if rval3 == None: rval3 = 0;
        if rval4 == None: rval4 = 0;
        if rval5 == None: rval5 = 0;
        P_Flow_Record[j].append(rval1 + rval2 + rval3 + rval4 + rval5)

    for k in range(0, len(Bus_Num)):
        ierr, rval = psspy.busdat(Bus_Num[k], 'KV');
        Voltage_KV_Record[k].append(rval);
        ierr, rval = psspy.busdat(Bus_Num[k], 'PU');
        Voltage_PU_Record[k].append(rval);

    #########################################   Write Result To Files #######################################
ResultFile = open(FigurePath + 'VoltageMonitor.csv', 'w');
ResultFile.write('Event \ Bus ' + ',')
for i in range(0, len(Bus_Nam)):
    ResultFile.write(Bus_Nam[i] + ',')
ResultFile.write('\n')

for i in range(0, len(Voltage_PU_Record[0])):
    ResultFile.write(Event_Name[i] + ',')
    for j in range(0, len(Voltage_PU_Record)):
        ResultFile.write(str(Voltage_PU_Record[j][i]) + ',');
    ResultFile.write('\n')
ResultFile.close()

### Write Power Flow - P Result
ResultFile = open(FigurePath + 'P_MW_Monitor.csv', 'w');
ResultFile.write('Event \ Branch' + ',')
for i in range(0, len(Power_Flow_Monitor_Start)):
    if Power_Flow_Monitor_Type[i] == 'SH' or Power_Flow_Monitor_Type[i] == 'QL' or Power_Flow_Monitor_Type[i] == 'GE':
        break;
    ResultFile.write(
        Power_Flow_Monitor_Type[i] + ' ' + Bus_Nam[Bus_Num.index(Power_Flow_Monitor_Start[i])] + ' to ' + Bus_Nam[
            Bus_Num.index(Power_Flow_Monitor_End[i])] + ',')
ResultFile.write('\n')

for i in range(0, len(P_Flow_Record[0])):
    ResultFile.write(Event_Name[i] + ',')
    for j in range(0, len(P_Flow_Record)):
        ResultFile.write(str(P_Flow_Record[j][i]) + ',')
    ResultFile.write('\n')

ResultFile.close()

##### Write Power Flow - Percentage Result
ResultFile = open(FigurePath + 'S_Pct_Monitor.csv', 'w');
ResultFile.write('Event \ Branch ' + ',')
for i in range(0, len(Power_Flow_Monitor_Start)):
    if Power_Flow_Monitor_Type[i] == 'SH' or Power_Flow_Monitor_Type[i] == 'QL' or Power_Flow_Monitor_Type[i] == 'GE':
        break;
    ResultFile.write(
        Power_Flow_Monitor_Type[i] + ' ' + Bus_Nam[Bus_Num.index(Power_Flow_Monitor_Start[i])] + ' to ' + Bus_Nam[
            Bus_Num.index(Power_Flow_Monitor_End[i])] + ',')
ResultFile.write('\n')

for i in range(0, len(S_Flow_Record[0])):
    ResultFile.write(Event_Name[i] + ',')
    for j in range(0, len(S_Flow_Record)):
        ResultFile.write(str(S_Flow_Record[j][i]) + ',')
    ResultFile.write('\n')

ResultFile.close()
