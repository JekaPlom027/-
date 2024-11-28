import sqlite3

class DatabaseManager:


    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                student_id INTEGER,
                teacher_id INTEGER
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                task_description TEXT,
                number_of_points INTEGER,
                Deadline TEXT,
                teacher_id INTEGER,
                comments TEXT,
                course_id INTEGER
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_completing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Deadline_compliance TEXT,
                Points_gained INTEGER,
                Student_id INTEGER,
                task_id INTEGER
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher_course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER,
                course_id INTEGER
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Surname TEXT NOT NULL
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_course (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_course_id INTEGER,
                student_id INTEGER
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL
            )
        ''')


        self.connection.commit()

    def insert_data(self):

        self.cursor.execute("INSERT INTO teacher (Name, Surname) VALUES ('John', 'Doe')")
        self.cursor.execute("INSERT INTO teacher (Name, Surname) VALUES ('Jane', 'Smith')")


        self.cursor.execute("INSERT INTO student (name, surname) VALUES ('Alice', 'Johnson')")
        self.cursor.execute("INSERT INTO student (name, surname) VALUES ('Bob', 'Brown')")


        self.cursor.execute("INSERT INTO course (course_name, student_id, teacher_id) VALUES ('Mathematics', 1, 1)")
        self.cursor.execute("INSERT INTO course (course_name, student_id, teacher_id) VALUES ('Physics', 2, 2)")


        self.cursor.execute("INSERT INTO tasks (name, task_description, number_of_points, Deadline, teacher_id, comments, course_id) VALUES ('Homework 1', 'Solve problems 1 to 10', 10, '2023-12-01', 1, 'First homework', 1)")
        self.cursor.execute("INSERT INTO tasks (name, task_description, number_of_points, Deadline, teacher_id, comments, course_id) VALUES ('Project 1', 'Complete the group project', 20, '2023-12-15', 2, 'Group project', 2)")


        self.cursor.execute("INSERT INTO task_completing (Deadline_compliance, Points_gained, Student_id, task_id) VALUES ('On time', 10, 1, 1)")
        self.cursor.execute("INSERT INTO task_completing (Deadline_compliance, Points_gained, Student_id, task_id) VALUES ('Late', 5, 2, 2)")


        self.cursor.execute("INSERT INTO teacher_course (teacher_id, course_id) VALUES (1, 1)")
        self.cursor.execute("INSERT INTO teacher_course (teacher_id, course_id) VALUES (2, 2)")


        self.cursor.execute("INSERT INTO student_course (main_course_id, student_id) VALUES (1, 1)")
        self.cursor.execute("INSERT INTO student_course (main_course_id, student_id) VALUES (2, 2)")


        self.connection.commit()

    def execute_select_queries(self):
        print("Teachers:")
        self.cursor.execute("SELECT * FROM teacher")
        for row in self.cursor.fetchall():
            print(row)


        print("\nStudents:")
        self.cursor.execute("SELECT * FROM student")
        for row in self.cursor.fetchall():
            print(row)


        print("\nCourses:")
        self.cursor.execute("SELECT * FROM course")
        for row in self.cursor.fetchall():
            print(row)


        print("\nTasks:")
        self.cursor.execute("SELECT * FROM tasks")
        for row in self.cursor.fetchall():
            print(row)


        print("\nTask Completions:")
        self.cursor.execute("SELECT * FROM task_completing")
        for row in self.cursor.fetchall():
            print(row)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    db_manager = DatabaseManager('Google Classroom.db')
    db_manager.create_tables()
    db_manager.insert_data()
    db_manager.execute_select_queries()
    db_manager.close_connection()