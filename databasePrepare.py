import sqlite3

def prepare_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("data.db")
    conn.execute("PRAGMA foreign_keys = ON")  # Ensure FK constraints are enforced
    cursor = conn.cursor()




    # Create User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        type TEXT,
        balance REAL DEFAULT 0,
        created TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # Create Product table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        bought_at REAL,
        sell_at REAL,
        quantity INTEGER,
        deposit REAL DEFAULT 0,
        created TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE SET NULL
    )
    """)

    # Create Operation table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Operation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        created TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE SET NULL,
        FOREIGN KEY(product_id) REFERENCES Product(id) ON DELETE SET NULL
    )
    """)

    # Create Service table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Service (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        description TEXT,
        price REAL,
        deposit REAL,
        created TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE SET NULL
    )
    """)

    # Create Transactions table (formerly Deposit)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        created TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES User(id) ON DELETE SET NULL
    )
    """)



    # Commit changes and close the connection
    conn.commit()
    conn.close()

        # Add defualt user to use it as Normal customer
    def check_defualt_customer():
        con = None 
        try:
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute("SELECT name FROM User WHERE name = '-'")
            result = cur.fetchone()
            
            if result is None:
                print(result)
                cur.execute("INSERT INTO User(name, phone, type, balance, created) VALUES ('-','','customer',0.0,CURRENT_TIMESTAMP)")
                con.commit()
        except sqlite3.Error as e:
            print(e)
            # 
        finally:
            if con:
                con.close()
    check_defualt_customer()

    print("All tables created successfully with safe deletion behavior.")
