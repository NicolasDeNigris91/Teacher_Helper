# ui_components.py
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox
from PyQt6.QtGui import QIcon

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["ID", "Nome", "Curso", "Celular"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setStyleSheet("QTableWidget::item:selected { background-color: #a6d5ff; }")

    def load_data(self, data):
        """Carrega os dados na tabela."""
        self.setRowCount(0)
        self.setRowCount(len(data))
        for i, row in enumerate(data):
            self.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.setItem(i, 3, QTableWidgetItem(str(row[3])))

class StudentDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QFormLayout(self)
        self.name_edit = QLineEdit(self)
        self.course_combo = QComboBox(self)
        self.course_combo.addItems(["Math", "Literature", "Astronomy", "Physics", "Biology"])
        self.mobile_edit = QLineEdit(self)

        self.layout.addRow("Nome:", self.name_edit)
        self.layout.addRow("Curso:", self.course_combo)
        self.layout.addRow("Celular:", self.mobile_edit)

        self.save_button = QPushButton("Salvar", self)
        self.layout.addWidget(self.save_button)