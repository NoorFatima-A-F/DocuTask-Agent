from pathlib import Path
def write_file(p, c):
    pt = Path(p)
    pt.parent.mkdir(parents=True, exist_ok=True)
    pt.write_text(c.strip() + chr(10), encoding='utf-8')
    print('  [WROTE]', p)
