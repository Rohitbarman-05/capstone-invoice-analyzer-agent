from src.extractor import extract_text
from src.parser import parse_fields_from_text
from src.validator import validate_totals
from src.db import init_db, save_invoice, invoice_exists
from src.ingest import file_hash

def process_invoice(path: str) -> dict:
    # Initialize DB
    init_db()

    # Generate hash for duplicate detection
    h = file_hash(path)

    duplicate = invoice_exists(h)

    text = extract_text(path)
    parsed = parse_fields_from_text(text)
    validation = validate_totals(parsed)

    # Save only if new
    if not duplicate:
        save_invoice(h, parsed.get("invoice_no"), parsed.get("vendor"), parsed.get("total"))

    return {
        "path": path,
        "parsed": parsed,
        "validation": validation,
        "duplicate": duplicate,
        "hash": h,
        "raw_text_snippet": text[:1000]
    }

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: python src/orchestrator.py <invoice-file-path>")
    else:
        out = process_invoice(sys.argv[1])
        print(json.dumps(out, indent=2))
