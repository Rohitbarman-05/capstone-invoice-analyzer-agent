def validate_totals(parsed: dict) -> dict:
    res = {"has_total": False, "total_value": None, "ok": None, "notes": []}
    total = parsed.get("total")
    if total:
        try:
            val = float(total.replace(",", ""))
            res["has_total"] = True
            res["total_value"] = val
            res["ok"] = True
        except Exception:
            res["notes"].append("Could not parse total as number")
            res["ok"] = False
    else:
        res["notes"].append("Total missing")
        res["ok"] = False
    return res
