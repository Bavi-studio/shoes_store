import psycopg2
from typing import Optional, Dict, List, Tuple, Any
from db_config import DB_SETTINGS 

class DatabaseConnectionError(Exception):
    """Исключение для ошибок подключения к БД."""
    pass

class AuthDatabase:
    """Базовый класс для подключения и аутентификации."""
    def __init__(self):
        self.conn: Optional[psycopg2.connection] = None
        self.settings: Dict[str, Any] = DB_SETTINGS

    def connect(self) -> bool:
        """Устанавливает соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(**self.settings)
            print("Успешное подключение к PostgreSQL.")
            return True
        except Exception as e:
            raise DatabaseConnectionError(f"Ошибка подключения к базе данных: {e}") from e

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> None:
        """Выполняет команду SQL (INSERT, UPDATE, CREATE и т.д.)."""
        if not self.conn:
            raise Exception("Соединение с БД не установлено для выполнения запроса.")
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        """Выполняет SELECT и возвращает одну строку."""
        if not self.conn:
            return None
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()
            
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """Выполняет SELECT и возвращает все строки. (Добавлено для удобства)"""
        if not self.conn:
            return []
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception:
            return []


    def check_credentials(self, username: str, password: str) -> Optional[Dict[str, str]]:
        """
        Проверяет пароль, используя 'login', и извлекает имя роли через JOIN.
        """
        if not self.conn:
            return None

        query = """
        SELECT 
            U.password, 
            U.full_name, 
            R.role_name  
        FROM Users U
        JOIN Roles R ON U.role_id = R.id
        WHERE U.login = %s; 
        """
        
        try:
            result = self.fetch_one(query, (username,))

            if result:
                db_password = result[0]
                db_full_name = result[1]
                db_role_name = result[2]

                if db_password == password:
                    return {
                        "full_name": db_full_name,
                        "role": db_role_name 
                    }
                else:
                    return None
            else:
                return None
        except Exception:
            return None


class ProductDatabase(AuthDatabase):
    """Класс для работы с товарами и методами CRUD."""
    
    # ------------------------------------------------------------------
    # --- НОВЫЙ ФУНКЦИОНАЛ ДЛЯ ПОСТАВЩИКОВ ---
    # ------------------------------------------------------------------

    def get_all_suppliers(self) -> List[str]:
        """Извлекает список всех имен поставщиков из базы данных."""
        if not self.conn:
            return []
        try:
            query = "SELECT name FROM suppliers ORDER BY name;"
            results = self.fetch_all(query)
            # Преобразование списка кортежей в список строк
            return [row[0] for row in results]
        except Exception:
            return []
            
    # ------------------------------------------------------------------
    # --- КОНЕЦ НОВОГО ФУНКЦИОНАЛА ---
    # ------------------------------------------------------------------


    def get_all_products(self) -> List[Dict[str, Any]]:
        if not self.conn: return []
        products: List[Dict[str, Any]] = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, name, category, description, manufacturer, supplier, unit, price, stock_quantity, discount_percent, image_path FROM products;")
                records = cur.fetchall()
                for record in records:
                    products.append({
                        'id': record[0], 'name': record[1], 'category': record[2],
                        'description': record[3], 'manufacturer': record[4],
                        'supplier': record[5], 'unit': record[6],
                        'price': float(record[7]), 'stock_quantity': int(record[8]),
                        'discount_percent': int(record[9]), 'image': record[10] if record[10] else ""
                    })
            return products
        except Exception:
            return []

    def add_product(self, data: Dict[str, Any]) -> bool:
        if not self.conn: return False
        try:
            query = "INSERT INTO products (name, category, description, manufacturer, supplier, unit, price, stock_quantity, discount_percent, image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            params = (data['name'], data['category'], data['description'], data['manufacturer'], data['supplier'], data['unit'], data['price'], data['stock_quantity'], data['discount_percent'], data.get('image', ''))
            
            self.execute_query(query, params)
            self.conn.commit()
            return True
        except Exception: 
            self.conn.rollback()
            return False

    def update_product(self, product_id: int, data: Dict[str, Any]) -> bool:
        if not self.conn: return False
        try:
            query = "UPDATE products SET name=%s, category=%s, description=%s, manufacturer=%s, supplier=%s, unit=%s, price=%s, stock_quantity=%s, discount_percent=%s, image_path=%s WHERE id=%s;"
            params = (data['name'], data['category'], data['description'], data['manufacturer'], data['supplier'], data['unit'], data['price'], data['stock_quantity'], data['discount_percent'], data.get('image', ''), product_id)
            
            self.execute_query(query, params)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback() 
            return False
    
    def get_all_orders(self) -> List[Dict[str, Any]]:
        """
        Возвращает список всех заказов с основными данными:
        артикул, статус, адрес из pvz, дата заказа и дата выдачи.
        """
        if not self.conn:
            return []

        orders: List[Dict[str, Any]] = []
        query = """
            SELECT o.order_number, o.status, p.address, o.order_date, o.delivery_date
            FROM orders o
            LEFT JOIN pvz p ON o.pvz_id = p.id
            ORDER BY o.order_date DESC;
        """
        try:
            records = self.fetch_all(query)
            for r in records:
                orders.append({
                    "order_number": r[0],
                    "status": r[1],
                    "address": r[2] or "Не указан",
                    "order_date": r[3],
                    "delivery_date": r[4]
                })
            return orders
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            return []


    def get_order_by_number(self, order_number: str) -> Optional[Dict[str, Any]]:
        """
        Возвращает данные заказа по его артикулу (order_number).
        """
        if not self.conn:
            return None
        try:
            query = """
            SELECT order_number, status, address, order_date
            FROM orders
            WHERE order_number = %s;
            """
            record = self.fetch_one(query, (order_number,))
            if record:
                return {
                    "order_number": record[0],
                    "status": record[1],
                    "address": record[2],
                    "order_date": record[3]
                }
            return None
        except Exception:
            return None