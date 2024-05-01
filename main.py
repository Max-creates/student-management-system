from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QLineEdit, QGridLayout, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem
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
        
        # Add menu
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        
        # Add actions to file menu
        add_action = QAction("Add Student", self)
        file_menu.addAction(add_action)
        
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
        




app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())
    
        
        
