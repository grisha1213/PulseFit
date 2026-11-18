import sqlite3
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml  

# Автоматически вычисляем пути от текущего файла (src/pulsefit/services/export_service.py)
BASE_DIR = Path(__file__).resolve().parent.parent       # папка src/pulsefit
PROJECT_ROOT = BASE_DIR.parent.parent                   # корень проекта
DB_PATH = BASE_DIR / "database" / "fitpulse.db"         # src/pulsefit/database/fitpulse.db
OUT_DIR = PROJECT_ROOT / "out"                          # папка out в корне проекта


class ExportService:
    def __init__(self, db_path: Path = DB_PATH, out_dir: Path = OUT_DIR):
        self.db_path = db_path
        self.out_dir = out_dir

    def _build_xml(self, parent: ET.Element, data, item_tag: str = "item"):
        """Универсальная рекурсивная сборка XML из словарей и списков."""
        if isinstance(data, list):
            for item in data:
                elem = ET.SubElement(parent, item_tag)
                self._build_xml(elem, item)
        elif isinstance(data, dict):
            for key, value in data.items():
                elem = ET.SubElement(parent, str(key))
                self._build_xml(elem, value)
        else:
            parent.text = "" if data is None else str(data)

    def export_client_subscriptions(self):
        # 1. Создаем папку out, если её нет
        self.out_dir.mkdir(parents=True, exist_ok=True)

        # 2. Извлекаем данные из БД
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    cs.client_subscription_id,
                    cs.start_date,
                    cs.end_date,
                    cs.status,
                    u.user_id,
                    u.name AS user_name,
                    u.surname AS user_surname,
                    u.phone AS user_phone,
                    st.subscription_type_id,
                    st.name AS sub_type_name,
                    st.price AS sub_type_price,
                    st.duration_days AS sub_type_duration
                FROM client_subscriptions cs
                JOIN users u ON cs.user_id = u.user_id
                JOIN subscription_types st ON cs.subscription_type_id = st.subscription_type_id
            """)
            rows = cursor.fetchall()

        # 3. Формируем плоскую (CSV) и вложенную (JSON, XML, YAML) структуры
        flat_data = [dict(row) for row in rows]
        nested_data = [
            {
                "client_subscription_id": row["client_subscription_id"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "status": row["status"],
                "user": {
                    "user_id": row["user_id"],
                    "name": row["user_name"],
                    "surname": row["user_surname"],
                    "phone": row["user_phone"],
                },
                "subscription_type": {
                    "subscription_type_id": row["subscription_type_id"],
                    "name": row["sub_type_name"],
                    "price": row["sub_type_price"],
                    "duration_days": row["sub_type_duration"],
                },
            }
            for row in rows
        ]

        # 4. Сохраняем в 4 формата
        # JSON
        with open(self.out_dir / "data.json", "w", encoding="utf-8") as f:
            json.dump(nested_data, f, ensure_ascii=False, indent=4)

        # CSV
        if flat_data:
            with open(self.out_dir / "data.csv", "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
                writer.writeheader()
                writer.writerows(flat_data)

        # YAML
        with open(self.out_dir / "data.yaml", "w", encoding="utf-8") as f:
            yaml.dump(nested_data, f, allow_unicode=True, sort_keys=False)

        # XML
        root = ET.Element("client_subscriptions")
        self._build_xml(root, nested_data, item_tag="subscription")
        tree = ET.ElementTree(root)
        if hasattr(ET, "indent"):
            ET.indent(tree, space="    ", level=0)
        tree.write(self.out_dir / "data.xml", encoding="utf-8", xml_declaration=True)

        print(f"Готово! Выгружено записей: {len(nested_data)}. Файлы лежат в: {self.out_dir}")


if __name__ == "__main__":
    service = ExportService()
    service.export_client_subscriptions()