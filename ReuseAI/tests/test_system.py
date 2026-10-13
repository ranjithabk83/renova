from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_no_fake_sample_dataset():
    p = ROOT / 'data' / 'components.csv'
    if not p.exists() or p.stat().st_size == 0:
        return
    df = pd.read_csv(p)
    assert 'dataset_source' in df.columns
    assert set(df['dataset_source'].dropna().unique()) <= {'CodeSearchNet'}
