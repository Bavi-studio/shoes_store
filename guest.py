from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from database import ProductDatabase
from admin import BaseProductWindow

class GuestWindow(BaseProductWindow):
    """
    Окно Гостя. Предоставляет доступ только к просмотру каталога с заголовком "Заказы".
    Поиск, фильтрация и сортировка отключены.
    """
    def __init__(self, db_connector: ProductDatabase, user_full_name: str, user_role: str): 
        # Принимает 4 аргумента, исправляя предыдущий TypeError
        super().__init__(db_connector, "Гость", "Гость", "Гость: Просмотр")
        
        self.enable_edit = False 
        
        self.create_top_panel()
        self.create_search_panel() # <--- Вызываем переопределенный метод (только заголовок "Заказы")
        self.create_scroll_area()
        self.load_products() 

    def load_products(self):
        self.display_products(self.products_data, enable_click=self.enable_edit)

    def open_edit_window(self, product_data):
        pass 
    
    # --- Переопределение для отображения только заголовка "Заказы" ---
    
    def create_search_panel(self):
        """Создает минимальную панель, содержащую только заголовок 'Заказы'."""
        search_frame = QFrame()
        # Добавляем небольшой внутренний отступ для заголовка
        search_frame.setStyleSheet("background-color: #F0F0F0; padding: 5px; color: black;") 

        v_layout = QVBoxLayout(search_frame)
        v_layout.setContentsMargins(10, 5, 10, 5) 
        v_layout.setSpacing(0)
        
        # --- ОБНОВЛЕННЫЙ ЗАГОЛОВОК "Заказы" (Размер 24) ---
        orders_header = QLabel("Каталог")
        orders_header.setAlignment(Qt.AlignCenter)
        orders_header.setFont(QFont("Arial", 24, QFont.Bold)) # Заголовок 24 пункта
        orders_header.setStyleSheet("color: black;")
        v_layout.addWidget(orders_header)
        # --------------------------------------------------
        
        self.main_layout.addWidget(search_frame) 

    # --- Отключаем методы управления, которые могут быть вызваны из BaseProductWindow ---

    def on_search_changed(self, text):
        pass
        
    def on_supplier_changed(self, supplier):
        pass
        
    def on_sort_changed(self, index):
        pass