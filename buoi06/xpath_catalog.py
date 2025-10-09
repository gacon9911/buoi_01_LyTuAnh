from lxml import etree
import mysql.connector

# -------------------------------
# 1️⃣ Kiểm tra hợp lệ XML với XSD
# -------------------------------
xml_file = "catalog.xml"
xsd_file = "catalog.xsd"

xml_doc = etree.parse(xml_file)
xsd_doc = etree.parse(xsd_file)
schema = etree.XMLSchema(xsd_doc)

if not schema.validate(xml_doc):
    print("❌ XML KHÔNG hợp lệ!")
    print(schema.error_log)
    exit()

print("✅ XML hợp lệ với XSD, bắt đầu đồng bộ dữ liệu...")

# -------------------------------
# 2️⃣ Tạo database nếu chưa có
# -------------------------------
try:
    temp_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute("CREATE DATABASE IF NOT EXISTS shop")
    temp_conn.close()
    print("✅ Đã kiểm tra và tạo database 'shop' nếu chưa tồn tại.")
except mysql.connector.Error as err:
    print("❌ Lỗi khi tạo database:", err)
    exit()

# -------------------------------
# 3️⃣ Kết nối MySQL và tạo bảng
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shop"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    currency VARCHAR(10) NOT NULL,
    stock INT NOT NULL,
    category_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
)
""")
conn.commit()

# -------------------------------
# 4️⃣ Đọc XML và chèn dữ liệu
# -------------------------------
root = xml_doc.getroot()
ns = {"ns": "http://www.w3schools.com"}

for cat in root.findall(".//ns:category", ns):
    cat_id = cat.get("id")
    cat_name = cat.text.strip() if cat.text else ""

    cursor.execute("""
        INSERT INTO Categories (id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
    """, (cat_id, cat_name))

for prod in root.findall(".//ns:product", ns):
    prod_id = prod.get("id")
    category_ref = prod.get("categoryRef")
    name = prod.findtext("ns:name", default="", namespaces=ns).strip()
    price_elem = prod.find("ns:price", ns)
    price = float(price_elem.text.strip()) if price_elem is not None else 0
    currency = price_elem.get("currency") if price_elem is not None else ""
    stock_text = prod.findtext("ns:stock", default="0", namespaces=ns)
    stock = int(stock_text.strip())

    cursor.execute("""
        INSERT INTO Products (id, name, price, currency, stock, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            price = VALUES(price),
            currency = VALUES(currency),
            stock = VALUES(stock),
            category_id = VALUES(category_id)
    """, (prod_id, name, price, currency, stock, category_ref))

conn.commit()
conn.close()

print("✅ Đồng bộ dữ liệu thành công vào MySQL database 'shop'")