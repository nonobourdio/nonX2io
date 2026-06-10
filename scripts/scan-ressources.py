import json, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else 'public'

def scan_dir(dirpath, prefix):
    entries = []
    for entry in sorted(os.listdir(dirpath)):
        fullpath = os.path.join(dirpath, entry)
        if os.path.isdir(fullpath):
            children = scan_dir(fullpath, f'{prefix}{entry}/')
            if children:
                item = {'name': entry, 'children': children}
                md_path = os.path.join(dirpath, entry + '.md')
                if os.path.exists(md_path):
                    item['path'] = f'{prefix}{entry}'
                entries.append(item)
        elif entry.endswith('.md'):
            name = entry[:-3]
            entries.append({'name': name, 'path': f'{prefix}{name}'})
    return entries

pages = []
for entry in sorted(os.listdir(root)):
    dirpath = os.path.join(root, entry)
    if os.path.isdir(dirpath):
        children = scan_dir(dirpath, f'{entry}/')
        if children:
            item = {'name': entry, 'children': children}
            md_path = os.path.join(root, entry + '.md')
            if os.path.exists(md_path):
                item['path'] = entry
            pages.append(item)

with open(os.path.join(root, 'tree-content.json'), 'w') as fp:
    json.dump(pages, fp, indent=2)
