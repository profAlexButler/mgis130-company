"""Check the company data against the contract. Runs on every change to data/ (see .github/workflows).
Exit code 1 if anything is wrong, so the check shows a red X on the commit or pull request."""
import json
import os
import re
import sys

SPEC = {
    "customers": {
        "id": [
            "text",
            "unique id, C plus three digits",
            None
        ],
        "name": [
            "text",
            "the customer's name",
            None
        ],
        "type": [
            "text",
            "Office lunch, Catering, Event, Venue, Campus or Regular",
            None
        ],
        "contact": [
            "text",
            "the person we talk to",
            None
        ],
        "email": [
            "text",
            "their email (all made up, @example.com)",
            None
        ],
        "lastContact": [
            "date",
            "the last time Sales talked to them",
            None
        ],
        "since": [
            "date",
            "when they became a customer",
            None
        ]
    },
    "orders": {
        "id": [
            "text",
            "unique id, O plus four digits",
            None
        ],
        "customerId": [
            "text",
            "who placed the order",
            "customers"
        ],
        "date": [
            "date",
            "the day of the order",
            None
        ],
        "description": [
            "text",
            "what we served",
            None
        ],
        "total": [
            "number",
            "invoice total in dollars",
            None
        ],
        "dueDate": [
            "date",
            "payment due, 14 days after the order",
            None
        ],
        "paid": [
            "yes/no",
            "true once the customer has paid",
            None
        ]
    },
    "requests": {
        "id": [
            "text",
            "unique id, R plus two digits",
            None
        ],
        "customerId": [
            "text",
            "who asked",
            "customers"
        ],
        "type": [
            "text",
            "Refund, Discount, Special order or Schedule change",
            None
        ],
        "submitted": [
            "date",
            "the day it came in",
            None
        ],
        "amount": [
            "number",
            "dollars involved (0 if none)",
            None
        ],
        "status": [
            "text",
            "Pending, Approved or Denied",
            None
        ],
        "approver": [
            "text",
            "Shift lead or Owner, by the approval rule",
            None
        ],
        "note": [
            "text",
            "what they asked for",
            None
        ]
    },
    "menu": {
        "id": [
            "text",
            "unique id, M plus two digits",
            None
        ],
        "name": [
            "text",
            "what the customer sees on the menu board",
            None
        ],
        "category": [
            "text",
            "Taco, Bowl, Side, Dessert or Drink",
            None
        ],
        "price": [
            "number",
            "price in dollars",
            None
        ],
        "available": [
            "yes/no",
            "true if it is on the menu right now",
            None
        ]
    },
    "sales": {
        "id": [
            "text",
            "unique id, W plus two digits",
            None
        ],
        "menuItemId": [
            "text",
            "which menu item",
            "menu"
        ],
        "weekOf": [
            "date",
            "the Monday the week starts",
            None
        ],
        "unitsThisWeek": [
            "number",
            "units sold this week",
            None
        ],
        "unitsLastWeek": [
            "number",
            "units sold the week before",
            None
        ]
    },
    "inventory": {
        "id": [
            "text",
            "unique id, I plus two digits",
            None
        ],
        "item": [
            "text",
            "what it is",
            None
        ],
        "category": [
            "text",
            "Food, Drink or Packaging",
            None
        ],
        "unit": [
            "text",
            "how we count it",
            None
        ],
        "onHand": [
            "number",
            "how many units we have now",
            None
        ],
        "reorderPoint": [
            "number",
            "reorder when on hand falls below this",
            None
        ],
        "supplierId": [
            "text",
            "who we buy it from",
            "suppliers"
        ],
        "lastOrdered": [
            "date",
            "the last time we ordered it",
            None
        ]
    },
    "suppliers": {
        "id": [
            "text",
            "unique id, S plus two digits",
            None
        ],
        "name": [
            "text",
            "the supplier's name",
            None
        ],
        "supplies": [
            "text",
            "what we buy from them",
            None
        ],
        "contact": [
            "text",
            "the person we order from",
            None
        ],
        "leadTimeDays": [
            "number",
            "days from ordering to delivery",
            None
        ]
    }
}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
problems = []
ids = {}
rows = {}

for name, spec in SPEC.items():
    path = os.path.join(ROOT, name + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        problems.append(name + ".json: file is missing")
        continue
    except json.JSONDecodeError as e:
        problems.append(name + ".json: not valid JSON at line %d, column %d (%s)" % (e.lineno, e.colno, e.msg))
        continue
    if not isinstance(data, list):
        problems.append(name + ".json: should be a JSON array [ ... ]")
        continue
    rows[name] = data
    seen = set()
    for n, row in enumerate(data, 1):
        where = "%s.json row %d" % (name, n)
        if not isinstance(row, dict):
            problems.append(where + ": should be an object { ... }")
            continue
        rid = row.get("id", "?")
        where += " (id " + str(rid) + ")"
        for fld, (typ, _m, _l) in spec.items():
            if fld not in row:
                problems.append(where + ": missing field '" + fld + "'")
                continue
            v = row[fld]
            if typ == "number" and (isinstance(v, bool) or not isinstance(v, (int, float))):
                problems.append(where + ": '" + fld + "' should be a number")
            elif typ == "yes/no" and not isinstance(v, bool):
                problems.append(where + ": '" + fld + "' should be true or false")
            elif typ == "date" and not (isinstance(v, str) and DATE.match(v)):
                problems.append(where + ": '" + fld + "' should be a date like 2026-10-07")
            elif typ == "text" and not isinstance(v, str):
                problems.append(where + ": '" + fld + "' should be text in quotes")
        for fld in row:
            if fld not in spec:
                problems.append(where + ": field '" + fld + "' is not in the contract")
        if rid in seen:
            problems.append(where + ": id is used twice")
        seen.add(rid)
    ids[name] = seen

for name, spec in SPEC.items():
    for fld, (_t, _m, link) in spec.items():
        if not link or name not in rows or link not in ids:
            continue
        for row in rows[name]:
            if isinstance(row, dict) and fld in row and row[fld] not in ids[link]:
                problems.append("%s.json (id %s): %s '%s' does not match any id in %s.json" % (name, row.get("id", "?"), fld, row[fld], link))

if problems:
    print("The company data does not match the contract:")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("All %d files match the contract (%d rows)." % (len(rows), sum(len(r) for r in rows.values())))
