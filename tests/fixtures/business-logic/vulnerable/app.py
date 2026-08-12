"""Vulnerable fixture: Race Condition / TOCTOU on balance deduction (CWE-362).

Expected: business-logic-review should flag `redeem_coupon` -- it checks
the coupon's `used` flag and then, in a separate statement, marks it used
and applies the discount. Two concurrent requests can both pass the check
before either commits the update, letting the same single-use coupon be
redeemed multiple times.
"""

from flask import Flask, request

app = Flask(__name__)


def get_coupon(code):
    ...  # returns {"code": ..., "used": bool, "discount": ...}


def mark_coupon_used(code):
    ...  # UPDATE coupons SET used = true WHERE code = %s


def apply_discount_to_cart(cart_id, discount):
    ...


@app.route("/cart/<cart_id>/redeem", methods=["POST"])
def redeem_coupon(cart_id):
    code = request.json["coupon_code"]
    coupon = get_coupon(code)

    # VULNERABLE: check-then-act with no atomicity -- two concurrent
    # requests can both read used=False before either request writes back.
    if coupon["used"]:
        return {"error": "coupon already used"}, 400

    mark_coupon_used(code)
    apply_discount_to_cart(cart_id, coupon["discount"])
    return {"applied": True}
