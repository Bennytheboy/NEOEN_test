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
import csv

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

# Set Simulation Path.
LoadScenario = "SummerPeakLoad"
ClauseName = "5.2.5.5 Contingency Response"
ProgramPath = "D:/NEOEN/"
GridInfoPath = "D:/NEOEN/"
HuaweiModelPath = "D:/NEOEN/"
OutputFilePath = ProgramPath + "5.2.5.5_SimulationOutput.outx"
FigurePath = "D:/NEOEN/"

if LoadScenario == "SummerPeakLoad":
    file_name = "SummerHi-20171219-153047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SummerLowLoad":
    file_name = "SummerLo-20171226-043047-34-SystemNormal_all_but_DDSF"
if LoadScenario == "SimplifiedSystem":
    file_name = "NEOEN Western Downs Solar Farm_C3WV_mod_T"

Bus_Name = []
Bus_List = []
Bus_Vol = []

with open(ProgramPath + "BusNameList_WV.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    Bus_Name.append(FileData[t_entry][0]);
    Bus_List.append(int(FileData[t_entry][1]));
    Bus_Vol.append(float(FileData[t_entry][2]));

PowerFlow_Monitor_Start_List = [];
PowerFlow_Monitor_End_List = [];
PowerFlow_Monitor_kV = [];
PowerFlow_Monitor_Type = [];  # LN=Line, TX=Transformer, GE=Generator, SH=Shunt, PL=P_Load, QL=Q_Load
Third_Bus_Record = [];  # Only for three-winding transformer
Equipment_ID = [];  # Only for three-winding transformer
with open(ProgramPath + "MonitorLine.csv", 'rb') as t_file:
    FileData = csv.reader(t_file)
    FileData = list(FileData)
for t_entry in range(1, len(FileData)):
    i = int(FileData[t_entry][0]);
    j = int(FileData[t_entry][1]);
    if i < j:
        PowerFlow_Monitor_Start_List.append(i);
        PowerFlow_Monitor_End_List.append(j);
        PowerFlow_Monitor_kV.append(Bus_Vol[Bus_List.index(i)]);
    if i > j:
        PowerFlow_Monitor_Start_List.append(j);
        PowerFlow_Monitor_End_List.append(i);
        PowerFlow_Monitor_kV.append(Bus_Vol[Bus_List.index(i)]);
    PowerFlow_Monitor_Type.append('LN')
    Third_Bus_Record.append(0);
    Equipment_ID.append('0');

PowerFlow_Monitor_Name_List = [];
for i in range(0, len(PowerFlow_Monitor_Start_List)):
    PowerFlow_Monitor_Name_List.append(Bus_Name[Bus_List.index(PowerFlow_Monitor_Start_List[i])] + ' to ' + Bus_Name[Bus_List.index(PowerFlow_Monitor_End_List[i])]);

Branch_Outage_List_Start = PowerFlow_Monitor_Start_List[0:-3]
Branch_Outage_List_End = PowerFlow_Monitor_End_List[0:-3]

EventName = [];
Branch_kV = [];
for i in range(0, len(Branch_Outage_List_Start)):
    EventName.append(Bus_Name[Bus_List.index(Branch_Outage_List_Start[i])] + ' to ' + Bus_Name[Bus_List.index(Branch_Outage_List_End[i])] + ' Fault');

for i in range(0, len(Branch_Outage_List_Start)):
    if ('132' in EventName[i]) and ('330' not in EventName[i]) and ('275' not in EventName[i]):
        Branch_kV.append(132)
    if ('330' in EventName[i]) and ('132' not in EventName[i]) and ('275' not in EventName[i]):
        Branch_kV.append(330)
    if ('275' in EventName[i]) and ('132' not in EventName[i]) and ('330' not in EventName[i]):
        Branch_kV.append(275)

# Bus_Name=['InverterTerminal','MetzPoC132', 'Armidale330',  'Armidale132',   'Armidale132C', 'Koolkhan132', 'GlenInnes132',     'CoffsHarbour330','CoffsHarbour132','Inverell132','Dumeresq330','Kempsy132', 'Tamworth330', 'Lismore132',  'Terranora110', 'PortMacquarie132', 'BulliCreek330',  'Mudgeeraba110']
# Bus_List=[100,              500,        21075,          22070,          29600,          23817,          23630,          21179,            22140,            23780,        21253,            23801,     21771,         22459,        23050,           25469,              49031,            45040]
# PowerFlow_Monitor_Start_List=[500,500,  21075,  21075,  22140,  22070,  23630,  22070,  21075,  22459,  22140,  23801,  21253,  23050]
# PowerFlow_Monitor_End_List=[22070,23817,21771,  21179,  29600,  23630,  23780,  23780,  21253,  23817,  23817,  25469,  49031,  45040]
# PowerFlow_Monitor_Name_List=[];
# or i in range(0,len(PowerFlow_Monitor_Start_List)):
# PowerFlow_Monitor_Name_List.append(Bus_Name[Bus_List.index(PowerFlow_Monitor_Start_List[i])]+' to '+Bus_Name[Bus_List.index(PowerFlow_Monitor_End_List[i])]);

# Branch_Outage_List_Start=PowerFlow_Monitor_Start_List[0:-3]
# Branch_Outage_List_End  =PowerFlow_Monitor_End_List[0:-3]

# Initialize
psspy.read(0, GridInfoPath + file_name + ".raw")
psspy.resq(GridInfoPath + file_name + ".seq")
ierr = psspy.addmodellibrary(GridInfoPath + 'dsusr.dll')
ierr = psspy.addmodellibrary(HuaweiModelPath + 'HWH9001_342.dll')
ierr = psspy.addmodellibrary(HuaweiModelPath + 'PPC_PSSE_ver_13_08_34_2_10082018_AUS.dll')
ierr = psspy.addmodellibrary(HuaweiModelPath + 'MOD_GPM_SB_V7.dll')
ierr = psspy.addmodellibrary(GridInfoPath + 'GEWTG34.dll')
ierr = psspy.addmodellibrary(GridInfoPath + 'SMAPPC_B111_34_IVF111.dll')
ierr = psspy.addmodellibrary(GridInfoPath + 'SMASC_C135_34_IVF111.dll')
psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
psspy.dynamics_solution_param_2([_i, _i, _i, _i, _i, _i, _i, _i], [1.000, _f, 0.001, 0.004, _f, _f, _f, _f])

for i in range(0, len(Branch_Outage_List_Start)):
    for fault_type in range(1, 5):

        # re - initialize
        psspy.read(0, GridInfoPath + file_name + ".raw")
        psspy.dyre_new([1, 1, 1, 1], GridInfoPath + file_name + ".dyr", "", "", "")
        psspy.resq(GridInfoPath + file_name + ".seq")

        psspy.dscn(30531)
        psspy.dscn(36530)
        psspy.dscn(37530)
        psspy.dscn(50030)  # add for Clenergy project

        psspy.machine_data_2(30531, r"""12""", [0, _i, _i, _i, _i, _i],
                             [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
        psspy.machine_data_2(37530, r"""12""", [0, _i, _i, _i, _i, _i],
                             [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
        psspy.machine_data_2(100, r"""1""", [_i, _i, _i, _i, _i, _i],
                             [115, _f, _f, _f, 132, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
        psspy.machine_data_2(100, r"""1""", [_i, _i, _i, _i, _i, _i],
                             [_f, _f, 5, _f, 132, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
        psspy.machine_data_2(100, r"""1""", [_i, _i, _i, _i, _i, _i],
                             [_f, _f, _f, 5, 132, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f,
                              _f])  # be careful, partial active power = not enough solar irraidance.
        psspy.fdns([1, 0, 0, 1, 0, 0, 99, 0])

        for t_var in range(0, 9000):
            psspy.change_var(t_var, 0)
        psspy.plmod_status(30531, r"""1""", 1, 0)
        psspy.plmod_status(30531, r"""1""", 6, 0)
        psspy.plmod_status(30531, r"""1""", 7, 0)
        psspy.plmod_status(37530, r"""1""", 1, 0)
        psspy.plmod_status(37530, r"""1""", 6, 0)
        psspy.plmod_status(37530, r"""1""", 7, 0)
        psspy.bus_frequency_channel([1, 400], r"""System frequency""")
        psspy.voltage_channel([2, -1, -1, 101], r"""Inverter Voltage Mag.""")
        psspy.voltage_channel([3, -1, -1, 400], r"""WDs SF POC Voltage Mag.""")
        psspy.branch_p_and_q_channel([4, -1, -1, 400, 46660], r"""1""", [r"""P Injection""", r"""Q Injection"""])
        ierr = psspy.machine_array_channel([7, 2, 101], r"""1""", r"""Pelec 101""")
        ierr = psspy.machine_array_channel([8, 3, 101], r"""1""", r"""Qelec 101""")
        ierr = psspy.machine_array_channel([9, 2, 101], r"""1""", r"""Pelec 102""")
        ierr = psspy.machine_array_channel([10, 3, 101], r"""1""", r"""Qelec 102""")
        ierr = psspy.machine_array_channel([11, 2, 101], r"""1""", r"""Pelec 103""")
        ierr = psspy.machine_array_channel([12, 3, 101], r"""1""", r"""Qelec 103""")
        ierr = psspy.machine_array_channel([13, 2, 101], r"""1""", r"""Pelec 104""")
        ierr = psspy.machine_array_channel([14, 3, 101], r"""1""", r"""Qelec 104""")
        [ierr, var_ppc_conp] = psspy.mdlind(101, '1', 'EXC', 'CON')
        [ierr, var_ppc_setp] = psspy.mdlind(101, '1', 'EXC', 'VAR')
        [ierr, var_ppc_mode] = psspy.mdlind(101, '1', 'EXC', 'ICON')
        [ierr, var_inv_con] = psspy.mdlind(101, '1', 'GEN', 'CON')
        [ierr, var_inv_var] = psspy.mdlind(101, '1', 'GEN', 'VAR')

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
        psspy.bsys(1, 0, [0.0, 0.0], 0, [], 9, [40320, 40340, 40350, 40970, 40980, 40990, 41050, 41071, 41120], 0, [],
                   0, [])
        psspy.conl(1, 0, 2, [0, 0], [100.0, 0.0, 0.0, 100.0])
        psspy.conl(0, 1, 2, [0, 0], [100.0, 0.0, -306.02, 303.0])
        psspy.conl(0, 1, 3, [0, 0], [100.0, 0.0, -306.02, 303.0])
        psspy.ordr(0)
        psspy.fact()
        psspy.tysl(0)
        psspy.bsys(0, 0, [0.4, 500.], 0, [], 0, [], 0, [], 0, [])

        # start simulation
        psspy.strt_2([0,0], OutputFilePath)
        psspy.run(0, 1, 1000, 1, 0)
        ##        psspy.change_var(var_ppc_setp+10,115)
        ##        psspy.change_var(var_ppc_setp+11,-25)
        psspy.run(0, 5, 1000, 1, 0)
        if fault_type == 1:  # three phase
            psspy.dist_branch_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', 1, Branch_kV[i],
                                    [0.0, -0.2E+10])
            fault_name = 'ThreePhase'
            if Branch_kV[i] == 330 or Branch_kV[i] == 275:
                fault_time = 0.120
            if Branch_kV[i] == 132:
                fault_time = 0.500

        if fault_type == 2:  # single phase
            psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 1, 1, 0, 0],
                                  [0.5, 0.0, 0.000001, 0.0, 0.0])
            fault_name = 'SinglePhase'
            if Branch_kV[i] == 330 or Branch_kV[i] == 275:
                fault_time = 0.250
            if Branch_kV[i] == 132:
                fault_time = 0.720

        if fault_type == 3:  # phase to phase
            psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 2, 1, 0, 0],
                                  [0.5, 9999.0, 9999.0, 0.0, 0.000001])
            fault_name = 'TwoPhase'
            if Branch_kV[i] == 330 or Branch_kV[i] == 275:
                fault_time = 0.250
            if Branch_kV[i] == 132:
                fault_time = 0.720

        if fault_type == 4:  # phase to phase to ground
            psspy.dist_spcb_fault(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1', [3, 0, 2, 1, 0, 0],
                                  [0.5, 0.0, 0.000001, 0.0, 0.000001])
            fault_name = 'TwoPhaseGround'
            if Branch_kV[i] == 330 or Branch_kV[i] == 275:
                fault_time = 0.250
            if Branch_kV[i] == 132:
                fault_time = 0.720

        psspy.run(0, 5.0 + fault_time, 1000, 1, 0)
        psspy.dist_branch_trip(Branch_Outage_List_Start[i], Branch_Outage_List_End[i], '1')
        psspy.run(0, 15.000, 1000, 1, 0)

        # start draw curves
        # new folder if necessary
        GraphPath = FigurePath + ClauseName + '/' + LoadScenario + '/' + fault_name
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

        CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
        CurrentAx[0][0].plot(chandata['time'], chandata[2]);
        CurrentAx[1][0].plot(chandata['time'], chandata[3]);
        CurrentAx[0][1].plot(chandata['time'], chandata[4]);
        CurrentAx[1][1].plot(chandata['time'], chandata[5]);

        CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
        CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
        CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
        CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

        CurrentAx[0][0].set_xlim(left=4)
        CurrentAx[1][0].set_xlim(left=4)
        CurrentAx[0][1].set_xlim(left=4)
        CurrentAx[1][1].set_xlim(left=4)

        CurrentAx[0][0].set_ylim([-0.2, 1.3])
        CurrentAx[1][0].set_ylim([-0.2, 1.3])
        CurrentAx[0][1].set_ylim([-50, 600])
        CurrentAx[1][1].set_ylim([-300, 300])

        CurrentAx[0][0].set_xlabel(r"""Time/s""")
        CurrentAx[1][0].set_xlabel(r"""Time/s""")
        CurrentAx[0][1].set_xlabel(r"""Time/s""")
        CurrentAx[1][1].set_xlabel(r"""Time/s""")

        CurrentAx[0][0].set_ylabel(r"""Voltage/PU""")
        CurrentAx[1][0].set_ylabel(r"""Voltage/PU""")
        CurrentAx[0][1].set_ylabel(r"""Power/MW""")
        CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

        CurrentAx[0][0].set_title(r"""Inverter Terminal Voltage""")
        CurrentAx[1][0].set_title(r"""WDs SF PoC Voltage""")
        CurrentAx[0][1].set_title(r"""WDs SF Active Power Output""")
        CurrentAx[1][1].set_title(r"""WDs SF Reactive Power Output""")

        save_figure_name = GraphPath + "/" + EventName[i] + ' ' + str(Branch_Outage_List_Start[i]) + '-' + str(
            Branch_Outage_List_End[i]) + '.png'
        CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
        plt.close(CurrentFig)





