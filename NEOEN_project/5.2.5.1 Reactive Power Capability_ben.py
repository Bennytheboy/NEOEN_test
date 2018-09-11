# Import modules
import os
import sys
import socket
import struct
import time

sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSBIN""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN;"+ os.environ['PATH'])
sys.path.append(r"""C:\Program Files (x86)\PTI\PSSE34\PSSPY27""")
os.environ['PATH'] = (r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27;"+ os.environ['PATH'])
import psse34
import psspy
import redirect
import numpy
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import dyntools

# OPEN PSS
_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()
redirect.psse2py()
psspy.psseinit(50000)

ierr = psspy.progress_output(6, ' ', [0, 0])  # disable output
ierr = psspy.prompt_output(6, ' ', [0, 0])  # disable output
ierr = psspy.report_output(6, ' ', [0, 0])  # disable output

# Set Simulation Path.
LoadScenario = "SimplifiedSystem"
ClauseName = "5.2.5.1 Reactive Power Capability_3"
ProgramPath = "F:/NEOEN/P_SimulationScripts/"
GridInfoPath = "F:/NEOEN/NEM_files/"
HuaweiModelPath = "F:/NEOEN/Huawei_models/"
OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
FigurePath = "F:/NEOEN/R_Results/"
# ProgramPath = "C:/NEOEN/P_SimulationScripts/"
# GridInfoPath = "C:/NEOEN/NEM_files/"
# HuaweiModelPath = "C:/NEOEN/Huawei_models/"
# OutputFilePath = ProgramPath + ClauseName+"_Simulation.outx"
# FigurePath = "C:/NEOEN/R_Results/"


if LoadScenario == "SummerPeakLoad":
        file_name = "SummerHi-20171219-153047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SummerLowLoad":
        file_name = "SummerLo-20171226-043047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SimplifiedSystem":
        file_name = "NEOEN Western Downs Solar Farm_C3WV"

# PowerFlowFileName = 'NEOEN Western Downs Solar Farm_C3WV_3.raw'

# Initialize
psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name +".raw")

P_Record = []
Q_Record = []
T_Record = []
V_Record = []
S_Record = []

overloop = 0

S = 120; # chang: this is wrong, each cluster has only ~120MVA capacity. I guess the power flow does not converge.

overloop=0; # add this line.


Capacitor = 0;  # capacitor

