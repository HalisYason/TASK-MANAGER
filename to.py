import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtCore


class TaskCard(QFrame):
    def __init__(self, task_name, due_date, section, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ccc; padding: 10px;")
        self.layout = QVBoxLayout(self)

        # Task name label
        self.task_label = QLabel(task_name)
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("font-size: 18px; color: black;")
        self.layout.addWidget(self.task_label)

        # Due date calculation
        today = QDate.currentDate()
        due_date = QDate.fromString(due_date, "yyyy-MM-dd")
        days_left = today.daysTo(due_date)
        self.due_date_label = QLabel(f"{days_left} gün kaldı")
        self.due_date_label.setAlignment(Qt.AlignRight)
        self.due_date_label.setStyleSheet("font-size: 10px; color: #555;")  # Küçük font
        self.layout.addWidget(self.due_date_label)

        # Buttons for "move" and "delete"
        self.buttons_layout = QHBoxLayout()
        self.move_button = QPushButton("Taşı")
        self.move_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        self.delete_button = QPushButton("Sil")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px; border-radius: 5px;")
        
        self.buttons_layout.addWidget(self.move_button)
        self.buttons_layout.addWidget(self.delete_button)
        
        self.layout.addLayout(self.buttons_layout)

        # Taşıma butonuna fonksiyon ekle
        self.move_button.clicked.connect(lambda: self.move_task(section))

        # Silme butonuna fonksiyon ekle
        self.delete_button.clicked.connect(self.delete_task)

        # Sabit kart boyutları (150px x 200px)
        self.setFixedSize(150, 200)

    def move_task(self, section):
        if section == "Plan":
            # Plan'dan Yapılıyor'a taşı
            ui.move_task_to_doing(self)
        elif section == "Yapılıyor":
            # Yapılıyor'dan Bitti'ye taşı
            ui.move_task_to_done(self)
        self.move_button.setEnabled(False)  # Taşı butonunu devre dışı bırak

    def delete_task(self):
        self.deleteLater()  # Task'ı siler


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Main Layout
        main_layout = QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(main_layout)

        # Task Creation Area (Tam Ortada)
        self.task_creation_box = QGroupBox("Yeni Task")
        self.task_creation_box.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; border: 1px solid #ccc;")
        task_creation_layout = QVBoxLayout(self.task_creation_box)
        
        # Task name input field (orta hizalı)
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Task adı girin...")
        self.task_name_input.setAlignment(Qt.AlignCenter)
        task_creation_layout.addWidget(self.task_name_input)

        # Date input field (YYYY-MM-DD)
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Tarih (YYYY-MM-DD) girin...")
        self.date_input.setAlignment(Qt.AlignCenter)
        task_creation_layout.addWidget(self.date_input)

        # Add Task Button
        self.add_task_button = QPushButton("Task Ekle")
        self.add_task_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        task_creation_layout.addWidget(self.add_task_button)
        
        main_layout.addWidget(self.task_creation_box)

        # Task Sections with Scrollable Areas
        self.sections_layout = QHBoxLayout()
        main_layout.addLayout(self.sections_layout)

        # Plan Section (scrollable)
        self.plan_section = self.create_section("Plan", "#FFEB3B")
        self.sections_layout.addWidget(self.plan_section)

        # Doing Section (scrollable)
        self.doing_section = self.create_section("Yapılıyor", "#FF9800")
        self.sections_layout.addWidget(self.doing_section)

        # Done Section (scrollable)
        self.done_section = self.create_section("Bitti", "#4CAF50")
        self.sections_layout.addWidget(self.done_section)

        # Button Click Event
        self.add_task_button.clicked.connect(self.add_task)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_section(self, title, color):
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")

        section_title = QLabel(title)
        section_title.setAlignment(Qt.AlignCenter)
        section_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        section_layout.addWidget(section_title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Bu kısmı doğru ekliyoruz
        section_layout.addWidget(scroll_area)

        # İçerik alanı için bir widget ekliyoruz
        scroll_widget = QWidget()
        scroll_widget.setLayout(section_layout)
        scroll_area.setWidget(scroll_widget)

        return scroll_area

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
        task_card.move_button.setVisible(False)  # Taşı butonunu gizle

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
