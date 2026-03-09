from PySide6.QtWidgets import QMainWindow
# Импортируем ProductDatabase для работы с базой
from database import ProductDatabase 
# Импортируем базовый класс и ProductCard из admin.py
from admin import BaseProductWindow 

class ManagerWindow(BaseProductWindow):
    """
    Окно менеджера, наследует все функции отображения, 
    поиска, фильтрации и сортировки от BaseProductWindow, 
    но отключает возможности редактирования и добавления.
    """
    def __init__(self, db_connector: ProductDatabase, user_full_name: str, user_role: str):
        # Вызываем конструктор базового класса
        super().__init__(db_connector, user_full_name, user_role, f"{user_role}: Просмотр и фильтрация")
        
        # --- Ключевые изменения для Менеджера ---
        # 1. Отключаем возможность клика по карточке для редактирования
        self.enable_edit = False 

        # 2. Создаем основные элементы
        self.create_top_panel()
        self.create_search_panel() # Менеджеру доступны Сортировка и Фильтр
        self.create_scroll_area()
        # 3. НЕ ВЫЗЫВАЕМ self.create_bottom_controls(), чтобы убрать кнопку "Добавить"
        
        self.load_products() 

    def load_products(self):
        """Загружает и отображает товары, передавая enable_edit=False."""
        self.display_products(self.products_data, enable_click=self.enable_edit)

    def open_edit_window(self, product_data):
        """Переопределяем метод: менеджер не может открывать окно редактирования."""
        pass
