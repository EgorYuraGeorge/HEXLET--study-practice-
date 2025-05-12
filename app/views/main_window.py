import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QToolBar,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox,
    QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import QDate
from app.controllers.tasks_controller import TaskController


class TaskManagerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.task_controller = TaskController()
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self) -> None:
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.add_action = toolbar.addAction("Добавить")
        self.add_action.triggered.connect(self.show_add_dialog)

        self.edit_action = toolbar.addAction("Редактировать")
        self.edit_action.triggered.connect(self.show_edit_dialog)

        self.delete_action = toolbar.addAction("Удалить")
        self.delete_action.triggered.connect(self.delete_selected_task)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Описание", "Срок", "Приоритет", "Статус"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

    def load_tasks(self) -> None:
        tasks = self.task_controller.get_tasks()
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(str(task.id)))
            self.table.setItem(row, 1, QTableWidgetItem(task.title))
            self.table.setItem(row, 2, QTableWidgetItem(task.description or ""))
            self.table.setItem(
                row, 3,
                QTableWidgetItem(
                    task.due_date.strftime("%d.%m.%Y") if task.due_date else ""
                )
            )
            self.table.setItem(row, 4, QTableWidgetItem(task.priority))
            self.table.setItem(row, 5, QTableWidgetItem(task.status))

    def show_add_dialog(self) -> None:
        dialog = QDialog(self)  # type: ignore
        dialog.setWindowTitle("Новая задача")
        layout = QFormLayout(dialog)

        title_edit = QLineEdit()
        desc_edit = QTextEdit()
        date_edit = QDateEdit()
        date_edit.setMinimumDate(QDate.currentDate())
        priority_combo = QComboBox()
        priority_combo.addItems(["low", "medium", "high"])

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow("Название:", title_edit)
        layout.addRow("Описание:", desc_edit)
        layout.addRow("Срок выполнения:", date_edit)
        layout.addRow("Приоритет:", priority_combo)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            try:
                self.task_controller.create_task(
                    title=title_edit.text(),
                    description=desc_edit.toPlainText(),
                    due_date=date_edit.date().toPython(),  # type: ignore
                    priority=priority_combo.currentText()
                )
                self.load_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def show_edit_dialog(self) -> None:
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для редактирования")
            return

        task_id = int(self.table.item(selected, 0).text())  # type: ignore
        task = self.task_controller.get_tasks()[selected]

        dialog = QDialog(self)
        dialog.setWindowTitle("Редактирование задачи")
        layout = QFormLayout(dialog)

        title_edit = QLineEdit(task.title)
        desc_edit = QTextEdit(task.description or "")
        date_edit = QDateEdit()
        if task.due_date:
            date_edit.setDate(QDate(task.due_date.year, task.due_date.month, task.due_date.day))

        priority_combo = QComboBox()
        priority_combo.addItems(["low", "medium", "high"])
        priority_combo.setCurrentText(task.priority)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow("Название:", title_edit)
        layout.addRow("Описание:", desc_edit)
        layout.addRow("Срок выполнения:", date_edit)
        layout.addRow("Приоритет:", priority_combo)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.Accepted:
            try:
                self.task_controller.update_task(
                    task_id,
                    title=title_edit.text(),
                    description=desc_edit.toPlainText(),
                    due_date=date_edit.date().toPython() if date_edit.date().isValid() else None,  # type: ignore
                    priority=priority_combo.currentText()
                )
                self.load_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def delete_selected_task(self) -> None:
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления")
            return

        task_id = int(self.table.item(selected, 0).text())  # type: ignore

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите удалить эту задачу?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.task_controller.delete_task(task_id)
                self.load_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec())
