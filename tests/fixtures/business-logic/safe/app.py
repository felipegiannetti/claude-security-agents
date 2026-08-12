"""Safe fixture: atomic check-and-act via a conditional UPDATE (paired with
vulnerable/app.py).

Expected: business-logic-review should NOT confirm a race-condition
finding here -- `mark_coupon_used_if_unused` performs the check and the
write as a single atomic database operation, so two concurrent requests
cannot both succeed: only one UPDATE can match `used = false` and flip it.
See skills/business-logic-review/references/race-conditions.md
"False-Positive Conditions".
"""

from flask import Flask, request

app = Flask(__name__)


def mark_coupon_used_if_unused(code):
    # SAFE: single atomic statement --
    # UPDATE coupons SET used = true WHERE code = %s AND used = false
    # RETURNING discount;
    # Returns the discount only if THIS call was the one that flipped the flag.
    ...


def apply_discount_to_cart(cart_id, discount):
    ...


@app.route("/cart/<cart_id>/redeem", methods=["POST"])
def redeem_coupon(cart_id):
    code = request.json["coupon_code"]

    # SAFE: check-and-act is one atomic operation -- only one concurrent
    # request can ever receive a non-None discount for the same coupon.
    discount = mark_coupon_used_if_unused(code)
    if discount is None:
        return {"error": "coupon already used"}, 400

    apply_discount_to_cart(cart_id, discount)
    return {"applied": True}
