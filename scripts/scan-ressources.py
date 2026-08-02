import json, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else 'public'

# Markdown files that live on disk but must NOT appear in the tree.
# 'Home' is the default landing page (loaded when no hash is set), so it
# has no reason to clutter the navigation.
EXCLUDE = {'Home.md'}


def scan_dir(dirpath, prefix):
    """Scan a directory and return its clickable children.

    A folder becomes a clickable tree node only if it contains a
    'currentfolder.md' inside it. Otherwise it is a plain grouping
    folder: still shown (so its children are reachable), but without
    a 'path' and therefore not clickable.
    """
    entries = []
    for entry in sorted(os.listdir(dirpath)):
        fullpath = os.path.join(dirpath, entry)

        if os.path.isdir(fullpath):
            children = scan_dir(fullpath, f'{prefix}{entry}/')
            if not children:
                continue
            item = {'name': entry, 'children': children}
            if os.path.exists(os.path.join(fullpath, 'currentfolder.md')):
                item['path'] = f'{prefix}{entry}'
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
            entries.append({'name': name, 'path': f'{prefix}{name}'})

    return entries


pages = scan_dir(root, '')

with open(os.path.join(root, 'tree-content.json'), 'w') as fp:
    json.dump(pages, fp, indent=2)
