import pandas as pd
from typing import List, Dict
from pathlib import Path

def export_csv(rows: List[Dict], path: Path):
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8")

def export_xlsx(rows: List[Dict], path: Path):
    pd.DataFrame(rows).to_excel(path, index=False)

def export_pdf(summary: Dict, path: Path):
    # Simple placeholder: write a small HTML and render via WeasyPrint
    from weasyprint import HTML
    html = f"""
    <h1>Twitter/X Report</h1>
    <p><b>Posts:</b> {summary['metrics']['posts']}</p>
    <p><b>Likes:</b> {summary['metrics']['likes']}</p>
    <p><b>Retweets:</b> {summary['metrics']['retweets']}</p>
    <p><b>Replies:</b> {summary['metrics']['replies']}</p>
    <p><b>Quotes:</b> {summary['metrics']['quotes']}</p>
    """
    HTML(string=html).write_pdf(path.as_posix())
