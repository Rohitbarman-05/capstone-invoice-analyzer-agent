# Smart Invoice Analyzer Agent
**Track:** Enterprise Agents  
**Author:** Rohit Barman 
**Short:** Extracts and validates invoice fields from PDFs/images, summarizes issues, and exports structured data.

## Features
- PDF / image ingestion with hashing & duplicate detection
- OCR fallback & deterministic parsing (regex)
- LLM-powered fallback parser for ambiguous formats
- Validation (total vs line items), tax checks
- Structured export (JSON/CSV) and webhook demo
- Session memory (SQLite) and simple observability (logs & metrics)

## How to run (Kaggle Notebook)
1. Open `notebooks/demo.ipynb`.
2. Upload sample invoices or use `data/sample_invoices/`.
3. Run cells in order: Ingest → Extract → Validate → Summarize → Export.

## Tech stack
- Python 3.10+
- PyPDF2 / pdfplumber
- pytesseract + Pillow (for OCR fallback)
- sqlite3 for memory
- OpenAI / Gemini (LLM) or local LLM via API (use env var)
- Flask (optional) for webhook demo

## Security
**Do NOT** include API keys in this repo. Use environment variables.

## Evaluation
- Field extraction accuracy on a labelled dataset (precision/recall)
- Processing time per invoice
- Duplicate detection rate

## License
MIT
