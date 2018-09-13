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
LoadScenario = "SummerPeakLoad"
ClauseName = "5.2.5.13 Reactive Power and Voltage Control"
ProgramPath = "F:/PosDoc Projects/11_Industrial Projects/NEOEN_HW/P_SimulationProgram/"
GridInfoPath = "F:/PosDoc Projects/11_Industrial Projects/NEOEN_HW/NEM_files/" + LoadScenario + "/"
HuaweiModelPath = "F:/PosDoc Projects/11_Industrial Projects/NEOEN_HW/D_HuaweiModels/34/"
OutputFilePath = ProgramPath + "5.2.5.13_SimulationOutput_1.outx"
FigurePath = "F:/PosDoc Projects/11_Industrial Projects/NEOEN_HW/R_Results/"

if LoadScenario == "SummerPeakLoad":
    file_name = "SummerHi-20171219-153047-34-SystemNormal_all_bus_DDSF"
if LoadScenario == "SummerLowLoad":
    file_name = "SummerLowNormal-20161225-040047"
if LoadScenario == "SimplifiedSystem":
    file_name = "NEOEN Western Downs Solar Farm_C3WV_3"


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
mpl.rcParams['legend.loc'] = 'lower center'
mpl.rcParams['legend.numpoints'] = 3
mpl.rcParams['legend.fontsize'] = 'small'

CurrentFig, CurrentAx = plt.subplots(2, 2, sharex=False, figsize=(20, 15));
CurrentAx[0][0].plot(chandata['time'], chandata[2]);
##            CurrentAx[0][0].plot(chandata['time'],chandata[9],linestyle='--',color='coral');
CurrentAx[1][0].plot(chandata['time'], chandata[3]);
CurrentAx[0][1].plot(chandata['time'], chandata[4]);
CurrentAx[1][1].plot(chandata['time'], chandata[5]);

CurrentAx[0][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][0].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[0][1].tick_params(axis='both', which='both', labelsize=24)
CurrentAx[1][1].tick_params(axis='both', which='both', labelsize=24)

CurrentAx[0][0].set_xlim([4, 15])
CurrentAx[1][0].set_xlim([4, 15])
CurrentAx[0][1].set_xlim([4, 15])
CurrentAx[1][1].set_xlim([4, 15])

CurrentAx[0][0].set_ylim([0.9, 1.1])
CurrentAx[1][0].set_ylim([0.9, 1.1])
CurrentAx[0][1].set_ylim([100, 120])
CurrentAx[1][1].set_ylim([-60, 60])

CurrentAx[0][0].set_xlabel(r"""Time/s""")
CurrentAx[1][0].set_xlabel(r"""Time/s""")
CurrentAx[0][1].set_xlabel(r"""Time/s""")
CurrentAx[1][1].set_xlabel(r"""Time/s""")

CurrentAx[0][0].set_ylabel(r"""Votlage/PU""")
CurrentAx[1][0].set_ylabel(r"""Voltage/PU""")
CurrentAx[0][1].set_ylabel(r"""Power/MW""")
CurrentAx[1][1].set_ylabel(r"""Power/MVar""")

CurrentAx[0][0].legend(["Inverter Terminal Voltage"])
CurrentAx[1][0].legend(["Metz SF PoC Voltage"])
CurrentAx[0][1].legend(["Metz SF Active Power Output"], loc='upper center')
CurrentAx[1][1].legend(["Metz SF Reactive Power Output"])

save_figure_name = GraphPath + "/" + '5% Step Change.png'
CurrentFig.savefig(save_figure_name, format='png', dpi=150, bbox_inches='tight')
plt.close(CurrentFig)

raw_input("Press enter to exit...")
redirect.reset()
