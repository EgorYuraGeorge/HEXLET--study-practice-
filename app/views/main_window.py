import sys
from datetime import datetime
from PySide6 import QtWidgets, QtCore, QtGui
from app.controllers.tasks_controller import TaskController

class TaskManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.task_controller = TaskController()
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # Центральный виджет
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Панель инструментов
        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)
        
        # Кнопки
        self.add_action = toolbar.addAction("Добавить")
        self.add_action.triggered.connect(self.show_add_dialog)
        
        self.edit_action = toolbar.addAction("Редактировать")
        self.edit_action.triggered.connect(self.show_edit_dialog)
        
        self.delete_action = toolbar.addAction("Удалить")
        self.delete_action.triggered.connect(self.delete_selected_task)
        
        # Таблица задач
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Описание", "Срок", "Приоритет", "Статус"
        ])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

    def load_tasks(self):
        """Загрузка задач в таблицу"""
        tasks = self.task_controller.get_tasks()
        self.table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.id)))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(task.title))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(task.description or ""))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(
                task.due_date.strftime("%d.%m.%Y") if task.due_date else ""))
            self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(task.priority))
            self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(task.status))

    def show_add_dialog(self):
        """Диалог добавления задачи"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Новая задача")
        
        layout = QtWidgets.QFormLayout(dialog)
        
        # Поля ввода
        title_edit = QtWidgets.QLineEdit()
        desc_edit = QtWidgets.QTextEdit()
        date_edit = QtWidgets.QDateEdit()
        date_edit.setMinimumDate(QtCore.QDate.currentDate())
        priority_combo = QtWidgets.QComboBox()
        priority_combo.addItems(["low", "medium", "high"])
        
        # Кнопки
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        # Добавляем элементы
        layout.addRow("Название:", title_edit)
        layout.addRow("Описание:", desc_edit)
        layout.addRow("Срок выполнения:", date_edit)
        layout.addRow("Приоритет:", priority_combo)
        layout.addRow(buttons)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                self.task_controller.create_task(
                    title=title_edit.text(),
                    description=desc_edit.toPlainText(),
                    due_date=date_edit.date().toPython(),
                    priority=priority_combo.currentText()
                )
                self.load_tasks()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def show_edit_dialog(self):
        """Диалог редактирования задачи"""
        selected = self.table.currentRow()
        if selected == -1:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите задачу для редактирования")
            return
            
        task_id = int(self.table.item(selected, 0).text())
        task = self.task_controller.get_tasks()[selected]
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Редактирование задачи")
        
        layout = QtWidgets.QFormLayout(dialog)
        
        # Поля ввода с текущими значениями
        title_edit = QtWidgets.QLineEdit(task.title)
        desc_edit = QtWidgets.QTextEdit(task.description or "")
        date_edit = QtWidgets.QDateEdit()
        if task.due_date:
            date_edit.setDate(QtCore.QDate(task.due_date.year, task.due_date.month, task.due_date.day))
        priority_combo = QtWidgets.QComboBox()
        priority_combo.addItems(["low", "medium", "high"])
        priority_combo.setCurrentText(task.priority)
        
        # Кнопки
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        # Добавляем элементы
        layout.addRow("Название:", title_edit)
        layout.addRow("Описание:", desc_edit)
        layout.addRow("Срок выполнения:", date_edit)
        layout.addRow("Приоритет:", priority_combo)
        layout.addRow(buttons)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            try:
                self.task_controller.update_task(
                    task_id,
                    title=title_edit.text(),
                    description=desc_edit.toPlainText(),
                    due_date=date_edit.date().toPython() if date_edit.date().isValid() else None,
                    priority=priority_combo.currentText()
                )
                self.load_tasks()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def delete_selected_task(self):
        """Удаление выбранной задачи"""
        selected = self.table.currentRow()
        if selected == -1:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления")
            return
            
        task_id = int(self.table.item(selected, 0).text())
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите удалить эту задачу?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.task_controller.delete_task(task_id)
                self.load_tasks()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
