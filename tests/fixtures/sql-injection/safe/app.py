"""Safe fixture: parameterized query (paired with vulnerable/app.py).

Expected: security-reviewer / security-verifier should NOT confirm a SQL
injection finding here -- `order_id` is passed as a bound parameter, never
concatenated into the query string, so it cannot alter the query's structure
regardless of its content. See
skills/injection-review/references/sql-injection.md "False-Positive
Conditions" -- prepared statements/parameterized queries.
"""

from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/orders")
def get_order():
    order_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # SAFE: order_id is bound as a parameter, not concatenated into the SQL string.
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    return {"rows": cursor.fetchall()}