for temperature in [40, 50]:
    for terminalv in [0.9, 1.0, 1.1]:
        if temperature == 50:
            derate = 0.9
        else:
            derate = 1.0

        psspy.plant_data(600, _i, [terminalv, _f])

        for P_Gen in numpy.arange(0, S * derate + 0.01, 1):
            psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
            #psspy.switched_shunt_chng_3(104, [_i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i],
            #                            [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, 0, _f], "")
            #psspy.switched_shunt_chng_3(204, [_i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i],
            #                            [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, 0, _f], "")
            Q_Gen = max(-S * 0.6, -math.sqrt(S * S * derate * derate - P_Gen * P_Gen))
            psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.plant_data(600, _i, [terminalv, _f])
            psspy.fdns([1, 0, 1, 1, 1, 1, 99, 0])
            ierr, pval = psspy.brnmsc(400, 46660, '1', 'P')  # chang: make sure there is such branch.
            ierr, qval = psspy.brnmsc(400, 46660, '1', 'Q')
            ierr, vval = psspy.busdat(101, 'PU')

            valid_pq = 0;
            loop = 0;
            while (1):
                if ((math.sqrt(P_Gen ** 2 + Q_Gen ** 2) < ((S * min(derate, vval)) + 0.02)) and vval <= 1.1):
                    valid_pq = 1;
                    break;


                if loop >= 50:
                    valid_pq = 0;
                    overloop=overloop+1 # chang: add this line.
                    break;

                if ((math.sqrt(P_Gen ** 2 + Q_Gen ** 2) > ((S * min(derate, vval)) + 0.02)) or vval > 1.1):
                    valid_pq = 0;
                    Q_Gen = Q_Gen + 1
                    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.fdns([1, 0, 1, 1, 1, 1, 99, 0])
                    ierr, pval = psspy.brnmsc(400, 46660, '1', 'P')
                    ierr, qval = psspy.brnmsc(400, 46660, '1', 'Q')
                    ierr, vval = psspy.busdat(101, 'PU')
                    loop = loop + 1;

            if valid_pq == 1:
                     P_Record.append(pval)
                     Q_Record.append(qval)
                     T_Record.append(temperature)
                     V_Record.append(terminalv)

        for P_Gen in numpy.arange(0, S * derate + 0.01, 1):     #################################CHANG: DO NOT CHANGE INDENTATION
            psspy.read(0, GridInfoPath + LoadScenario + "/" + file_name + ".raw")
            Q_Gen = min(S * 0.6, math.sqrt(S * S * derate * derate - P_Gen * P_Gen))
    #psspy.switched_shunt_chng_3(104, [_i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i],
     #                           [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, Capacitor, _f], "")
    #psspy.switched_shunt_chng_3(204, [_i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i, _i],
    #                            [_f, _f, _f, _f, _f, _f, _f, _f, _f, _f, Capacitor, _f], "")
            psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                     [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                 [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
            psspy.plant_data(600, _i, [terminalv, _f])
            psspy.fdns([1, 0, 1, 1, 1, 1, 99, 0])
            ierr, pval = psspy.brnmsc(400, 46660, '1', 'P')
            ierr, qval = psspy.brnmsc(400, 46660, '1', 'Q')
            ierr, vval = psspy.busdat(101, 'PU')
            valid_pq = 0;
            loop = 0;
            while (1):
                if math.sqrt(P_Gen ** 2 + Q_Gen ** 2) < ((S * min(derate, vval)) + 0.02) and vval <= 1.1:
                    valid_pq = 1;
                    break;

                if loop >= 50:
                    valid_pq = 0;
                    overloop=overloop+1
                    break;

                if math.sqrt(P_Gen ** 2 + Q_Gen ** 2) > ((S * min(derate, vval)) + 0.02) or vval > 1.1:
                    valid_pq = 0;
                    Q_Gen = Q_Gen - 1
                    psspy.machine_data_2(101, r"""1""", [_i, _i, _i, _i, _i, _i],
                                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(102, r"""1""", [_i, _i, _i, _i, _i, _i],
                                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(103, r"""1""", [_i, _i, _i, _i, _i, _i],
                                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.machine_data_2(104, r"""1""", [_i, _i, _i, _i, _i, _i],
                                                         [P_Gen, Q_Gen, Q_Gen, Q_Gen, S, 0, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f, _f])
                    psspy.fdns([1, 0, 1, 1, 1, 1, 99, 0])
                    ierr, pval = psspy.brnmsc(400, 46660, '1', 'P')
                    ierr, qval = psspy.brnmsc(400, 46660, '1', 'Q')
                    ierr, vval = psspy.busdat(101, 'PU')
                    loop = loop + 1;
            if valid_pq == 1:
                P_Record.append(pval)
                Q_Record.append(qval)
                T_Record.append(temperature)
                V_Record.append(terminalv)

print overloop

P_Record = numpy.asarray(P_Record)
Q_Record = numpy.asarray(Q_Record)
T_Record = numpy.asarray(T_Record)
V_Record = numpy.asarray(V_Record)
numpy.savetxt('F:\NEOEN\R_Results\SolarFarmPQDiagram.csv', (P_Record, Q_Record, T_Record, V_Record), delimiter=',')

# Handling Data

DrawCenterX = 0;
DrawCenterY = -10;

##PQ_Array=[Q_Record-DrawCenterX,P_Record-DrawCenterY];
##PQ_Angle=numpy.arccos(numpy.divide(PQ_Array[0],numpy.sqrt(numpy.square(PQ_Array[0])+numpy.square(PQ_Array[1]))));


##P_Recrod=P_Record[SortIndex];
##Q_Record=Q_Record[SortIndex];
##T_Record=T_Record[SortIndex];
##V_Record=V_Record[SortIndex];


P_40_09 = P_Record[(T_Record == 40) & (V_Record == 0.9)];
P_40_10 = P_Record[(T_Record == 40) & (V_Record == 1.0)];
P_40_11 = P_Record[(T_Record == 40) & (V_Record == 1.1)];
P_50_09 = P_Record[(T_Record == 50) & (V_Record == 0.9)];
P_50_10 = P_Record[(T_Record == 50) & (V_Record == 1.0)];
P_50_11 = P_Record[(T_Record == 50) & (V_Record == 1.1)];

Q_40_09 = Q_Record[(T_Record == 40) & (V_Record == 0.9)];
Q_40_10 = Q_Record[(T_Record == 40) & (V_Record == 1.0)];
Q_40_11 = Q_Record[(T_Record == 40) & (V_Record == 1.1)];
Q_50_09 = Q_Record[(T_Record == 50) & (V_Record == 0.9)];
Q_50_10 = Q_Record[(T_Record == 50) & (V_Record == 1.0)];
Q_50_11 = Q_Record[(T_Record == 50) & (V_Record == 1.1)];

PQ_Array = [Q_40_09 - DrawCenterX, P_40_09 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_40_09_index = numpy.argsort(PQ_Angle / 400);  # MAY NEED TO CORRECT 150 TO 400.

PQ_Array = [Q_40_10 - DrawCenterX, P_40_10 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_40_10_index = numpy.argsort(PQ_Angle / 400); # MAY NEED TO CORRECT 150 TO 400.

PQ_Array = [Q_40_11 - DrawCenterX, P_40_11 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_40_11_index = numpy.argsort(PQ_Angle / 400);

PQ_Array = [Q_50_09 - DrawCenterX, P_50_09 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_50_09_index = numpy.argsort(PQ_Angle / 400);

PQ_Array = [Q_50_10 - DrawCenterX, P_50_10 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_50_10_index = numpy.argsort(PQ_Angle / 400.0);

PQ_Array = [Q_50_11 - DrawCenterX, P_50_11 - DrawCenterY];
PQ_Angle = numpy.arccos(numpy.divide(PQ_Array[0], numpy.sqrt(numpy.square(PQ_Array[0]) + numpy.square(PQ_Array[1]))));
A_50_11_index = numpy.argsort(PQ_Angle / 400.0);

P_40_09 = P_40_09[A_40_09_index];
P_40_10 = P_40_10[A_40_10_index];
P_40_11 = P_40_11[A_40_11_index];
P_50_09 = P_50_09[A_50_09_index];
P_50_10 = P_50_10[A_50_10_index];
P_50_11 = P_50_11[A_50_11_index];

Q_40_09 = Q_40_09[A_40_09_index];
Q_40_10 = Q_40_10[A_40_10_index];
Q_40_11 = Q_40_11[A_40_11_index];
Q_50_09 = Q_50_09[A_50_09_index];
Q_50_10 = Q_50_10[A_50_10_index];
Q_50_11 = Q_50_11[A_50_11_index];

# new folder if necessary
GraphPath = FigurePath + ClauseName + '/'
if not os.path.exists(GraphPath):
    os.makedirs(GraphPath)

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

CurrentFig, CurrentAx = plt.subplots(1, 1, sharex=False, figsize=(16, 12));

CurrentAx.plot(Q_40_09, P_40_09, color='blue', linestyle='-', marker='o', markevery=5);
CurrentAx.plot(Q_40_10, P_40_10, color='green', linestyle='-', marker='s', markevery=5);
CurrentAx.plot(Q_40_11, P_40_11, color='orange', linestyle='-', marker='^', markevery=5);
CurrentAx.plot([-150, -150, 150, 150], [0, 400, 400, 0], color='red', linestyle=':');
CurrentAx.legend([r"""T=25,V=0.9""", r"""T=25,V=1.0""", r"""T=25,V=1.1""", r"""Automatic Access Standard"""])
save_figure_name = GraphPath + 'P-Q Diagram @25 degree' + '.png'

CurrentAx.tick_params(axis='both', which='both', labelsize=24)
CurrentAx.set_xlabel(r"""Q / MVar""")
CurrentAx.set_ylabel(r"""P / MW  """)
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)

CurrentAx.plot(Q_50_09,P_50_09,color='blue',linestyle='-',marker='o',markevery=5);
CurrentAx.plot(Q_50_10,P_50_10,color='green',linestyle='-',marker='s',markevery=5);
CurrentAx.plot(Q_50_11,P_50_11,color='orange',linestyle='-',marker='^',markevery=5);
CurrentAx.plot([-150, -150, 150, 150], [0, 400, 400, 0],color='red',linestyle=':');
CurrentAx.legend([r"""T=50,V=0.9""",r"""T=50,V=1.0""",r"""T=50,V=1.1""",r"""Automatic Access Standard"""])  #,r"""Proposed Minimum Reactive Power"""
save_figure_name=GraphPath+'P-Q Diagram @50 degree'+'.png'


CurrentAx.tick_params(axis='both', which='both', labelsize=24)

##CurrentAx.set_xlim([-120,120])
##CurrentAx.set_ylim([ -10,140])

CurrentAx.set_xlabel(r"""Q / MVar""")
CurrentAx.set_ylabel(r"""P / MW  """)

CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)



