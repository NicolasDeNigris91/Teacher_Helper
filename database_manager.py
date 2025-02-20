# database_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela de alunos se ela não existir."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students
                             (id INTEGER PRIMARY KEY, 
                              name TEXT NOT NULL, 
                              course TEXT NOT NULL, 
                              mobile TEXT NOT NULL)''')
        self.connection.commit()

    def add_student(self, name, course, mobile):
        """Adiciona um novo aluno ao banco de dados."""
        self.cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        self.connection.commit()

    def edit_student(self, student_id, name, course, mobile):
        """Edita os dados de um aluno existente."""
        self.cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?", (name, course, mobile, student_id))
        self.connection.commit()

    def remove_student(self, student_id):
        """Remove um aluno do banco de dados."""
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.connection.commit()

    def search_students(self, name=None, mobile=None, course=None):
        """Pesquisa alunos com base nos critérios fornecidos."""
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE ?"
            params.append(f'%{name}%')
        if mobile:
            query += " AND mobile LIKE ?"
            params.append(f'%{mobile}%')
        if course:
            query += " AND course = ?"
            params.append(course)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_all_students(self):
        """Retorna todos os alunos cadastrados."""
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.connection.close()