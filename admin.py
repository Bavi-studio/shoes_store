import sys
import os  # импорт для работы с путями
from PySide6.QtWidgets import QSpacerItem

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER_IMAGE = os.path.join(BASE_DIR, "picture.png")  # заглушка

from PySide6.QtWidgets import (
    QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QPushButton, QScrollArea, QSizePolicy, QGridLayout,
    QMessageBox, QLineEdit, QDialog
)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt, QSize, Signal

# Убедитесь, что эти файлы существуют!
from add import AddProductWindow
from edit_window import EditProductWindow
from auth import AuthWindow
from orders import OrdersWindow

# Импорт коннектора БД
from database import ProductDatabase, DatabaseConnectionError


class ProductCard(QFrame):
    """
    Виджет для отображения информации о товаре.
    Включает логику отображения скидки и кликабельность.
    """
    clicked = Signal(dict)

    def __init__(self, product_data: dict, enable_click: bool, **kwargs):
        super().__init__(**kwargs)
        self.product_data = product_data
        self.enable_click = enable_click

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.setObjectName("productCard")
        self.setStyleSheet("""
            #productCard { background-color: #7FFF00; border: 1px solid black} 
            #productCard QLabel {color: black;}
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(180)

        if self.enable_click:
            self.setCursor(Qt.PointingHandCursor)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)
        main_v_layout.setContentsMargins(0, 0, 0, 0)

        top_h_layout = QHBoxLayout()
        top_h_layout.setContentsMargins(5, 5, 5, 5)
        top_h_layout.setSpacing(10)

        # 1. Фото
        frame_photo = QFrame()
        frame_photo.setFixedSize(QSize(180, 150))
        frame_photo.setFrameShape(QFrame.Box)
        frame_photo.setStyleSheet("background-color: lightgray; border: 0px solid black;")
        photo_layout = QVBoxLayout(frame_photo)
        photo_label = QLabel()
        image_path = self.product_data.get("image", "")
        pixmap = QPixmap(image_path) if image_path else QPixmap(PLACEHOLDER_IMAGE)

        # Если путь некорректный, используем заглушку
        if pixmap.isNull():
            pixmap = QPixmap(PLACEHOLDER_IMAGE)

        photo_label.setPixmap(
            pixmap.scaled(150, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        photo_label.setAlignment(Qt.AlignCenter)
        photo_layout.addWidget(photo_label)
        top_h_layout.addWidget(frame_photo)

        # 2. Основная информация
        frame_info = QFrame()
        frame_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        frame_info.setStyleSheet("background-color: white;")
        info_layout = QGridLayout(frame_info)
        info_layout.setContentsMargins(5, 5, 5, 5)

        data = self.product_data

        title_text = f"{data.get('category', 'Н/Д')} | {data.get('name', 'Н/Д')}"
        title_label = QLabel(title_text)
        title_font = QFont("Arial", 10)
        title_font.setBold(True)
        title_label.setFont(title_font)
        info_layout.addWidget(title_label, 0, 0)

        info_layout.addWidget(QLabel(f"Описание товара: {data.get('description', 'Нет')[:40]}"), 1, 0)
        info_layout.addWidget(QLabel(f"Производитель: {data.get('manufacturer', 'Н/Д')}"), 2, 0)
        info_layout.addWidget(QLabel(f"Поставщик: {data.get('supplier', 'Н/Д')}"), 3, 0)
        info_layout.addWidget(QLabel(f"Единица измерения: {data.get('unit', 'Н/Д')}"), 5, 0)

        # Логика цены со скидкой
        price = float(data.get("price", 0.0) or 0.0)
        discount = float(data.get("discount_percent", 0.0) or 0.0)
        discounted_price = price * (1 - discount / 100)

        if discount > 0:
            double_price_label = QLabel(
                f"<span style='color:red; text-decoration: line-through;'>{price:.2f} руб.</span> "
                f"<span>{discounted_price:.2f} руб.</span>"
            )
        else:
            double_price_label = QLabel(f"{price:.2f} руб.")

        info_layout.addWidget(double_price_label, 4, 0)

        # Количество на складе
        stock_qty = data.get("stock_quantity", 0)
        stock_label = QLabel(f"Количество на складе: {stock_qty}")

        if stock_qty == 0:
            stock_label.setStyleSheet("background-color: #ADD8E6;")

        info_layout.addWidget(stock_label, 6, 0)

        info_layout.setColumnStretch(0, 1)
        top_h_layout.addWidget(frame_info)

        # 3. Фрейм скидки
        discount_frame = QFrame()
        discount_frame.setObjectName("discountFrame")
        discount_frame.setFixedSize(QSize(100, 160))
        discount_frame.setFrameShape(QFrame.NoFrame)
        discount_frame.setLineWidth(0)
        discount_layout = QVBoxLayout(discount_frame)
        discount_layout.setAlignment(Qt.AlignCenter)

        discount = data.get("discount_percent", 0)
        discount_value = QLabel(f"{discount}%")
        discount_font = QFont("Arial", 28)
        discount_font.setBold(True)
        discount_value.setFont(discount_font)
        discount_value.setAlignment(Qt.AlignCenter)

        if discount <= 15:
            discount_frame.setStyleSheet("background-color: white; border: none;")
            discount_value.setStyleSheet("color: red;")
        else:
            discount_frame.setStyleSheet("background-color: #2E8B57; border: none;")
            discount_value.setStyleSheet("color: white;")

        discount_layout.addWidget(discount_value)
        top_h_layout.addWidget(discount_frame)

        main_v_layout.addLayout(top_h_layout)

    def mousePressEvent(self, event):
        if self.enable_click and event.button() == Qt.LeftButton:
            self.clicked.emit(self.product_data)


# --- БАЗОВЫЙ КЛАСС ДЛЯ ВСЕХ ОКОН С ПРОДУКТАМИ ---
class BaseProductWindow(QMainWindow):
    """
    Предоставляет общую структуру (верхняя панель, панель поиска, область прокрутки)
    и общую логику (фильтрация, сортировка, выход).
    """

    def __init__(self, db_connector: ProductDatabase, user_full_name: str, user_role: str, window_title: str):
        super().__init__()
        self.db = db_connector
        self.user_full_name = user_full_name
        self.user_role = user_role
        self.logout_requested = False
        self.setWindowTitle(window_title)
        self.setMinimumSize(QSize(900, 600))

        # --------------------------------------------------------------------------
        # --- ИЗМЕНЕНИЕ: Установка иконки с использованием абсолютного пути ---
        # Вычисляем абсолютный путь к иконке
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_full_path = os.path.join(base_dir, "Icon.JPG")

        # Устанавливаем иконку окна
        self.setWindowIcon(QIcon(self.icon_full_path))
        # --------------------------------------------------------------------------

        self.current_search_text = ""
        self.current_supplier_filter = "Все поставщики"
        self.current_sorting = 0
        self.products_data = self.db.get_all_products()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def logout(self):
        self.logout_requested = True
        self.close()

    def create_top_panel(self):
        admin_top_frame = QFrame()
        admin_top_frame.setStyleSheet("background-color: #00FA9A; color: black;")
        admin_top_layout = QHBoxLayout(admin_top_frame)
        admin_top_layout.setContentsMargins(10, 5, 10, 5)
        admin_top_layout.setSpacing(10)

        logo_label = QLabel()
        # --------------------------------------------------------------------------
        # --- ИЗМЕНЕНИЕ: Использование абсолютного пути для логотипа ---
        pixmap = QPixmap(self.icon_full_path)
        # --------------------------------------------------------------------------
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(40, 40)

        admin_top_layout.addWidget(logo_label)

        # Отображаем ФИО и Роль
        display_text = f"{self.user_full_name} ({self.user_role})"
        admin_info_label = QLabel(display_text)
        admin_info_label.setFont(QFont("Arial", 10))

        logout_btn = QPushButton("Выход")
        logout_btn.setFont(QFont("Arial", 10))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("border: none; background-color: transparent; color: black;")
        logout_btn.clicked.connect(self.logout)

        admin_top_layout.addStretch()
        admin_top_layout.addWidget(admin_info_label)
        admin_top_layout.addWidget(QLabel("|"))
        admin_top_layout.addWidget(logout_btn)

        self.main_layout.addWidget(admin_top_frame)

    def display_products(self, products, enable_click=False):
        """Отображает список товаров в области прокрутки."""
        while self.products_layout.count() > 0:
            item = self.products_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for product in products:
            card = ProductCard(product, enable_click=enable_click)
            if enable_click:
                card.clicked.connect(self.open_edit_window)
            self.products_layout.addWidget(card)

        self.products_layout.addStretch()

    def load_products(self):
        """Метод для загрузки товаров, должен быть переопределен в дочерних классах."""
        pass

    def apply_filters(self):
        """Применяет текущие фильтры и сортировку к отображаемым товарам."""
        products = self.products_data.copy()

        if self.current_search_text:
            products = [
                p for p in products
                if self.current_search_text in p["name"].lower()
                   or self.current_search_text in p["category"].lower()
                   or self.current_search_text in p["description"].lower()
            ]

        if self.current_supplier_filter != "Все поставщики":
            products = [
                p for p in products
                if p["supplier"] == self.current_supplier_filter
            ]

        if hasattr(self, 'sort_combo') and self.current_sorting != 0:
            if self.current_sorting == 1:
                products = sorted(products, key=lambda x: x["stock_quantity"])
            elif self.current_sorting == 2:
                products = sorted(products, key=lambda x: x["stock_quantity"], reverse=True)

        self.display_products(products, enable_click=getattr(self, 'enable_edit', False))

    def on_search_changed(self, text):
        self.current_search_text = text.lower()
        self.apply_filters()

    def update_supplier_filter(self):
        """Обновляет список поставщиков в QComboBox."""
        if not hasattr(self, 'supplier_combo'):
            return

        self.supplier_combo.blockSignals(True)
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Все поставщики")
        suppliers = self.db.get_all_suppliers()
        for s in suppliers:
            self.supplier_combo.addItem(s)
        index = self.supplier_combo.findText(self.current_supplier_filter)
        if index != -1:
            self.supplier_combo.setCurrentIndex(index)
        else:
            self.current_supplier_filter = "Все поставщики"
        self.supplier_combo.blockSignals(False)

    def on_supplier_changed(self, supplier):
        self.current_supplier_filter = supplier
        self.apply_filters()

    def on_sort_changed(self, index):
        self.current_sorting = index
        self.apply_filters()

    def open_orders_window(self):
        win = OrdersWindow(self.db)
        win.exec()

    def create_search_panel(self):
        """Создает панель поиска, фильтрации и сортировки, включая заголовок 'Заказы'."""
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: #F0F0F0; padding: 5px; color: black;")

        v_layout = QVBoxLayout(search_frame)
        v_layout.setContentsMargins(10, 0, 10, 0)
        v_layout.setSpacing(5)

        # --- ГОРИЗОНТАЛЬНЫЙ ЛЕЙАУТ: Кнопка слева, заголовок справа ---
        header_layout = QHBoxLayout()

        # Кнопка "Заказы"
        orders_btn = QPushButton("Заказы")
        orders_btn.setFont(QFont("Arial", 14, QFont.Bold))
        orders_btn.setCursor(Qt.PointingHandCursor)
        orders_btn.setStyleSheet("""
            background-color: #00FA9A;
            border: 2px solid #00FA9A;
            border-radius: 6px;
            padding: 6px 12px;
            color: black;
        """)
        orders_btn.clicked.connect(self.open_orders_window)  # метод для обработки нажатия
        header_layout.addWidget(orders_btn, alignment=Qt.AlignLeft)

        header_layout.addStretch(7)

        # --- ОБНОВЛЕННЫЙ ЗАГОЛОВОК "Заказы" (Размер 24) ---
        orders_header = QLabel("Каталог")
        orders_header.setAlignment(Qt.AlignCenter)
        orders_header.setFont(QFont("Arial", 24, QFont.Bold))  # Увеличение размера шрифта
        orders_header.setStyleSheet("color: black; margin-top: 5px;")
        header_layout.addWidget(orders_header, alignment=Qt.AlignLeft)  # выравниваем рядом с кнопкой

        header_layout.addStretch(8)
        v_layout.addLayout(header_layout)
        # ---------------------------------------------------
        # Панель поиска
        header_layout.addStretch(2)
        title_label = QLabel("Поиск | Фильтр | Сортировка")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 12))
        v_layout.addWidget(title_label)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск...")
        search_input.textChanged.connect(self.on_search_changed)
        v_layout.addWidget(search_input)

        self.supplier_combo = QComboBox()
        self.update_supplier_filter()
        self.supplier_combo.currentTextChanged.connect(self.on_supplier_changed)
        v_layout.addWidget(self.supplier_combo)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Без сортировки", "Количество ↑ (возрастание)", "Количество ↓ (убывание)"])
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        v_layout.addWidget(self.sort_combo)

        self.main_layout.addWidget(search_frame)

    def create_scroll_area(self):
        """Создает область прокрутки для карточек товаров."""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.scroll_widget = QWidget()
        self.products_layout = QVBoxLayout(self.scroll_widget)
        self.products_layout.setAlignment(Qt.AlignTop)
        self.scroll_widget.setStyleSheet("background-color: white;")
        self.products_layout.setSpacing(10)
        self.products_layout.setContentsMargins(10, 10, 10, 10)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def create_bottom_controls(self):
        """Заглушка для нижнего контрольного фрейма."""
        pass


# --- ОКНО АДМИНИСТРАТОРА ---
class AdminWindow(BaseProductWindow):
    """
    Окно Администратора. Наследует все от BaseProductWindow, 
    добавляет кнопку "Добавить" и возможность редактирования (клик по карточке).
    """

    def __init__(self, db_connector: ProductDatabase, user_full_name: str, user_role: str):
        super().__init__(db_connector, user_full_name, user_role, f"{user_role}: Управление Товарами")
        self.enable_edit = True
        self.add_window = None

        self.create_top_panel()
        self.create_search_panel()
        self.create_scroll_area()
        self.create_bottom_controls()  # Добавляем кнопку "Добавить"

        self.load_products()

    def load_products(self):
        self.display_products(self.products_data, enable_click=self.enable_edit)

    def reload_data(self):
        """Перезагружает данные из БД, применяет фильтры и обновляет комбобокс поставщиков."""
        self.products_data = self.db.get_all_products()
        self.apply_filters()
        self.update_supplier_filter()

    def open_add_window(self):
        """Открывает окно добавления товара."""
        self.add_window = AddProductWindow(db_connector=self.db, parent=self)
        self.add_window.product_added.connect(self.reload_data)
        self.add_window.show()

    def open_edit_window(self, product_data):
        """Обрабатывает клик по карточке, открывая окно редактирования."""
        edit_win = EditProductWindow(product_data, self.db, self)
        product_id = product_data.get('id')

        if edit_win.exec() == QDialog.Accepted:
            updated_data = edit_win.get_result()

            # Сохраняем старый путь к изображению, если новый пуст
            if "image" in updated_data and not updated_data["image"]:
                updated_data["image"] = product_data.get("image", "")

            if self.db.update_product(product_id, updated_data):
                QMessageBox.information(self, "Информация", "Продукт успешно обновлен в БД.")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось обновить продукт в БД.")

            self.reload_data()

    def create_bottom_controls(self):
        """Создает нижний фрейм с кнопкой 'Добавить'."""
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("background-color: #00FA9A; padding: 5px; color: black;")

        controls_h_layout = QHBoxLayout(bottom_frame)
        controls_h_layout.setContentsMargins(10, 5, 10, 5)
        controls_h_layout.setSpacing(10)

        add_button = QPushButton("Добавить")
        add_button.setStyleSheet(
            "background-color: #00FA9A; border: 1px solid black; padding: 10px; color: black;"
        )
        add_button.clicked.connect(self.open_add_window)

        controls_h_layout.addWidget(add_button)
        self.main_layout.addWidget(bottom_frame)


if __name__ == '__main__':
    """
    Блок для автономного запуска окна Администратора.
    """
    app = QApplication(sys.argv)

    db_connector = ProductDatabase()

    try:
        db_connector.connect()
    except DatabaseConnectionError as e:
        QMessageBox.critical(None, "Ошибка подключения к БД", f"Не удалось подключиться: {e}")
        sys.exit(1)

        # Эмулируем успешный вход для целей тестирования
    test_user_full_name = "Иванов Иван - Администратор"
    test_user_role = "Администратор"

    admin_window = AdminWindow(db_connector=db_connector, user_full_name=test_user_full_name, user_role=test_user_role)
    admin_window.show()
    sys.exit(app.exec())
