"""Download a real CodeSearchNet-derived Python dataset.

Default: 10,000 records streamed from the public Hugging Face mirror
Nan-Do/code-search-net-python. The records originate from CodeSearchNet's
open-source GitHub functions. No synthetic rows are generated.
"""
from pathlib import Path
import pandas as pd
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'components.csv'
RAW = ROOT / 'datasets' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
OUT.parent.mkdir(parents=True, exist_ok=True)

LIMIT = 10000
print('Loading real CodeSearchNet Python records from Hugging Face...')
print('Dataset: Nan-Do/code-search-net-python')
print('Requested records:', LIMIT)

ds = load_dataset('Nan-Do/code-search-net-python', split='train', streaming=True)

rows = []
for row in ds:
    code = row.get('code', '') or ''
    if not code.strip():
        continue
    rows.append({
        'component_id': f'CSN-{len(rows)+1:06d}',
        'repo': row.get('repo', ''),
        'path': row.get('path', ''),
        'func_name': row.get('func_name', ''),
        'code': code,
        'language': row.get('language', 'python'),
        'docstring': row.get('docstring', ''),
        'sha': row.get('sha', ''),
        'url': row.get('url', ''),
        'partition': row.get('partition', ''),
        'summary': row.get('summary', ''),
        'dataset_source': 'CodeSearchNet',
    })
    if len(rows) >= LIMIT:
        break

if not rows:
    raise RuntimeError('No records were downloaded. Check internet access and the dataset name.')

pd.DataFrame(rows).to_csv(OUT, index=False, encoding='utf-8')
print(f'Saved {len(rows):,} real records to {OUT}')
