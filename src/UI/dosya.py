import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        # Widget'lar
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Statusbar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # Statusbar'a bilgi ekleme
        self.statusbar.showMessage("Hazırlanıyor...")

        # Pencereyi tam ekran yap
        MainWindow.showMaximized()  # Tam ekran yerine maksimal boyutta pencere göster

        # Pencereyi normal hale getir
        MainWindow.setWindowFlags(QtCore.Qt.Window)  # Pencereyi normal hale getirir ve butonları gösterir

        # Menüleri ve pencereyi bağla
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()  # Pencereyi göster
    sys.exit(app.exec_())  # Uygulamayı başlat
