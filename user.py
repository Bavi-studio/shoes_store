from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from database import ProductDatabase
from admin import BaseProductWindow

class UserWindow(BaseProductWindow):
    def __init__(self, db_connector: ProductDatabase, user_full_name: str, user_role: str):
        super().__init__(db_connector, user_full_name, user_role, f"{user_role}: Просмотр товаров")
        
        # Клиент не может редактировать
        self.enable_edit = False 
        
        self.create_top_panel()
        self.create_search_panel() # <--- Теперь включает заголовок "Заказы"
        self.create_scroll_area()
        self.load_products() 

    def load_products(self):
        self.display_products(self.products_data, enable_click=self.enable_edit)

    def open_edit_window(self, product_data):
        pass 

    ## ✅ ПЕРЕОПРЕДЕЛЕНИЕ: Добавляем только заголовок "Заказы"
    def create_search_panel(self):
        """Создает минимальную панель, содержащую только заголовок 'Заказы'."""
        search_frame = QFrame()
        # Добавляем небольшой внутренний отступ для заголовка
        search_frame.setStyleSheet("background-color: #F0F0F0; padding: 5px; color: black;") 

        v_layout = QVBoxLayout(search_frame)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)
        
        # --- ЗАГОЛОВОК "Заказы" ---
        orders_header = QLabel("Заказы")
        orders_header.setAlignment(Qt.AlignCenter)
        orders_header.setFont(QFont("Arial", 24, QFont.Bold)) # Размер 24
        orders_header.setStyleSheet("color: black;")
        v_layout.addWidget(orders_header)
        # ---------------------------
        
        # Добавляем фрейм в основной макет
        self.main_layout.addWidget(search_frame) 

    ## 🚫 ОБНУЛЯЕМ МЕТОДЫ ФИЛЬТРАЦИИ И СОРТИРОВКИ (на всякий случай)
    def on_search_changed(self, text):
        pass
        
    def on_supplier_changed(self, supplier):
        pass
        
    def on_sort_changed(self, index):
        pass