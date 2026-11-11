# Imports one imgsli-style set into a mod's folder: <set>/<n_view>/<n - label>.jpg -> <mod>/images/<slug>/<view>/<n>.jpg
# (downscaled), and adds or replaces its entry in <mod>/comparisons.json.
#
#   python tools/import_imgsli.py <mod> <set folder> <slug> "<title>" "<description>" [--pair A B] [--skip LABEL ...] [--label OLD=NEW ...] [--width 3840]
#
# <mod>: the mod's folder name, also its part of the address (e.g. slowlandscapelodgen). Created if new; set its
# "title" in <mod>/comparisons.json.
# --pair: the two images the pages open with, left first, by the number in their file names. Scenes where one of them
# is missing open with their first two. Byte-identical duplicates within a scene are skipped.
# --skip: labels (as in the file names) of images to leave out. --label: replace a label from the file names.
import argparse, hashlib, json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ap = argparse.ArgumentParser()
ap.add_argument('mod'); ap.add_argument('src'); ap.add_argument('slug'); ap.add_argument('title'); ap.add_argument('description')
ap.add_argument('--pair', nargs=2, type=int, default=[1, 2]); ap.add_argument('--skip', nargs='*', default=[]); ap.add_argument('--label', nargs='*', default=[]); ap.add_argument('--width', type=int, default=3840)
a = ap.parse_args()
RENAME = dict(x.split('=', 1) for x in a.label)
assert a.mod not in ('assets', 'tools'), 'that folder name is taken'
MOD = os.path.join(ROOT, a.mod)
DATA = os.path.join(MOD, 'comparisons.json')

views = []
for vd in sorted(os.listdir(a.src)):
    m = re.match(r'(\d+)_(.+)', vd)
    if not m or not os.path.isdir(os.path.join(a.src, vd)):
        continue
    vslug = m.group(2).replace('_', '-')
    out_dir = os.path.join(MOD, 'images', a.slug, vslug); os.makedirs(out_dir, exist_ok=True)
    images, seen, numbers = [], set(), []
    for f in sorted(os.listdir(os.path.join(a.src, vd)), key=lambda f: int(f.split(' ')[0])):
        n, label = re.match(r'(\d+) - (.+)\.jpg$', f).groups()
        if label in a.skip:
            continue
        digest = hashlib.md5(open(os.path.join(a.src, vd, f), 'rb').read()).hexdigest()
        if digest in seen:
            print(f'  skipped {vd}/{f}: same file as an earlier one'); continue
        seen.add(digest); numbers.append(int(n))
        im = Image.open(os.path.join(a.src, vd, f)).convert('RGB')
        if im.width > a.width:
            im = im.resize((a.width, round(im.height * a.width / im.width)), Image.LANCZOS)
        rel = f'images/{a.slug}/{vslug}/{n}.jpg'   # relative to the mod's folder
        im.save(os.path.join(MOD, rel), quality=85, optimize=True, progressive=True)
        images.append({'label': RENAME.get(label, label), 'src': rel})
    pair = [numbers.index(x) + 1 for x in a.pair] if all(x in numbers for x in a.pair) else [1, 2]
    views.append({'slug': vslug, 'name': vslug.replace('-', ' ').capitalize(), 'pair': pair, 'images': images})
    print(a.mod, a.slug, vslug, len(images), 'images', flush=True)

data = json.load(open(DATA, encoding='utf-8')) if os.path.exists(DATA) else {'title': a.mod, 'comparisons': []}
entry = {'slug': a.slug, 'title': a.title, 'description': a.description, 'views': views}
old = next((c for c in data['comparisons'] if c['slug'] == a.slug), {})
if 'main_view' in old:   # keep the opening scene set by hand
    entry['main_view'] = old['main_view']
slugs = [c['slug'] for c in data['comparisons']]   # replace in place, new ones go last
if a.slug in slugs:
    data['comparisons'][slugs.index(a.slug)] = entry
else:
    data['comparisons'].append(entry)
json.dump(data, open(DATA, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
