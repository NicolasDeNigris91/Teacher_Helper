# main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QMenu, QWidget, QVBoxLayout, QLabel, QToolBar, QStatusBar, QMessageBox, QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from database_manager import DatabaseManager
from ui_components import TableWidget, StudentDialog

class StudentManagerSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager('database.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Student Manager System")
        self.setup_menus()
        self.setup_toolbar()
        self.setup_table()
        self.setup_status_bar()

    def setup_menus(self):
        """Configura os menus da barra de menu."""
        menubar = self.menuBar()

        # Menu Add
        add_menu = menubar.addMenu("Add")
        add_action = QAction("Adicionar Aluno", self)
        add_action.triggered.connect(self.add_student)
        add_menu.addAction(add_action)

        # Menu Search
        search_menu = menubar.addMenu("Search")
        search_action = QAction("Pesquisar Aluno", self)
        search_action.triggered.connect(self.search_student)
        search_menu.addAction(search_action)

        # Menu Edit
        edit_menu = menubar.addMenu("Edit")
        edit_action = QAction("Editar Aluno", self)
        edit_action.triggered.connect(self.edit_student)
        edit_menu.addAction(edit_action)

        # Menu Remove
        remove_menu = menubar.addMenu("Remove")
        remove_action = QAction("Remover Aluno", self)
        remove_action.triggered.connect(self.remove_student)
        remove_menu.addAction(remove_action)

        # Menu Reports
        reports_menu = menubar.addMenu("Reports")
        report_action = QAction("Relatório por Curso", self)
        report_action.triggered.connect(self.generate_course_report)
        reports_menu.addAction(report_action)

    def setup_toolbar(self):
        """Configura a toolbar com ícones e ações."""
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        # Ícone de pesquisa
        search_icon = QIcon("icons/search.png")
        search_action = QAction(search_icon, "Pesquisar Aluno", self)
        search_action.triggered.connect(self.search_student)
        search_action.setToolTip("Pesquisar Aluno")
        toolbar.addAction(search_action)

        # Ícone de adicionar
        add_icon = QIcon("icons/add.png")
        add_action = QAction(add_icon, "Adicionar Aluno", self)
        add_action.triggered.connect(self.add_student)
        add_action.setToolTip("Adicionar Aluno")
        toolbar.addAction(add_action)

    def setup_table(self):
        """Configura a tabela de alunos."""
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.table = TableWidget()
        layout.addWidget(self.table)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.load_data()

    def setup_status_bar(self):
        """Configura a status bar com botões de ação."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Botão de editar
        edit_icon = QIcon("icons/edit.png")
        edit_button = QPushButton(edit_icon, "Editar")
        edit_button.clicked.connect(self.edit_student)
        edit_button.setToolTip("Editar Aluno")
        self.status_bar.addWidget(edit_button)

        # Botão de remover
        delete_icon = QIcon("icons/delete.png")
        delete_button = QPushButton(delete_icon, "Remover")
        delete_button.clicked.connect(self.remove_student)
        delete_button.setToolTip("Remover Aluno")
        self.status_bar.addWidget(delete_button)

    def load_data(self):
        """Carrega os dados dos alunos na tabela."""
        students = self.db.get_all_students()
        self.table.load_data(students)

    def add_student(self):
        """Abre o diálogo para adicionar um novo aluno."""
        dialog = StudentDialog("Adicionar Aluno", self)
        dialog.save_button.clicked.connect(lambda: self.save_student(dialog))
        dialog.exec()

    def save_student(self, dialog):
        """Salva os dados do aluno no banco de dados."""
        name = dialog.name_edit.text()
        course = dialog.course_combo.currentText()
        mobile = dialog.mobile_edit.text()

        if name and course and mobile:
            self.db.add_student(name, course, mobile)
            self.load_data()
            self.show_message("Sucesso", "Aluno adicionado com sucesso!")
            dialog.accept()
        else:
            self.show_message("Erro", "Por favor, preencha todos os campos antes de continuar.", QMessageBox.Icon.Warning)

    def edit_student(self):
        """Abre o diálogo para editar um aluno existente."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            student_id = self.table.item(selected_row, 0).text()
            name = self.table.item(selected_row, 1).text()
            course = self.table.item(selected_row, 2).text()
            mobile = self.table.item(selected_row, 3).text()

            dialog = StudentDialog("Editar Aluno", self)
            dialog.name_edit.setText(name)
            dialog.course_combo.setCurrentText(course)
            dialog.mobile_edit.setText(mobile)
            dialog.save_button.clicked.connect(lambda: self.update_student(dialog, student_id))
            dialog.exec()
        else:
            self.show_message("Erro", "Selecione um aluno para editar.", QMessageBox.Icon.Warning)

    def update_student(self, dialog, student_id):
        """Atualiza os dados do aluno no banco de dados."""
        name = dialog.name_edit.text()
        course = dialog.course_combo.currentText()
        mobile = dialog.mobile_edit.text()

        if name and course and mobile:
            self.db.edit_student(student_id, name, course, mobile)
            self.load_data()
            self.show_message("Sucesso", "Aluno atualizado com sucesso!")
            dialog.accept()
        else:
            self.show_message("Erro", "Por favor, preencha todos os campos antes de continuar.", QMessageBox.Icon.Warning)

    def remove_student(self):
        """Remove um aluno do banco de dados."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            student_id = self.table.item(selected_row, 0).text()

            reply = QMessageBox.question(self, "Remover Aluno", "Tem certeza que deseja remover este aluno?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.db.remove_student(student_id)
                self.load_data()
                self.show_message("Sucesso", "Aluno removido com sucesso!")
        else:
            self.show_message("Erro", "Selecione um aluno para remover.", QMessageBox.Icon.Warning)

    def search_student(self):
        """Abre o diálogo para pesquisar alunos."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Pesquisar Aluno")

        layout = QFormLayout(dialog)
        name_edit = QLineEdit(dialog)
        mobile_edit = QLineEdit(dialog)
        course_combo = QComboBox(dialog)
        course_combo.addItems(["Todos", "Math", "Literature", "Astronomy", "Physics", "Biology"])

        layout.addRow("Nome:", name_edit)
        layout.addRow("Celular:", mobile_edit)
        layout.addRow("Curso:", course_combo)

        search_button = QPushButton("Pesquisar")
        search_button.clicked.connect(lambda: self.execute_search(dialog, name_edit, mobile_edit, course_combo))
        layout.addWidget(search_button)

        dialog.setLayout(layout)
        dialog.exec()

    def execute_search(self, dialog, name_edit, mobile_edit, course_combo):
        """Executa a pesquisa e exibe os resultados na tabela."""
        name = name_edit.text()
        mobile = mobile_edit.text()
        course = course_combo.currentText()

        students = self.db.search_students(name, mobile, course if course != "Todos" else None)
        self.table.load_data(students)
        dialog.accept()

    def generate_course_report(self):
        """Gera um relatório de alunos por curso."""
        self.cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")
        rows = self.cursor.fetchall()

        report = "Relatório de Alunos por Curso:\n\n"
        for row in rows:
            report += f"{row[0]}: {row[1]} aluno(s)\n"

        self.show_message("Relatório por Curso", report)

    def show_message(self, title, message, icon=QMessageBox.Icon.Information):
        """Exibe uma mensagem na tela."""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec()

    def closeEvent(self, event):
        """Fecha a conexão com o banco de dados ao fechar a janela."""
        self.db.close()
        event.accept()