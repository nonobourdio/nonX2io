import json, os, re, subprocess, sys

root = sys.argv[1] if len(sys.argv) > 1 else 'public'

# Markdown files that live on disk but must NOT appear in the tree.
# Currently empty: 'Home' is the landing page AND shows in the tree
# (highlighted as current when no hash is set). Keep the mechanism for
# future hidden pages.
EXCLUDE = set()

# Tree behaviour markers, read from a folder's currentfolder.md. As HTML
# comments they are invisible in the rendered page and can sit anywhere
# in the file.
#
#   <!-- tree: open -->   expand the folder in the tree at launch
#                        (absent = collapsed by default)
#   <!-- tree: recent --> sort the folder's children by most recent
#                        modification first (inherited by subfolders),
#                        instead of the default alphabetical order
OPEN_RE = re.compile(r'<!--\s*tree:\s*open\s*-->', re.IGNORECASE)
RECENT_RE = re.compile(r'<!--\s*tree:\s*recent\s*-->', re.IGNORECASE)


def read_currentfolder(dirpath):
    try:
        with open(os.path.join(dirpath, 'currentfolder.md'), encoding='utf-8') as fp:
            return fp.read()
    except FileNotFoundError:
        return None


def git_mtime(path):
    """Modification time of a path, as a unix timestamp.

    Uses the last commit touching it (git mtimes are reproducible: a
    fresh CI clone resets filesystem mtimes, which would scramble a
    purely mtime-based sort), with the filesystem mtime as fallback for
    files that are not committed yet.
    """
    try:
        out = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', '--', path],
            capture_output=True, text=True, check=True)
        ts = out.stdout.strip()
        if ts:
            return int(ts)
    except Exception:
        pass
    return int(os.path.getmtime(path))


def scan_dir(dirpath, prefix, recent=False):
    """Scan a directory and return its clickable children.

    A folder becomes a clickable tree node only if it contains a
    'currentfolder.md' inside it. Otherwise it is a plain grouping
    folder: still shown (so its children are reachable), but without
    a 'path' and therefore not clickable.

    With recent=True (or the folder's own <!-- tree: recent --> marker),
    children are sorted most-recently-modified first instead of
    alphabetically; ties keep the alphabetical order. A folder's date is
    the newest date among its own contents. '_key' is the internal sort
    key, stripped from the final JSON.
    """
    entries = []
    for entry in sorted(os.listdir(dirpath)):
        fullpath = os.path.join(dirpath, entry)

        if os.path.isdir(fullpath):
            content = read_currentfolder(fullpath)
            folder_recent = recent or (content is not None and bool(RECENT_RE.search(content)))
            children = scan_dir(fullpath, f'{prefix}{entry}/', folder_recent)
            if not children:
                continue
            item = {'name': entry, 'children': children, '_key': max(c['_key'] for c in children)}
            if content is not None:
                item['_key'] = max(item['_key'], git_mtime(os.path.join(fullpath, 'currentfolder.md')))
                item['path'] = f'{prefix}{entry}'
                if OPEN_RE.search(content):
                    item['open'] = True
            entries.append(item)

        elif entry.endswith('.md'):
            # currentfolder.md is the folder's own landing page, not a
            # standalone leaf: it is exposed via the parent folder's
            # 'path', so skip it here.
            if entry == 'currentfolder.md':
                continue
            if entry in EXCLUDE:
                continue
            name = entry[:-3]
            entries.append({'name': name, 'path': f'{prefix}{name}', '_key': git_mtime(fullpath)})

    if recent:
        entries.sort(key=lambda it: it['_key'], reverse=True)
    return entries


def strip_keys(items):
    for item in items:
        item.pop('_key', None)
        if 'children' in item:
            strip_keys(item['children'])


pages = scan_dir(root, '')

strip_keys(pages)

with open(os.path.join(root, 'tree-content.json'), 'w') as fp:
    json.dump(pages, fp, indent=2)
