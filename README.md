# Our Food Truck: company data

The shared data for our MGIS 130 class company, a food truck. Every department's app reads from here. This repo plays the part of the company's ERP database: one place for the data, so every department sees the same customers, orders and numbers.

- **Read the contract first:** [CONTRACT.md](CONTRACT.md) lists every file, every field, how the files connect, and what each department's page shows.
- **The data:** the `data/` folder. Read it from `https://profalexbutler.github.io/mgis130-company/data/`.
- **Want to add or change something?** Open the file on github.com, click the pencil, make your change, and choose Propose changes. GitHub will make a copy (a fork) for you and open a pull request. The owner reviews it before it is merged.
- **The check:** every change to `data/` runs `scripts/check_data.py` (see the Actions tab). It checks that each file is valid JSON, that every row has the contract's fields, that ids are unique, and that every customerId, supplierId and menuItemId points at a row that exists.

Everything in this repo is made up. Never put real customer data in a public repo.

Repo: https://github.com/profalexbutler/mgis130-company
