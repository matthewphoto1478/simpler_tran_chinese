"""Print the per-file verdict table from the CJK report."""
import json, sys
path = sys.argv[1]
s = json.load(open(path, encoding='utf-8'))
print('=== verdict rows (CJK-bearing files) ===')
for r in s['files']:
    if r['cjk'] > 0:
        print(f"  {r['verdict']:>30}  cjk={r['cjk']:>5}  s2t_chg={r['s2t_changed']:>5}  t2s_chg={r['t2s_changed']:>5}  s2t_pct={r['s2t_pct']:>5}%  t2s_pct={r['t2s_pct']:>5}%   {r['file']}")
print()
print('=== no-CJK files ===')
for r in s['files']:
    if r['cjk'] == 0:
        print('  ', r['file'])