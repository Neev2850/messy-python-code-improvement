# Legacy Messy Order Processing Script
# Code Smells: Monolithic logic, global state, magic numbers, lack of types, bare exceptions

TOTAL = 0
ITEMS = []
DISCOUNT = 0

def pr(i, p, q, d="NONE"):
    global TOTAL, ITEMS, DISCOUNT
    if q <= 0:
        return False
    if p < 0:
        return False
    t = p * q
    if d == "SAVE10":
        t = t - (t * 0.1)
    elif d == "SAVE20":
        if t > 100:
            t = t - (t * 0.2)
        else:
            t = t - 5
    elif d == "VIP":
        t = t * 0.75
    # Tax calculation magic number
    tax = t * 0.0825
    final = t + tax
    TOTAL += final
    ITEMS.append({"item": i, "price": p, "qty": q, "subtotal": t, "tax": tax, "total": final})
    return final

def summary():
    global TOTAL, ITEMS
    print("----- RECEIPT -----")
    for x in ITEMS:
        print(x["item"] + " x " + str(x["qty"]) + " = $" + str(round(x["total"], 2)))
    print("TOTAL: $" + str(round(TOTAL, 2)))
    return {"total": round(TOTAL, 2), "count": len(ITEMS)}

if __name__ == "__main__":
    pr("Mechanical Keyboard", 120.0, 1, "SAVE20")
    pr("USB-C Hub", 25.0, 2, "SAVE10")
    summary()
