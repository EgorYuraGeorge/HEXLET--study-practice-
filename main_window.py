import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QSize


class TableApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Таблица статусов")
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: gray;")


        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setRowCount(10)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Статус", "Дата", "Приоритет", "Автор", "Описание", "Удалить"])
        self.table_widget.setMinimumSize(QSize(645, 310)) # type: ignore


        self.table_widget.setStyleSheet("""
            QTableWidget {
                border: 2px solid gray;
                background-color: white;
                font-size: 14px;  /* Размер шрифта элементов таблицы */
            }
            QTableWidget::item {
                color: green;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                font-size: 14px;  /* Размер шрифта заголовков */
            }
        """)

        self.fill_table()


        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table_widget, alignment=QtCore.Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)

    def fill_table(self):

        data = [
            ["Завершено", "25.05.2025", "Средний", "MJ", "Подать заявку"],
            ["Ожидание", "24.05.2025", "Средний", "MJ", "Создание макета"],
            ["В работе", "24.05.2025", "Средний", "MJ", "Проверка ТЗ"],
            ["Завершено", "25.05.2025", "Низкий", "MJ", "Отчет о проекте"],
            ["В ожидании", "30.05.2025", "Высокий", "MJ", "Анализ данных"],
            ["Завершено", "26.05.2025", "Средний", "MJ", "Документация"],
            ["Ожидание", "28.05.2025", "Низкий", "MJ", "Исследование"],
            ["В работе", "29.05.2025", "Средний", "MJ", "Дизайн"],
            ["Завершено", "31.05.2025", "Высокий", "MJ", "Тестирование"],
            ["Ожидание", "25.06.2025", "Низкий", "MJ", "Презентация"],
        ]


        for row, (status, date, priority, author, description) in enumerate(data):
            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(status))
            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(date))
            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(priority))
            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(author))
            self.table_widget.setItem(row, 4, QtWidgets.QTableWidgetItem(description))

            if row == 0:
                for col_index in range(5):
                    item = self.table_widget.item(row, col_index)
                    item.setForeground(QtGui.QColor("gray"))
            elif row == 1:
                for col_index in range(5):
                    item = self.table_widget.item(row, col_index)
                    item.setForeground(QtGui.QColor("red"))
            elif row == 2:
                for col_index in range(5):
                    item = self.table_widget.item(row, col_index)
                    item.setForeground(QtGui.QColor("green"))


            delete_button = QtWidgets.QPushButton("🗑️")
            delete_button.setFixedSize(30, 30)
            self.table_widget.setCellWidget(row, 5, delete_button)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TableApp()
    window.show()
    sys.exit(app.exec())