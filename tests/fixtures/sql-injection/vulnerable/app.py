"""Vulnerable fixture: SQL Injection (CWE-89).

Expected: security-reviewer should flag `get_order` -- the `order_id` query
parameter is concatenated directly into the SQL string with no
parameterization, and reaches `cursor.execute` unmodified.
"""

from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/orders")
def get_order():
    order_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # VULNERABLE: order_id is attacker-controlled and concatenated directly
    # into the query string, with no parameter binding.
    query = "SELECT * FROM orders WHERE id = " + order_id
    cursor.execute(query)
    return {"rows": cursor.fetchall()}
