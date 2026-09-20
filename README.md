# Auctions

An eBay-style auction site — list items, bid on them, comment, and watch listings.

## Stack

Django · Python · SQLite

## Features

- Create listings with a starting bid, description, image and category
- Bid on active listings, with validation against the current highest bid
- Close a listing and declare the winner
- Comments per listing
- Per-user watchlist
- Browse by category

## Running it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Notes

Built as a CS50 Web Programming project.
