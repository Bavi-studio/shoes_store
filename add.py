import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QDoubleSpinBox, QSpinBox,
    QFrame,
    QFileDialog 
)
from PySide6.QtCore import Qt, QSize, Signal 
from PySide6.QtGui import QPixmap


class AddProductWindow(QWidget):
    """Окно для добавления нового товара с компактным дизайном."""
    
    product_added = Signal() 

    def __init__(self, db_connector=None, parent=None):
        super().__init__()
        self.parent = parent
        self.db = db_connector 
        self.image_path = "" 
        self.setWindowTitle("Добавление")
        self.setFixedSize(650, 400) 
        self.setup_ui()

    def setup_ui(self):
        # Главный горизонтальный макет: [Изображение] | [Поля ввода и Кнопки]
        main_h_layout = QHBoxLayout(self) 
        main_h_layout.setContentsMargins(10, 10, 10, 10)
        main_h_layout.setSpacing(15)
        
        # --- ЛЕВАЯ ЧАСТЬ: Изображение и Управление Фото ---
        image_v_layout = QVBoxLayout()
        image_v_layout.setAlignment(Qt.AlignTop)
        
        # Заглушка для изображения
        self.image_label = QLabel("Нет фото")
        self.image_label.setFixedSize(QSize(250, 250))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f8f8f8;")
        
        upload_btn = QPushButton("Загрузить фото")
        upload_btn.clicked.connect(self.select_image)

        image_v_layout.addWidget(self.image_label)
        image_v_layout.addWidget(upload_btn)
        image_v_layout.addStretch() 
        
        main_h_layout.addLayout(image_v_layout)

        # --- ПРАВАЯ ЧАСТЬ: Поля ввода и Кнопки ---
        fields_v_layout = QVBoxLayout()
        
        # 1. Сетка для полей ввода (компактное размещение)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        # Поля ввода
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        
        # --- НОВОЕ: Поле поставщика теперь QComboBox, заполняется из БД ---
        self.supplier_input = QComboBox() 
        if self.db:
            suppliers = self.db.get_all_suppliers()
            self.supplier_input.addItems(suppliers)
        else:
            self.supplier_input.addItems(["Поставщик А", "Поставщик Б", "Поставщик В"]) 
        # ------------------------------------------------------------------
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["пара", "шт.", "уп.", "кг"])
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 1000000.00)
        self.price_input.setDecimals(2)
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 9999)
        self.discount_input = QSpinBox()
        self.discount_input.setRange(0, 100)
        
        # Размещение в сетке (QLabel, QWidget)
        row = 0
        def add_field(label_text, widget):
            nonlocal row
            grid_layout.addWidget(QLabel(label_text), row, 0)
            grid_layout.addWidget(widget, row, 1)
            row += 1

        add_field("Название:", self.name_input)
        add_field("Категория:", self.category_input)
        add_field("Описание:", self.description_input)
        add_field("Производитель:", self.manufacturer_input)
        add_field("Поставщик:", self.supplier_input)
        add_field("Единица:", self.unit_combo)
        add_field("Цена (руб.):", self.price_input)
        add_field("На складе:", self.stock_input)
        add_field("Скидка (%):", self.discount_input)

        fields_v_layout.addLayout(grid_layout)
        fields_v_layout.addStretch() 

        # 2. Кнопки "Назад" и "Сохранить"
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Назад")
        save_btn = QPushButton("Сохранить")
        
        back_btn.clicked.connect(self.close) 
        save_btn.clicked.connect(self.save_product)

        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)
        fields_v_layout.addLayout(btn_layout)
        
        main_h_layout.addLayout(fields_v_layout)

    def select_image(self):
        """Открывает диалог выбора файла, сохраняет путь и отображает изображение."""
        file_filter = "Изображения (*.png *.jpg *.jpeg *.bmp)"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выбрать фотографию товара", 
            "", 
            file_filter
        )
        
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(self.image_path)
            
            if not pixmap.isNull():
                # Масштабирование и отображение изображения в image_label
                self.image_label.setPixmap(
                    pixmap.scaled(
                        self.image_label.size(), 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                )
                self.image_label.setText("") 
            else:
                self.image_path = ""
                self.image_label.setText("Ошибка загрузки фото")
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение.")


    def save_product(self):
        """
        Сохранение данных в базу данных через db_connector.
        """
        
        # Валидация (минимум)
        if not self.name_input.text() or not self.category_input.text():
            QMessageBox.warning(self, "Предупреждение", "Поля 'Название' и 'Категория' не могут быть пустыми.")
            return
            
        if not self.db:
            QMessageBox.critical(self, "Ошибка", "Отсутствует подключение к базе данных.")
            return

        new_product_data = {
            'name': self.name_input.text(),
            'category': self.category_input.text(),
            'description': self.description_input.text(),
            'manufacturer': self.manufacturer_input.text(),
            # --- ИЗМЕНЕНИЕ: Используем currentText() для QComboBox ---
            'supplier': self.supplier_input.currentText(),
            # --------------------------------------------------------
            'unit': self.unit_combo.currentText(),
            'price': self.price_input.value(),
            'stock_quantity': self.stock_input.value(),
            'discount_percent': self.discount_input.value(),
            "image": self.image_path 
        }

        # <-- СОХРАНЕНИЕ ЧЕРЕЗ БД -->
        if self.db.add_product(new_product_data):
            QMessageBox.information(self, "Уведомление", f"Товар '{new_product_data['name']}' успешно добавлен в БД.")
            
            # 1. Отправляем сигнал об успешном добавлении
            self.product_added.emit()
            
            # 2. Закрываем окно
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка БД", "Не удалось добавить товар в базу данных.")
            
# Блок запуска оставлен без изменений
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddProductWindow()
    window.show()
    sys.exit(app.exec())