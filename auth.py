from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from database import AuthDatabase 

class AuthWindow(QDialog):
    def __init__(self, db_connector: AuthDatabase, parent=None):
        super().__init__(parent)
        self.db = db_connector
        
        # Атрибуты, которые используются в main.py для маршрутизации
        self.user_full_name = "" 
        self.user_role = ""
        
        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 250) # Увеличим размер, чтобы вместить новую кнопку

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Вход в систему")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        self.login_btn = QPushButton("Войти")
        self.login_btn.setStyleSheet("background-color: #00FA9A; padding: 5px;")
        self.login_btn.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_btn)

        # --- НОВАЯ КНОПКА "ГОСТЬ" ---
        self.guest_btn = QPushButton("Войти как Гость")
        self.guest_btn.setStyleSheet("background-color: #00FA9A; padding: 5px;")
        self.guest_btn.clicked.connect(self.login_as_guest)
        layout.addWidget(self.guest_btn)
        # -----------------------------

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)

    def check_credentials(self):
        login = self.login_input.text()
        password = self.pass_input.text()
        
        if not self.db.conn:
             QMessageBox.critical(self, "Ошибка БД", "Соединение с базой данных не установлено.")
             return

        user_data = self.db.check_credentials(login, password)

        if user_data:
            self.user_full_name = user_data['full_name']
            self.user_role = user_data['role']
            self.accept()
        else:
            QMessageBox.warning(self, "Предупреждение", "Неверный логин или пароль")
            self.pass_input.clear()
            
    def login_as_guest(self):
        """
        Устанавливает роль "guest" и закрывает окно, 
        сигнализируя main.py о необходимости открыть GuestWindow.
        """
        self.user_full_name = "Гость"
        self.user_role = "guest"
        self.accept()