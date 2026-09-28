import sqlite3

# ----------------- DATABASE SETUP -----------------
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    # Books table banayein
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
        )
    """)
    conn.commit()
    conn.close()

# ----------------- FUNCTIONS -----------------
def add_book():
    title = input("\nKitab ka naam (Title) dalein: ").strip()
    author = input("Author ka naam dalein: ").strip()

    if not title or not author:
        print("Kitab aur Author ka naam khali nahi ho sakta!")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, status) VALUES (?, ?, 'Available')", (title, author))
    conn.commit()
    conn.close()
    print(f"'{title}' ko library me safaltapoorvak add kar diya gaya hai.")

def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, status FROM books")
    books = cursor.fetchall()
    conn.close()

    if not books:
        print("\nLibrary me abhi koi kitab nahi hai.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<5} | {'Title':<25} | {'Author':<20} | {'Status':<10}")
    print("=" * 65)
    for b in books:
        print(f"{b[0]:<5} | {b[1]:<25} | {b[2]:<20} | {b[3]:<10}")
    print("=" * 65)

def issue_book():
    view_books()
    try:
        book_id = int(input("\nIssue karne ke liye Book ID dalein: "))
    except ValueError:
        print("Kripya sahi number dalein!")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()

    if not row:
        print("Is ID ki koi kitab nahi mili.")
    elif row[0] == "Issued":
        print("Ye kitab pehle se kisi ko di ja chuki hai (Already Issued).")
    else:
        cursor.execute("UPDATE books SET status = 'Issued' WHERE id = ?", (book_id,))
        conn.commit()
        print("Kitab safaltapoorvak Issue kar di gayi hai.")
    conn.close()

def return_book():
    try:
        book_id = int(input("\nWapas karne ke liye Book ID dalein: "))
    except ValueError:
        print("Kripya sahi number dalein!")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()

    if not row:
        print("Is ID ki koi kitab nahi mili.")
    elif row[0] == "Available":
        print("Ye kitab pehle se hi library me jama hai (Not Issued).")
    else:
        cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
        conn.commit()
        print("Kitab safaltapoorvak Return ho gayi hai.")
    conn.close()

def delete_book():
    try:
        book_id = int(input("\nDelete karne ke liye Book ID dalein: "))
    except ValueError:
        print("Kripya sahi number dalein!")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()

    if not row:
        print("Is ID ki koi kitab nahi mili.")
    else:
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        print(f"'{row[0]}' ko library se delete kar diya gaya.")
    conn.close()

# ----------------- MAIN MENU -----------------
def main():
    init_db()
    while True:
        print("\n" + "*" * 35)
        print("  LIBRARY MANAGEMENT SYSTEM")
        print("*" * 35)
        print("1. Nayi Kitab Add Karein")
        print("2. Sabhi Kitabein Dekhein")
        print("3. Kitab Issue Karein")
        print("4. Kitab Return Karein")
        print("5. Kitab Delete Karein")
        print("6. Exit")

        choice = input("\nApna option chunein (1-6): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("\nProgram band ho raha hai. Dhanyawad!")
            break
        else:
            print("Galat option! Kripya 1 se 6 ke beech number chunein.")

if __name__ == "__main__":
    main()
