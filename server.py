from flask import Flask, request, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "restaurant.db"

MENU = {
    "Phở Bò": {
        "price": 88,
        "desc": "Rich beef broth, rice noodles, herbs",
        "image": "/static/photos/pho_bo.jpg"
    },
    "Bánh Mì": {
        "price": 45,
        "desc": "Crispy baguette with grilled meat and pickles",
        "image": "/static/photos/banh_mi.jpeg"
    },
    "Bún Thịt Nướng": {
        "price": 78,
        "desc": "Grilled pork, vermicelli, fresh vegetables",
        "image": "/static/photos/bun_thit_nuong.jpeg"
    },
    "Gỏi Cuốn": {
        "price": 42,
        "desc": "Fresh rice paper rolls with herbs",
        "image": "/static/photos/goi_cuon.jpg"
    },
    "Cà Phê Sữa Đá": {
        "price": 32,
        "desc": "Vietnamese iced coffee with condensed milk",
        "image": "/static/photos/ca_phe_sua_da.jpeg"
    },
    "Trà Đá": {
        "price": 12,
        "desc": "Vietnamese iced tea",
        "image": "/static/photos/tra_da.jpeg"
    }
}
STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
    background: #faf5ef;
    color: #2b1d0e;
    margin: 0;
}

.container {
    max-width: 1200px;
    margin: 30px auto;
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.hero {
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
    color: #b45309;
}

.subtitle {
    text-align: center;
    color: #666;
}

.food-card, .card {
    border: 1px solid #f3d7b6;
    padding: 20px;
    border-radius: 16px;
    background: #fffaf3;
    margin-bottom: 15px;
}

.food-card {
    display: flex;
    align-items: center;
    gap: 25px;
}

.food-image {
    width: 220px;
    height: 160px;
    object-fit: cover;
    border-radius: 14px;
    flex-shrink: 0;
}

.food-info {
    flex: 1;
    padding-left: 10px;
}

.food-info h3 {
    margin: 0;
    color: #b45309;
    font-size: 28px;
}

.food-info p {
    margin-top: 10px;
    color: #666;
    font-size: 18px;
}

.food-info strong {
    display: block;
    margin-top: 10px;
    font-size: 24px;
}

.qty-box {
    width: 100px;
    text-align: center;
}

.qty-box input {
    width: 70px;
}

button {
    width: 100%;
    background: #c2410c;
    color: white;
    border: none;
    padding: 14px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
}

button:hover {
    background: #9a3412;
}

input {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-top: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th {
    background: #f97316;
    color: white;
}

td, th {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
}

tr:nth-child(even) {
    background: #fff7ed;
}

.nav {
    text-align: center;
    margin-top: 20px;
}

.nav a {
    color: #dc2626;
    font-weight: bold;
    text-decoration: none;
    margin: 0 10px;
}

@media (max-width: 768px) {

    .food-card {
        flex-direction: column;
        text-align: center;
    }

    .food-image {
        width: 100%;
        height: 220px;
    }

    .qty-box {
        width: 100%;
    }

    .container {
        margin: 10px;
    }

}

</style>
"""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def admin():
    html = """
    {{ style|safe }}
    <div class="container">
        <div class="hero">
            <h1>🍜 Phở Saigon Kitchen</h1>
            <p class="subtitle">Restaurant Admin Portal</p>
        </div>

        <div class="nav">
            <a href="/kitchen">Kitchen Dashboard</a>
            <a href="/sales">Sales Dashboard</a>
        </div>
    </div>
    """
    return render_template_string(html, style=STYLE)


@app.route("/table/<int:table_number>")
def table_menu(table_number):
    html = """
    {{ style|safe }}

    <div class="container">
        <div class="hero">
            <h1>🍜 Phở Saigon Kitchen</h1>
            <p class="subtitle">Fresh Broths • Grilled Meats • Vietnamese Coffee</p>
            <p><strong>Table {{ table_number }}</strong></p>
        </div>

        <form action="/submit_order" method="POST">
            <input type="hidden" name="table_number" value="{{ table_number }}">

            {% for item, info in menu.items() %}
            <div class="food-card">
                <img src="{{ info.image }}" class="food-image">

                <div class="food-info">
                    <h3>{{ item }}</h3>
                    <p>{{ info.desc }}</p>
                    <strong>${{ info.price }}</strong>
                </div>

                <div class="qty-box">
                    <label>Qty</label>
                    <input name="{{ item }}" type="number" value="0" min="0">
                </div>
            </div>
            {% endfor %}

            <button type="submit">Submit Order</button>
        </form>
    </div>
    """

    return render_template_string(
        html,
        table_number=table_number,
        menu=MENU,
        style=STYLE
    )


@app.route("/submit_order", methods=["POST"])
def submit_order():
    table_number = int(request.form["table_number"])
    created_at = datetime.now().isoformat()

    selected_items = []

    for item, info in MENU.items():
        price = info["price"]
        quantity = int(request.form[item])

        if quantity > 0:
            selected_items.append({
                "item": item,
                "quantity": quantity,
                "unit_price": price,
                "total_price": price * quantity
            })

    if len(selected_items) == 0:
        return redirect(f"/table/{table_number}")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (table_number, status, created_at)
        VALUES (?, ?, ?)
    """, (table_number, "New", created_at))

    order_id = cursor.lastrowid

    for selected in selected_items:
        cursor.execute("""
            INSERT INTO order_items
            (order_id, item, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_id,
            selected["item"],
            selected["quantity"],
            selected["unit_price"],
            selected["total_price"]
        ))

    conn.commit()
    conn.close()

    return redirect(f"/order_confirmed/{table_number}/{order_id}")


@app.route("/kitchen")
def kitchen():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, table_number, status, created_at
        FROM orders
        WHERE status != 'Served'
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()
    order_data = []

    for order in orders:
        order_id = order[0]

        cursor.execute("""
            SELECT item, quantity
            FROM order_items
            WHERE order_id = ?
        """, (order_id,))

        items = cursor.fetchall()

        order_data.append({
            "id": order[0],
            "table_number": order[1],
            "status": order[2],
            "created_at": order[3],
            "items": items
        })

    conn.close()

    latest_order_id = order_data[0]["id"] if order_data else 0

    html = """
    {{ style|safe }}

    <div class="container">
        <div class="hero">
            <h1>Kitchen Orders</h1>
            <p class="subtitle">Auto-refreshing every 3 seconds</p>
        </div>

        {% for order in orders %}
        <div class="card">
            <h2>Order #{{ order.id }} · Table {{ order.table_number }}</h2>
            <p>Status: <strong>{{ order.status }}</strong></p>
            <p>Time: {{ order.created_at }}</p>

            <ul>
                {% for item in order["items"] %}
                    <li>{{ item[1] }}x {{ item[0] }}</li>
                {% endfor %}
            </ul>

            <form action="/update_status/{{ order.id }}/Preparing" method="POST">
                <button type="submit">Preparing</button>
            </form>
            <br>

            <form action="/update_status/{{ order.id }}/Ready" method="POST">
                <button type="submit">Ready</button>
            </form>
            <br>

            <form action="/update_status/{{ order.id }}/Served" method="POST">
                <button type="submit">Served</button>
            </form>
        </div>
        {% endfor %}

        <div class="nav">
            <a href="/">Admin</a>
            <a href="/sales">Sales Dashboard</a>
        </div>
    </div>

    <script>
        const latestOrderId = {{ latest_order_id }};
        const previousOrderId = localStorage.getItem("latestOrderId");

        if (previousOrderId !== null && Number(latestOrderId) > Number(previousOrderId)) {
            const audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
            audio.play();
        }

        localStorage.setItem("latestOrderId", latestOrderId);

        setTimeout(function() {
            window.location.reload();
        }, 3000);
    </script>
    """

    return render_template_string(
        html,
        orders=order_data,
        latest_order_id=latest_order_id,
        style=STYLE
    )


@app.route("/update_status/<int:order_id>/<new_status>", methods=["POST"])
def update_status(order_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?
    """, (new_status, order_id))

    conn.commit()
    conn.close()

    return redirect("/kitchen")


@app.route("/sales")
def sales():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(order_items.total_price)
        FROM order_items
        JOIN orders ON order_items.order_id = orders.id
        WHERE orders.status = 'Served'
    """)
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'Served'
    """)
    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT order_items.item, SUM(order_items.quantity), SUM(order_items.total_price)
        FROM order_items
        JOIN orders ON order_items.order_id = orders.id
        WHERE orders.status = 'Served'
        GROUP BY order_items.item
        ORDER BY SUM(order_items.total_price) DESC
    """)
    item_sales = cursor.fetchall()

    conn.close()

    html = """
    {{ style|safe }}

    <div class="container">
        <div class="hero">
            <h1>Sales Dashboard</h1>
            <p class="subtitle">Served orders only</p>
        </div>

        <div class="card">
            <h2>Total Revenue: ${{ total_revenue }}</h2>
            <h2>Total Served Orders: {{ total_orders }}</h2>
        </div>

        <h2>Sales by Item</h2>

        <table>
            <tr>
                <th>Item</th>
                <th>Quantity Sold</th>
                <th>Revenue</th>
            </tr>

            {% for item in item_sales %}
            <tr>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>${{ item[2] }}</td>
            </tr>
            {% endfor %}
        </table>

        <div class="nav">
            <a href="/">Admin</a>
            <a href="/kitchen">Kitchen</a>
        </div>
    </div>
    """

    return render_template_string(
        html,
        total_revenue=total_revenue,
        total_orders=total_orders,
        item_sales=item_sales,
        style=STYLE
    )

@app.route("/order_confirmed/<int:table_number>/<int:order_id>")
def order_confirmed(table_number, order_id):
    html = """
    {{ style|safe }}

    <div class="container">
        <div class="hero">
            <h1>✅ Order Sent</h1>
            <p class="subtitle">Your order has been sent to the kitchen.</p>
        </div>

        <div class="card">
            <h2>Table {{ table_number }}</h2>
            <h2>Order #{{ order_id }}</h2>
            <p>Estimated wait: <strong>10–15 minutes</strong></p>
        </div>

        <a href="/order/{{ order_id }}">
            Track My Order
        </a>

        <br><br>

        <a href="/table/{{ table_number }}">
            Order More Food
        </a>
    </div>
    """

    return render_template_string(
        html,
        table_number=table_number,
        order_id=order_id,
        style=STYLE
    )

@app.route("/order/<int:order_id>")
def track_order(order_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, table_number, status, created_at
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    conn.close()

    if not order:
        return "Order not found"

    status_icon = {
        "New": "🆕",
        "Preparing": "🍳",
        "Ready": "🔔",
        "Served": "✅"
    }.get(order[2], "❓")

    html = """
    {{ style|safe }}

    <div class="container">

        <div class="hero">
            <h1>{{ icon }} Order Status</h1>
        </div>

        <div class="card">
            <h2>Order #{{ order[0] }}</h2>

            <p><strong>Table:</strong> {{ order[1] }}</p>

            <p>
                <strong>Status:</strong>
                {{ order[2] }}
            </p>

            <p>
                <strong>Created:</strong>
                {{ order[3] }}
            </p>
        </div>

        <div class="nav">
            <a href="/table/{{ order[1] }}">
                Order More Food
            </a>
        </div>

    </div>

    <script>
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
    """

    return render_template_string(
        html,
        order=order,
        icon=status_icon,
        style=STYLE
    )

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)