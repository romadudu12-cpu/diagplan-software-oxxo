
from datetime import date
from flask import Flask, flash, redirect, render_template, request, url_for
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "diagplan.db"

app = Flask(__name__)
app.secret_key = "diagplan-chave-local"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT '',
            sku TEXT UNIQUE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
            expiry_date TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            lot_id INTEGER,
            movement_type TEXT NOT NULL CHECK(movement_type IN ('entrada', 'saida')),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(lot_id) REFERENCES lots(id)
        );
        """)

@app.context_processor
def inject_today():
    return {"today": date.today().isoformat()}

@app.route("/")
def index():
    hoje = date.today().isoformat()

    with get_db() as db:
        products_count = db.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        total_units = db.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM lots
            WHERE expiry_date IS NULL OR expiry_date >= ?
        """, (hoje,)).fetchone()[0]

        expiring = db.execute("""
            SELECT l.id, p.name, l.quantity, l.expiry_date
            FROM lots l
            JOIN products p ON p.id = l.product_id
            WHERE l.expiry_date IS NOT NULL
              AND l.quantity > 0
              AND l.expiry_date <= date('now', '+30 day')
            ORDER BY l.expiry_date
            LIMIT 8
        """).fetchall()

        recent = db.execute("""
            SELECT m.*, p.name AS product_name
            FROM movements m
            JOIN products p ON p.id = m.product_id
            ORDER BY m.id DESC
            LIMIT 8
        """).fetchall()

        expired_units = db.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM lots
            WHERE expiry_date IS NOT NULL
              AND expiry_date < ?
        """, (hoje,)).fetchone()[0]

    return render_template(
        "index.html",
        products_count=products_count,
        total_units=total_units,
        expiring=expiring,
        recent=recent,
        expired_units=expired_units
    )

@app.route("/produtos")
def products():
    hoje = date.today().isoformat()

    with get_db() as db:
        rows = db.execute("""
            SELECT
                p.*,
                COALESCE(SUM(l.quantity), 0) AS stock,
                COALESCE(SUM(
                    CASE
                        WHEN l.expiry_date IS NULL OR l.expiry_date >= ?
                        THEN l.quantity ELSE 0
                    END
                ), 0) AS available_stock,
                COALESCE(SUM(
                    CASE
                        WHEN l.expiry_date IS NOT NULL AND l.expiry_date < ?
                        THEN l.quantity ELSE 0
                    END
                ), 0) AS expired_stock,
                MIN(
                    CASE
                        WHEN l.quantity > 0
                         AND (l.expiry_date IS NULL OR l.expiry_date >= ?)
                        THEN l.expiry_date
                    END
                ) AS next_expiry
            FROM products p
            LEFT JOIN lots l ON l.product_id = p.id
            GROUP BY p.id
            ORDER BY p.name
        """, (hoje, hoje, hoje)).fetchall()

    return render_template("products.html", products=rows)

@app.route("/produtos/novo", methods=["GET", "POST"])
def new_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        sku = request.form.get("sku", "").strip() or None

        if not name:
            flash("Informe o nome do produto.", "danger")
            return render_template("product_form.html")

        try:
            with get_db() as db:
                db.execute("""
                    INSERT INTO products(name, category, sku)
                    VALUES (?, ?, ?)
                """, (name, category, sku))

            flash("Produto cadastrado com sucesso.", "success")
            return redirect(url_for("products"))

        except sqlite3.IntegrityError:
            flash("Este código SKU já está cadastrado.", "danger")

    return render_template("product_form.html")

@app.route("/movimentacoes", methods=["GET", "POST"])
def movements():
    with get_db() as db:

        if request.method == "POST":
            product_id = request.form.get("product_id", type=int)
            movement_type = request.form.get("movement_type")
            quantity = request.form.get("quantity", type=int)
            expiry_date = request.form.get("expiry_date") or None
            notes = request.form.get("notes", "").strip()

            product = db.execute(
                "SELECT id FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()

            if (
                not product
                or movement_type not in ("entrada", "saida")
                or not quantity
                or quantity < 1
            ):
                flash("Confira o produto, o tipo e a quantidade.", "danger")
                return redirect(url_for("movements"))

            if movement_type == "entrada":

                if expiry_date and expiry_date < date.today().isoformat():
                    flash("Não é permitido cadastrar entrada de lote vencido.", "danger")
                    return redirect(url_for("movements"))

                cur = db.execute("""
                    INSERT INTO lots(product_id, quantity, expiry_date)
                    VALUES (?, ?, ?)
                """, (product_id, quantity, expiry_date))

                lot_id = cur.lastrowid

            else:
                hoje = date.today().isoformat()

                lots = db.execute("""
                    SELECT id, quantity, expiry_date
                    FROM lots
                    WHERE product_id = ?
                      AND quantity > 0
                      AND (expiry_date IS NULL OR expiry_date >= ?)
                    ORDER BY
                      CASE WHEN expiry_date IS NULL THEN 1 ELSE 0 END,
                      expiry_date, id
                """, (product_id, hoje)).fetchall()

                available = sum(lot["quantity"] for lot in lots)

                if quantity > available:
                    flash(
                        f"Estoque disponível insuficiente. "
                        f"Disponível: {available} unidade(s).",
                        "danger"
                    )
                    return redirect(url_for("movements"))

                remaining = quantity
                lot_id = None

                for lot in lots:
                    if remaining <= 0:
                        break

                    take = min(lot["quantity"], remaining)

                    db.execute("""
                        UPDATE lots
                        SET quantity = quantity - ?
                        WHERE id = ?
                    """, (take, lot["id"]))

                    remaining -= take
                    lot_id = lot["id"]

            db.execute("""
                INSERT INTO movements(
                    product_id, lot_id, movement_type, quantity, notes
                )
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, lot_id, movement_type, quantity, notes))

            flash("Movimentação registrada com sucesso.", "success")
            return redirect(url_for("movements"))

        product_rows = db.execute("""
            SELECT id, name
            FROM products
            ORDER BY name
        """).fetchall()

        history = db.execute("""
            SELECT m.*, p.name AS product_name
            FROM movements m
            JOIN products p ON p.id = m.product_id
            ORDER BY m.id DESC
            LIMIT 50
        """).fetchall()

    return render_template(
        "movements.html",
        products=product_rows,
        movements=history
    )

@app.route("/lotes")
def lots():
    hoje = date.today().isoformat()

    with get_db() as db:
        rows = db.execute("""
            SELECT
                l.*,
                p.name AS product_name,
                CASE
                    WHEN l.expiry_date IS NULL THEN 'Sem validade'
                    WHEN l.expiry_date < ? THEN 'Vencido'
                    WHEN l.expiry_date <= date('now', '+30 day') THEN 'A vencer'
                    ELSE 'Dentro da validade'
                END AS status
            FROM lots l
            JOIN products p ON p.id = l.product_id
            ORDER BY
                CASE WHEN l.expiry_date IS NULL THEN 1 ELSE 0 END,
                l.expiry_date
        """, (hoje,)).fetchall()

    return render_template("lots.html", lots=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
