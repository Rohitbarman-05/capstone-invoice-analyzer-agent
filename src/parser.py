import re
from typing import List, Dict, Any

def first_match(pattern: str, text: str):
    m = re.search(pattern, text, re.I | re.M)
    return m.group(1).strip() if m else None

def parse_line_items(text: str) -> List[Dict[str, Any]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    items = []
    # Heuristics: look for lines with qty and price, or price at end
    for ln in lines:
        # pattern: description ... qty ... unit_price  OR description ... unit_price
        m = re.search(r'^(.+?)\s+([0-9]+)\s+([0-9\.,]+\d)\s*$', ln)
        if m:
            desc = m.group(1).strip()
            try:
                qty = int(m.group(2))
            except:
                qty = 1
            price = float(m.group(3).replace(',', ''))
            items.append({"description": desc, "qty": qty, "unit_price": price})
            continue
        m2 = re.search(r'^(.+?)\s+([0-9\.,]+\d)\s*$', ln)
        if m2:
            desc = m2.group(1).strip()
            price = float(m2.group(2).replace(',', ''))
            items.append({"description": desc, "qty": 1, "unit_price": price})
    return items

def normalize_number(s: str):
    if s is None: 
        return None
    s = s.strip()
    s = s.replace('₹','').replace('Rs.','').replace('$','')
    s = s.replace(',','')
    try:
        return float(s)
    except:
        # extract first numeric substring
        m = re.search(r'([0-9\.,]+\d)', s)
        if m:
            return float(m.group(1).replace(',',''))
    return None

def parse_fields_from_text(text: str) -> Dict[str, Any]:
    # Try common field patterns
    vendor = first_match(r'^(?:From|Supplier|Vendor)[:\s]*(.+)$', text) or first_match(r'^(.{3,80})\n.*Invoice', text)
    invoice_no = first_match(r'Invoice\s*(?:No|#|Number)[:\s]*([A-Z0-9\-/]+)', text) or first_match(r'\b([A-Z]{1,5}-\d{1,8})\b', text)
    date = first_match(r'(?:Invoice Date|Date)[:\s]*([0-3]?\d[\/\-\.\s][01]?\d[\/\-\.\s]\d{2,4})', text)
    currency = first_match(r'\b(USD|INR|EUR|GBP|AUD|CAD|₹|\$|Rs\.)\b', text)
    total_raw = first_match(r'(?:Total\s*(?:Amount)?|Grand Total|Amount Due)[:\s]*([0-9\.,]+\d)', text) or first_match(r'([0-9\.,]+\d)\s*(?:Total|Grand Total|Amount Due)', text)
    subtotal_raw = first_match(r'(?:Subtotal)[:\s]*([0-9\.,]+\d)', text)
    tax_raw = first_match(r'(?:Tax|GST|VAT)[:\s]*([0-9\.,]+\d)', text)

    line_items = parse_line_items(text)

    return {
        "vendor": vendor,
        "invoice_no": invoice_no,
        "date": date,
        "currency": currency,
        "line_items": line_items,
        "subtotal": normalize_number(subtotal_raw),
        "tax": normalize_number(tax_raw),
        "total": normalize_number(total_raw),
        # keep original raw strings for debugging
        "raw_totals": {"subtotal_raw": subtotal_raw, "tax_raw": tax_raw, "total_raw": total_raw}
    }
