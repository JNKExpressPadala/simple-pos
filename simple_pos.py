import sqlite3

# Initialize the database
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
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Add product
def add_product():
    barcode = input("Barcode: ")
    name = input("Name: ")
    price = float(input("Price: "))
    cost = float(input("Cost: "))
    stock = int(input("Stock: "))

    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?)", (barcode, name, price, cost, stock))
    conn.commit()
    conn.close()
    print("✅ Product added.")

# Sell product
def sell_product():
    barcode = input("Enter barcode: ")
    qty = int(input("Enter quantity: "))

    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, cost, stock FROM products WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()

    if result:
        name, price, cost, stock = result
        if stock < qty:
            print("❌ Not enough stock.")
        else:
            new_stock = stock - qty
            cursor.execute("UPDATE products SET stock = ? WHERE barcode = ?", (new_stock, barcode))
            cursor.execute("INSERT INTO sales (barcode, quantity) VALUES (?, ?)", (barcode, qty))
            conn.commit()
            print(f"✅ Sold {qty} x {name}")
            print(f"💵 Revenue: ${price * qty:.2f}, Profit: ${(price - cost) * qty:.2f}")
    else:
        print("❌ Product not found.")

    conn.close()

# Show inventory
def view_inventory():
    conn = sqlite3.connect("simple_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[1]} | Barcode: {row[0]} | Price: ${row[2]} | Stock: {row[4]}")
    conn.close()

# Main menu
def main():
    init_db()
    while True:
        print("\n=== Simple POS ===")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. View Inventory")
        print("4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            sell_product()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()