from pathlib import Path
import hashlib
import shutil

def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def ingest_file(src_path: str, dest_folder: str = "data/sample_invoices"):
    src = Path(src_path)
    dest_folder = Path(dest_folder)
    dest_folder.mkdir(parents=True, exist_ok=True)
    dst = dest_folder / src.name
    shutil.copy2(src, dst)
    return {"path": str(dst), "hash": file_hash(str(dst))}
