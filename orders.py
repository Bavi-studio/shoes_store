import psycopg2, os
from PySide6.QtWidgets import (
    QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QScrollArea, QSizePolicy, QGridLayout,
    QMessageBox, QLineEdit, QDialog
)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QScrollArea, QSizePolicy
)
# Импорт коннектора БД
from database import ProductDatabase, DatabaseConnectionError

class OrderCard(QFrame):
    """Карточка заказа с динамическим отображением всех полей."""
    def __init__(self, order_data: dict, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(140)
        self.setStyleSheet("""
            background-color: #F0FFF0;
            color: black;  /* задаём цвет текста */
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        # словарь соответствий ключей в словаре заказа → русская надпись
        RUS_LABELS = {
            "order_number": "Номер заказа",
            "status": "Статус",
            "address": "Адрес",
            "order_date": "Дата заказа",
            "delivery_date": "Дата выдачи"
        }

        for key, value in order_data.items():
            display_value = value if value is not None else "Не указано"
            label_text = f"{RUS_LABELS.get(key, key)}: {display_value}"
            left_layout.addWidget(QLabel(label_text))
        
        layout.addLayout(left_layout)
        layout.addStretch()



class OrdersWindow(QDialog):
    """Окно заказов с карточками, загружаемыми из базы данных."""
    def __init__(self, db_connector: ProductDatabase, parent=None):
        super().__init__(parent)
        self.db = db_connector
        self.setWindowTitle("Информация о заказах")
        self.setMinimumSize(QSize(800, 600))

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "Icon.JPG")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setStyleSheet("""
            background-color: white;
        """)

        # Прокручиваемая область
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)

        # Кнопка обновления
        # main_layout.addWidget(refresh_btn)
        refresh_btn = QPushButton("Обновить заказы")
        refresh_btn.clicked.connect(self.load_orders)
        refresh_btn.setStyleSheet("""
            background-color: #00FA9A;
            color: black;            /* цвет текста */
            font-weight: bold;       /* можно сделать текст жирным */
            border-radius: 5px;      /* скругление углов */
            padding: 5px 10px;       /* отступы внутри кнопки */
        """)
        main_layout.addWidget(refresh_btn)


        # Загружаем заказы
        self.load_orders()

    def load_orders(self):
        # Очищаем старые карточки
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Берем данные из БД
        orders = self.db.get_all_orders()
        if not orders:
            self.scroll_layout.addWidget(QLabel("Заказы не найдены или ошибка подключения к базе."))
            return

        # Добавляем карточки заказов
        for order in orders:
            # Убедимся, что есть все нужные поля
            if "delivery_date" not in order:
                order["delivery_date"] = "Не указана"
            card = OrderCard(order)
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()


