import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtCore

class TaskCard(QFrame):
    def __init__(self, task_name, due_date, section, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ccc; padding: 10px;")
        self.layout = QVBoxLayout(self)

        self.setFixedSize(250, 100)  # Kart boyutu sabitlendi

        self.task_label = QLabel(task_name)
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("font-size: 18px; color: black;")
        self.layout.addWidget(self.task_label)

        today = QDate.currentDate()
        due_date = QDate.fromString(due_date, "yyyy-MM-dd")
        days_left = today.daysTo(due_date)
        self.due_date_label = QLabel(f"{days_left} gün kaldı")
        self.due_date_label.setAlignment(Qt.AlignRight)
        self.due_date_label.setStyleSheet("font-size: 10px; color: #555;")
        self.layout.addWidget(self.due_date_label)

        self.buttons_layout = QHBoxLayout()
        self.move_button = QPushButton("Taşı")
        self.move_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        self.delete_button = QPushButton("Sil")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px; border-radius: 5px;")
        
        self.buttons_layout.addWidget(self.move_button)
        self.buttons_layout.addWidget(self.delete_button)
        
        self.layout.addLayout(self.buttons_layout)

        self.move_button.clicked.connect(lambda: self.move_task(section))
        self.delete_button.clicked.connect(self.delete_task)

    def move_task(self, section):
        if section == "Plan":
            ui.move_task_to_doing(self)
        elif section == "Yapılıyor":
            ui.move_task_to_done(self)
        self.move_button.setEnabled(False)

    def delete_task(self):
        self.deleteLater()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(main_layout)

        self.task_creation_box = QGroupBox("Yeni Task")
        self.task_creation_box.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; border: 1px solid #ccc;")
        task_creation_layout = QVBoxLayout(self.task_creation_box)
        
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Task adı girin...")
        self.task_name_input.setAlignment(Qt.AlignCenter)
        task_creation_layout.addWidget(self.task_name_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Tarih (YYYY-MM-DD) girin...")
        self.date_input.setAlignment(Qt.AlignCenter)
        task_creation_layout.addWidget(self.date_input)

        self.add_task_button = QPushButton("Task Ekle")
        self.add_task_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        task_creation_layout.addWidget(self.add_task_button)
        
        main_layout.addWidget(self.task_creation_box)

        self.sections_layout = QHBoxLayout()
        main_layout.addLayout(self.sections_layout)

        self.plan_section = self.create_section("Plan", "#FFEB3B")
        self.sections_layout.addWidget(self.plan_section)

        self.doing_section = self.create_section("Yapılıyor", "#FF9800")
        self.sections_layout.addWidget(self.doing_section)

        self.done_section = self.create_section("Bitti", "#4CAF50")
        self.sections_layout.addWidget(self.done_section)

        self.add_task_button.clicked.connect(self.add_task)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_section(self, title, color):
        group_box = QGroupBox(title)
        group_box.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
        layout = QVBoxLayout()
        group_box.setLayout(layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)

        return scroll_widget

    def add_task(self):
        task_name = self.task_name_input.text()
        due_date = self.date_input.text()

        if task_name and due_date:
            task_card = TaskCard(task_name, due_date, "Plan")
            self.plan_section.layout().addWidget(task_card)
            self.task_name_input.clear()
            self.date_input.clear()

    def move_task_to_doing(self, task_card):
        self.doing_section.layout().addWidget(task_card)
        task_card.setStyleSheet("background-color: #FF9800; border-radius: 10px; padding: 10px;")

    def move_task_to_done(self, task_card):
        self.done_section.layout().addWidget(task_card)
        task_card.setStyleSheet("background-color: #4CAF50; border-radius: 10px; padding: 10px;")
        task_card.move_button.setVisible(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Task Manager"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
