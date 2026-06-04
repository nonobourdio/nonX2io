import json, os, sys

root = sys.argv[1] if len(sys.argv) > 1 else 'public'

pages = {}

for entry in sorted(os.listdir(root)):
    dirpath = os.path.join(root, entry)
    if os.path.isdir(dirpath):
        children = []
        for f in sorted(os.listdir(dirpath)):
            if f.endswith('.md'):
                name = f[:-3]
                children.append({'name': name, 'path': f'{entry}/{name}'})
        if children:
            pages[entry] = children

with open(os.path.join(root, 'ressources.json'), 'w') as fp:
    json.dump(pages, fp, indent=2)
