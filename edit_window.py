# edit_window.py (Полностью исправленный)
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QFileDialog, QSpinBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class EditProductWindow(QDialog):
    # ИЗМЕНЕНИЕ: Добавлен аргумент db_connector для соответствия вызову из AdminWindow
    def __init__(self, product_data=None, db_connector=None, parent=None):
        super().__init__(parent)
        
        self.db = db_connector 

        self.setWindowTitle("Редактирование товара")
        self.setMinimumWidth(400)

        self.product_data = product_data  # Словарь с исходными данными
        self.image_path = product_data.get('image') if product_data else None 
        
        main_layout = QVBoxLayout(self)

        # --- Поле Название ---
        main_layout.addWidget(QLabel("Название товара:"))
        self.name_edit = QLineEdit()
        main_layout.addWidget(self.name_edit)

        # --- Поле Описание ---
        main_layout.addWidget(QLabel("Описание:"))
        self.desc_edit = QTextEdit()
        main_layout.addWidget(self.desc_edit)

        # --- Поставщик ---
        main_layout.addWidget(QLabel("Поставщик:"))
        self.supplier_combo = QComboBox()
        
        # --- НОВОЕ: Загрузка поставщиков из БД ---
        if self.db:
            suppliers = self.db.get_all_suppliers()
            self.supplier_combo.addItems(suppliers)
        else:
            # Если БД недоступна, используем заглушки
            self.supplier_combo.addItems(["Поставщик А", "Поставщик B", "Поставщик C"])
        # ------------------------------------------

        main_layout.addWidget(self.supplier_combo)

        # --- Количество ---
        main_layout.addWidget(QLabel("Количество на складе:"))
        self.count_spin = QSpinBox()
        self.count_spin.setRange(0, 100000)
        main_layout.addWidget(self.count_spin)

        # --- Цена ---
        main_layout.addWidget(QLabel("Цена:"))
        self.price_edit = QLineEdit()
        main_layout.addWidget(self.price_edit)

        # --- Фото товара ---
        img_layout = QHBoxLayout()
        main_layout.addLayout(img_layout)

        self.photo_label = QLabel("Нет изображения")
        self.photo_label.setFixedSize(120, 120)
        self.photo_label.setStyleSheet("border: 1px solid gray; background: #f0f0f0;")
        self.photo_label.setAlignment(Qt.AlignCenter)
        img_layout.addWidget(self.photo_label)

        choose_btn = QPushButton("Выбрать фото")
        choose_btn.clicked.connect(self.choose_image)
        img_layout.addWidget(choose_btn)

        # --- Нижние кнопки ---
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)

        # Заполняем данными если пришли
        if product_data:
            self.load_data(product_data)

    # ----------------------------------------------------------------

    def choose_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.image_path = path
            pixmap = QPixmap(path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)

    # ----------------------------------------------------------------

    def load_data(self, data: dict):
        """Заполнение окна текущими данными карточки"""
        self.name_edit.setText(data.get("name", ""))
        self.desc_edit.setPlainText(data.get("description", ""))
        self.price_edit.setText(str(data.get("price", "")))
        self.count_spin.setValue(data.get("stock_quantity", 0))

        # --- ИЗМЕНЕНИЕ: Теперь список заполняется из БД, поиск значения ---
        supplier = data.get("supplier")
        if supplier in [self.supplier_combo.itemText(i) for i in range(self.supplier_combo.count())]:
            self.supplier_combo.setCurrentText(supplier)
        # ------------------------------------------------------------------

        image = data.get("image")
        if image:
            pixmap = QPixmap(image).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)

    # ----------------------------------------------------------------

    def get_result(self):
        """
        Возвращает результат для сохранения, включая все обязательные поля
        из исходных данных для корректной работы SQL-запроса UPDATE.
        """
        
        # Используем исходные данные (self.product_data), чтобы получить поля,
        # которые не редактируются в этой форме (category, manufacturer, unit, discount_percent).
        original_data = self.product_data if self.product_data else {}
        
        return {
            "name": self.name_edit.text(),
            
            # НЕРЕДАКТИРУЕМЫЕ ПОЛЯ (для SQL):
            "category": original_data.get("category", ""), 
            "manufacturer": original_data.get("manufacturer", ""),
            "unit": original_data.get("unit", "шт."),            
            "discount_percent": original_data.get("discount_percent", 0), 
            
            # РЕДАКТИРУЕМЫЕ ПОЛЯ:
            "description": self.desc_edit.toPlainText(),
            "supplier": self.supplier_combo.currentText(), # Используем текущий текст из QComboBox
            "stock_quantity": self.count_spin.value(),
            "price": self.price_edit.text(),
            "image": self.image_path
        }