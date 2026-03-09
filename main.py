import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from database import ProductDatabase, DatabaseConnectionError

# Импорт окон
from auth import AuthWindow

# Импортируйте все классы окон, которые будут использоваться для маршрутизации
from admin import AdminWindow
from manager import ManagerWindow
from user import UserWindow
from guest import GuestWindow 


def run_application():
    """Главная функция для запуска приложения."""
    app = QApplication(sys.argv)
    db_connector = ProductDatabase()
    app.setWindowIcon(QIcon("Icon.jpg"))  # Путь к вашей иконке

    try:
        # Установка соединения с базой данных
        if not db_connector.connect():
             QMessageBox.critical(None, "Ошибка подключения", "Не удалось установить соединение с базой данных.")
             sys.exit(1)
        
 
        # -----------------------------------------------

        # Опционально: Инициализация таблиц и начальных пользователей при первом запуске
        # Если вы не использовали SQL-скрипт, раскомментируйте эту строку:
        # db_connector.create_initial_roles_and_users()

    except DatabaseConnectionError as e:
        QMessageBox.critical(None, "Ошибка подключения к БД", f"Не удалось подключиться: {e}")
        sys.exit(1) 

    # --- ЦИКЛ АУТЕНТИФИКАЦИИ И МАРШРУТИЗАЦИИ ---
    while True:
        auth_window = AuthWindow(db_connector)

        # Запускаем окно авторизации
        if auth_window.exec() == QDialog.Accepted:
            
            # Получаем данные пользователя из AuthWindow
            user_role = getattr(auth_window, 'user_role', 'guest')
            user_full_name = getattr(auth_window, 'user_full_name', 'Гость')

            current_window = None

            # --- МАРШРУТИЗАЦИЯ ПО РОЛЯМ ---
            if user_role == 'Администратор':
                current_window = AdminWindow(db_connector, user_full_name, user_role)
                
            elif user_role == 'Менеджер':
                current_window = ManagerWindow(db_connector, user_full_name, user_role)
                
            # Обрабатываем роли 'Пользователь' и 'Клиент' одинаково
            elif user_role == 'Пользователь' or user_role == 'Клиент': 
                current_window = UserWindow(db_connector, user_full_name, user_role)
                
            elif user_role == 'guest':
                current_window = GuestWindow(db_connector, user_full_name, user_role)
            
            else:
                # На случай, если роль из БД не соответствует ожидаемым
                QMessageBox.critical(None, "Ошибка роли", f"Неизвестная роль пользователя: {user_role}")
                continue  # Возвращаемся к окну авторизации

            # Запускаем окно, соответствующее роли
            current_window.show()
            app.exec() 
            
            # Проверяем, был ли запрошен выход из аккаунта (а не закрытие приложения)
            if not current_window.logout_requested:
                # Если выход не запрошен, значит, приложение закрыто полностью
                break
                
        else:
            # Если окно авторизации закрыто (нажата 'Отмена' или крестик), выходим
            break
            
    db_connector.close()
    sys.exit()


if __name__ == '__main__':
    run_application()