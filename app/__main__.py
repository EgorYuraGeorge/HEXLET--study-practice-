import sys
from PySide6.QtWidgets import QApplication
from app.views.main_window import TaskManagerWindow
from app.models.db import init_db

def main():
    # Инициализация БД
    init_db()
    
    # Создание приложения
    app = QApplication(sys.argv)
    
    # Главное окно
    window = TaskManagerWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()