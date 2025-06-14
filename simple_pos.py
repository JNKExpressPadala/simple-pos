import sqlite3

# === Initialize the database ===
def init_db():
    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        barcode TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        cost REAL NOT NULL,
        stock INTEGER NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()

# === Add a product to the database ===
def add_product():
    barcode = input("Enter barcode: ")
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    cost = float(input("Enter cost: "))
    stock = int(input("Enter stock quantity: "))

    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?)",
                   (barcode, name, price, cost, stock))

    conn.commit()
    conn.close()
    print("✅ Product added!")

# === Record a sale ===
def sell_product():
    barcode = input("Enter barcode: ")
    quantity = int(input("Enter quantity: "))

    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, price, cost, stock FROM products WHERE barcode = ?", (barcode,))
    product = cursor.fetchone()

    if product:
        name, price, cost, stock = product
        if stock >= quantity:
            cursor.execute("UPDATE products SET stock = stock - ? WHERE barcode = ?", (quantity, barcode))
            cursor.execute("INSERT INTO sales (barcode, quantity) VALUES (?, ?)", (barcode, quantity))
            conn.commit()
            print(f"🛒 Sold {quantity} x {name}")
            print(f"💵 Total: ₱{price * quantity:.2f}")
            print(f"📈 Profit: ₱{(price - cost) * quantity:.2f}")
        else:
            print("❌ Not enough stock!")
    else:
        print("❌ Product not found!")

    conn.close()

# === View inventory ===
def view_inventory():
    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n📦 Inventory:")
    print("Barcode\t\tName\t\tPrice\tCost\tStock")
    for p in products:
        print(f"{p[0]}\t{p[1]}\t{p[2]}\t{p[3]}\t{p[4]}")
    conn.close()

# === Main Menu ===
def main():
    init_db()
    while True:
        print("\n=== Simple POS ===")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. View Inventory")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            sell_product()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
