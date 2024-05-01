from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QLineEdit, QGridLayout, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    # Child init
    def __init__(self):
        # Parent init
        super().__init__()
        # Set title
        self.setWindowTitle("Student Management System")
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        
        # Add menu
        file_menu = self.menuBar().addMenu("&File")
        edit_menu = self.menuBar().addMenu("&Edit")
        help_menu = self.menuBar().addMenu("&Help")
        
        # Add actions to file menu
        add_action = QAction("Add Student", self)
        add_action.triggered.connect(self.insert)
        file_menu.addAction(add_action)
        
        # Add actions to edit menu
        search_action = QAction("Search", self)
        edit_menu.addAction(search_action)
        search_action.triggered.connect(self.search)
        
        # Add actions to help menu
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        # for MAC about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        # Add data table
        self.table = QTableWidget()
        # Add columns
        self.table.setColumnCount(4)
        # Set column names
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # Hide table indexing
        self.table.verticalHeader().setVisible(False)
        # Set table as central widget
        self.setCentralWidget(self.table)
        
        
    def load_data(self):
        # Connect to database
        connection = sqlite3.connect("database.db")
        # Store data in variable
        result = list(connection.execute("SELECT * FROM students"))
        # To not overwrite rows
        self.table.setRowCount(0)
        # Add data to table
        for row_number, row_data in enumerate(result):
            #print(row_number)
            #print(row_data)
            # Add data to table
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                #print(column_number)
                #print(data)
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()
        
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        self.student_to_search = QLineEdit()
        self.student_to_search.setPlaceholderText("Student Name")
        layout.addWidget(self.student_to_search)
        
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        
        self.setLayout(layout)
        
        
    def search(self):
        name = self.student_to_search.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        #print(rows)
        window.table.clearSelection()
        for row in rows:
            items = window.table.findItems(row[1], Qt.MatchFlag.MatchExactly)
            for item in items:
                row_index = item.row()
                for column in range(window.table.columnCount()):
                    window.table.item(row_index, column).setSelected(True)

        
        cursor.close()
        connection.close()


        
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name)
        
        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # Add mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        # Add submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())
    
        
        
