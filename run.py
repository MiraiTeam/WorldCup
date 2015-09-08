from teams import *
from arrange import *
from ui import *
import sys

app = QtGui.QApplication(sys.argv)
MainWindow = GUI()

teams = GetTeamsInfo()
PrintTeamsInfo(teams)
groups = Seeding(teams)
arrange = GetArrangement(groups,0)
PrintArrangement(arrange)

MainWindow.setPic(81,"agenting")
MainWindow.setPic(82,"deguo")
MainWindow.setPic(83,"yidali")
MainWindow.setPic(84,"meiguo")
MainWindow.setPic(85,"faguo")
MainWindow.setPic(86,"xibanya")
MainWindow.setPic(87,"moxige")
MainWindow.setPic(88,"ruishi")
MainWindow.setPic(41,"deguo")

sys.exit(app.exec_())
