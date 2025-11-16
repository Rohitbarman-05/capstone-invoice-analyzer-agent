import sqlite3
from pathlib import Path

DB_PATH = Path("data/invoices.db")

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            hash TEXT PRIMARY KEY,
            invoice_no TEXT,
            vendor TEXT,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_invoice(hash_str, invoice_no, vendor, total):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO invoices(hash, invoice_no, vendor, total) VALUES (?,?,?,?)",
        (hash_str, invoice_no, vendor, total)
    )
    conn.commit()
    conn.close()

def invoice_exists(hash_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM invoices WHERE hash=?", (hash_str,))
    exists = bool(c.fetchone())
    conn.close()
    return exists
