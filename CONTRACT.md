# Company contract: Our Food Truck

This repo is our company's one database. Every department reads its data from here, and nobody keeps a private copy. Everything in it is made up.

## Where the data lives

Base URL: `https://profalexbutler.github.io/mgis130-company/data/`

Each file is at the base URL plus its name, for example `https://profalexbutler.github.io/mgis130-company/data/customers.json`. Read files with `fetch(url, { cache: "no-store" })` so you always get the latest version.

Every file is a JSON array. Each object in it is one row. Dates are text in the form YYYY-MM-DD, numbers have no $ signs, and yes/no fields are `true` or `false`.

## How the files connect

Some fields hold another file's id. To show a name, look up the matching row in the other file.

| This field | Points at |
|---|---|
| `orders.json` customerId | the `id` of a row in `customers.json` |
| `requests.json` customerId | the `id` of a row in `customers.json` |
| `sales.json` menuItemId | the `id` of a row in `menu.json` |
| `inventory.json` supplierId | the `id` of a row in `suppliers.json` |

## The data files

### customers.json

Each row is a customer: a business, group or regular we sell to. Kept up to date by Sales.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | C001 | unique id, C plus three digits |
| name | text | Riverside Brewing Co. | the customer's name |
| type | text | Venue | Office lunch, Catering, Event, Venue, Campus or Regular |
| contact | text | Marcus Hale | the person we talk to |
| email | text | marcus.hale@example.com | their email (all made up, @example.com) |
| lastContact | date | 2026-10-02 | the last time Sales talked to them |
| since | date | 2025-05-10 | when they became a customer |

### orders.json

Each row is a catering, office or event order we invoiced. Kept up to date by Finance.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | O1001 | unique id, O plus four digits |
| customerId | text | C011 | who placed the order |
| date | date | 2026-08-01 | the day of the order |
| description | text | Back-to-school night, 120 people | what we served |
| total | number | 1320.0 | invoice total in dollars |
| dueDate | date | 2026-08-15 | payment due, 14 days after the order |
| paid | yes/no | true | true once the customer has paid |

### requests.json

Each row is a refund, discount, special order or schedule change someone asked for. Kept up to date by Operations.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | R01 | unique id, R plus two digits |
| customerId | text | C008 | who asked |
| type | text | Refund | Refund, Discount, Special order or Schedule change |
| submitted | date | 2026-09-24 | the day it came in |
| amount | number | 9.25 | dollars involved (0 if none) |
| status | text | Approved | Pending, Approved or Denied |
| approver | text | Shift lead | Shift lead or Owner, by the approval rule |
| note | text | Got carnitas instead of tinga | what they asked for |

### menu.json

Each row is an item on the truck's menu. Kept up to date by Analytics.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | M01 | unique id, M plus two digits |
| name | text | Chicken tinga taco | what the customer sees on the menu board |
| category | text | Taco | Taco, Bowl, Side, Dessert or Drink |
| price | number | 4.5 | price in dollars |
| available | yes/no | true | true if it is on the menu right now |

### sales.json

Each row is one menu item's sales for the week. Kept up to date by Analytics.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | W01 | unique id, W plus two digits |
| menuItemId | text | M01 | which menu item |
| weekOf | date | 2026-09-28 | the Monday the week starts |
| unitsThisWeek | number | 212 | units sold this week |
| unitsLastWeek | number | 198 | units sold the week before |

### inventory.json

Each row is something we keep on the truck or in storage. Kept up to date by Warehouse.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | I01 | unique id, I plus two digits |
| item | text | Corn tortillas | what it is |
| category | text | Food | Food, Drink or Packaging |
| unit | text | pack of 50 | how we count it |
| onHand | number | 12 | how many units we have now |
| reorderPoint | number | 10 | reorder when on hand falls below this |
| supplierId | text | S03 | who we buy it from |
| lastOrdered | date | 2026-10-01 | the last time we ordered it |

### suppliers.json

Each row is a company we buy from. Kept up to date by Warehouse.

| Field | Type | Example | Meaning |
|---|---|---|---|
| id | text | S01 | unique id, S plus two digits |
| name | text | Valley Produce Co. | the supplier's name |
| supplies | text | Produce and dry goods | what we buy from them |
| contact | text | Ana Ruiz | the person we order from |
| leadTimeDays | number | 2 | days from ordering to delivery |

## Business rules

- **Approvals (Operations):** refunds and discounts of $25 or less are approved by a shift lead. Anything over $25, and every special order or schedule change, goes to the owner.
- **Payment (Finance):** an order is due 14 days after its date.
- **Reordering (Warehouse):** reorder an item when on hand falls below its reorder point. The supplier's lead time says how many days it takes to arrive.

## Page hooks (the same for every department)

| Hook | What it is |
|---|---|
| `#title` | the heading: the company name and your department |
| `#summary` | a row of 2 or 3 numbers |
| `#list` | where the cards go, one card per row of data |
| `.card` | one row of data |
| `.tag` | a short label on a card |
| `.alert` | added to a card that needs attention |

## Department views

### Sales (CRM)

- **Reads:** `customers.json`
- **Each card shows:** name, type, contact, last contact
- **Tag:** type
- **Summary:** number of customers; number due for a call
- **Alert when:** lastContact is more than 30 days before today

### Warehouse (SCM)

- **Reads:** `inventory.json`, `suppliers.json`
- **Each card shows:** item, on hand, reorder point, unit, and the supplier's name and lead time (look up supplierId in suppliers.json)
- **Tag:** category
- **Summary:** items we track; items below their reorder point
- **Alert when:** onHand is less than reorderPoint

### Finance (Accounting)

- **Reads:** `orders.json`, `customers.json`
- **Each card shows:** the customer's name (look up customerId in customers.json), description, date, total, due date
- **Tag:** Paid or Unpaid
- **Summary:** total billed; total still unpaid
- **Alert when:** paid is false and dueDate is before today

### Analytics (BI)

- **Reads:** `sales.json`, `menu.json`
- **Each card shows:** the item's name and price (look up menuItemId in menu.json), units this week, units last week
- **Tag:** the item's category from menu.json
- **Summary:** units sold this week; this week's best seller
- **Alert when:** unitsThisWeek is less than unitsLastWeek

### Operations (Workflow)

- **Reads:** `requests.json`, `customers.json`
- **Each card shows:** the customer's name (look up customerId in customers.json), type, amount, submitted, approver, note
- **Tag:** status
- **Summary:** pending requests; requests approved
- **Alert when:** status is Pending and it was submitted more than 3 days before today

## Changing this contract

Every department's code uses these file names and field names. Renaming or removing a field breaks every page that reads it. So changes go through a pull request: propose the change, the owner of this repo reviews it, and it is merged only once the contract is updated to match. Adding a new row is a small change; renaming a field is a big one.
