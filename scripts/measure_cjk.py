"""
Measure whether the prose in the repo is Simplified or Traditional Chinese.

Method: take every Chinese character in each file. Run OpenCC s2t and t2s.
For each conversion, count how many original characters were *changed* by the
converter.

Interpretation:
  - `s2t` rewrites many chars -> it found Simplified forms and promoted them.
    The source was Simplified.
  - `t2s` rewrites many chars -> it found Traditional forms and simplified them.
    The source was Traditional.
  - The "winner" is whichever converter did *more* work.

Why not byte-length diff: OpenCC preserves some characters in either
direction (punctuation, ASCII, characters that happen to be identical), and
length-based diff is noisy. Counting *replaced* CJK code points is exact.

A file is "Traditional" if t2s changes more than s2t (the converter
found Traditional forms to simplify). It is "Simplified" if s2t changes
more (the converter found Simplified forms to traditionalise). When the
two are close, the file is mixed or ambiguous.
"""
import os, sys, json, subprocess
from pathlib import Path
import opencc

CJK_RANGES = [
    (0x3400, 0x4DBF),   # CJK Extension A
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x20000, 0x2A6DF), # CJK Extension B
]

def is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)

def cjk_chars(text: str):
    return [ch for ch in text if is_cjk(ch)]

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    s2t = opencc.OpenCC('s2t')
    t2s = opencc.OpenCC('t2s')

    files = []
    for p in sorted(root.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel.startswith('.git/') or rel.startswith('.cursor/'):
            continue
        if not p.suffix.lower() in {'.md', '.markdown', '.txt', '.json', '.yml', '.yaml'}:
            continue
        files.append(p)

    rows = []
    for p in files:
        rel = p.relative_to(root).as_posix()
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        chars = cjk_chars(text)
        if not chars:
            rows.append({'file': rel, 'cjk': 0, 's2t_changed': 0, 't2s_changed': 0, 'verdict': 'no CJK'})
            continue
        s2t_out = s2t.convert(text)
        t2s_out = t2s.convert(text)
        # Re-extract CJK from each output for fair diff
        s2t_chars = cjk_chars(s2t_out)
        t2s_chars = cjk_chars(t2s_out)
        s2t_changed = sum(1 for a, b in zip(chars, s2t_chars) if a != b)
        t2s_changed = sum(1 for a, b in zip(chars, t2s_chars) if a != b)
        n = len(chars)
        if s2t_changed == t2s_changed:
            verdict = 'mixed or ambiguous'
        elif s2t_changed > t2s_changed:
            # s2t did more rewriting -> it found Simplified forms to promote.
            verdict = 'Simplified'
        else:
            # t2s did more rewriting -> it found Traditional forms to simplify.
            verdict = 'Traditional'
        rows.append({
            'file': rel,
            'cjk': n,
            's2t_changed': s2t_changed,
            't2s_changed': t2s_changed,
            's2t_pct': round(100 * s2t_changed / n, 2),
            't2s_pct': round(100 * t2s_changed / n, 2),
            'verdict': verdict,
        })

    total_cjk = sum(r['cjk'] for r in rows)
    total_s2t = sum(r['s2t_changed'] for r in rows)
    total_t2s = sum(r['t2s_changed'] for r in rows)
    verdicts = {}
    for r in rows:
        verdicts[r['verdict']] = verdicts.get(r['verdict'], 0) + 1

    summary = {
        'files_analyzed': len(rows),
        'files_with_cjk': sum(1 for r in rows if r['cjk'] > 0),
        'total_cjk_chars': total_cjk,
        'total_changed_by_s2t': total_s2t,
        'total_changed_by_t2s': total_t2s,
        's2t_pct': round(100 * total_s2t / total_cjk, 3) if total_cjk else 0,
        't2s_pct': round(100 * total_t2s / total_cjk, 3) if total_cjk else 0,
        'files_by_verdict': verdicts,
        'files': rows,
    }
    out = Path(sys.argv[2] if len(sys.argv) > 2 else 'cjk_report.json')
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: summary[k] for k in summary if k != 'files'}, ensure_ascii=False, indent=2))
    print('---')
    print(f'wrote {out}')

if __name__ == '__main__':
    main()