from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Ініціалізація бази даних
def init_db():
    with sqlite3.connect("tickets.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                departure_city TEXT NOT NULL,
                destination_city TEXT NOT NULL,
                travel_date TEXT NOT NULL,
                ticket_type TEXT NOT NULL
            )
        """)
        conn.commit()

# Головна сторінка із формою замовлення квитка
@app.route("/", methods=["GET", "POST"])
def order_ticket():
    if request.method == "POST":
        # Отримання даних із форми
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        departure_city = request.form.get("departure_city")
        destination_city = request.form.get("destination_city")
        travel_date = request.form.get("travel_date")
        ticket_type = request.form.get("ticket_type")
        
        # Збереження даних у базу
        with sqlite3.connect("tickets.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tickets (name, email, phone, departure_city, destination_city, travel_date, ticket_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, departure_city, destination_city, travel_date, ticket_type))
            conn.commit()
        
        return render_template(
            "success.html",
            name=name,
            email=email,
            phone=phone,
            departure_city=departure_city,
            destination_city=destination_city,
            travel_date=travel_date,
            ticket_type=ticket_type,
        )
    
    return render_template("form.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
