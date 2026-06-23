# 🍜 Restaurant QR Ordering System

A QR-code-based restaurant ordering system built with Python, Flask, SQLite, HTML, and CSS.

Customers scan a QR code at their table, browse the menu, place orders, and track order status. Kitchen staff can manage incoming orders through a kitchen dashboard, while managers can monitor restaurant sales through a sales dashboard.

---

## Features

### Customer Features

* QR code ordering system
* Table-specific ordering pages
* Food menu with images
* Multi-item ordering
* Order confirmation page
* Real-time order status tracking
* Mobile-friendly web interface

### Kitchen Features

* Live kitchen dashboard
* Incoming order management
* Order status workflow:

  * New
  * Preparing
  * Ready
  * Served
* Automatic dashboard refresh
* New order notification sound

### Management Features

* Sales dashboard
* Total revenue tracking
* Served order statistics
* Best-selling item analytics

---

## Tech Stack

### Backend

* Python
* Flask

### Database

* SQLite

### Frontend

* HTML
* CSS

### Other

* QR Code Generation
* Local Image Hosting
* REST-style Flask Routes

---

## Database Design

### Orders Table

```text
orders
├── id
├── table_number
├── status
└── created_at
```

### Order Items Table

```text
order_items
├── id
├── order_id
├── item
├── quantity
├── unit_price
└── total_price
```

Relationship:

```text
One Order
    ↓
Many Order Items
```

This allows a customer to place a single order containing multiple menu items.

---

## Project Structure

```text
Restaurant-QR-Ordering-System/

├── server.py
├── restaurant.db
├── README.md
│
├── static/
│   ├── photos/
│   │   ├── pho_bo.jpg
│   │   ├── banh_mi.jpeg
│   │   ├── bun_thit_nuong.jpeg
│   │   ├── goi_cuon.jpg
│   │   ├── ca_phe_sua_da.jpeg
│   │   └── tra_da.jpeg
│   │
│   └── table_qrcodes/
│
└── venv/
```

---

## How It Works

### Customer Flow

```text
Scan QR Code
        ↓
Open Table Page
        ↓
Select Menu Items
        ↓
Submit Order
        ↓
Order Confirmation
        ↓
Track Order Status
```

### Kitchen Flow

```text
New Order
     ↓
Preparing
     ↓
Ready
     ↓
Served
```

### Management Flow

```text
Orders Completed
        ↓
Sales Dashboard
        ↓
Revenue & Analytics
```

---

## Running Locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install flask
```

Run the server:

```bash
python3 server.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Current Status

This project is currently a functional prototype intended for learning web development, restaurant automation, and backend system design.

The system successfully demonstrates:

* QR ordering
* Database persistence
* Order tracking
* Kitchen workflow management
* Sales analytics

---

## Future Improvements

* Mobile-first redesign
* Menu categories
* Shopping cart
* Inventory management
* Staff call button
* Request bill feature
* WebSocket real-time updates
* Online deployment
* Payment integration
* Admin authentication
* Advanced analytics

---

## Author

Developed by DelnRDev as a restaurant automation and web development project.
