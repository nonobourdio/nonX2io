# Subsites: HTML pages inside the site

A "subsite" is any `.html` file inside `public/`. It shows up in the tree by itself, in the folder where you put it, and opens inside the panel like a Markdown page does.

The page is a normal standalone web page, so it can be made with any tool, or written by hand. `templates/subsite.html` is an empty page that already has the colours and fonts of the site, ready to be filled in.

## Add a page

1. Create the page with your tool and export it as plain HTML.
2. Put the file inside a folder of `public/`, next to your `.md` pages. If the tool also exports a folder of images or scripts, keep it next to the file.
3. Push. The page is now in the tree.

## Rules

- **The file name is the label in the tree.** `Ma page.html` shows up as "Ma page".
- **Never name it `index.html`.** That name is the frame itself, and it never shows in the tree. Rename the file: its links keep working.
- **Nothing outside `public/` is published.** That is where `templates/` and this guide live.
- **Put the file directly where you want it in the tree.** A folder that only contains your page shows up in the tree as well, so the name would appear twice. Keep the page in the folder and its assets folder next to it, for example `Portfolio/Ma page.html` and `Portfolio/Ma page_files/`.
- **No PHP or any other server feature.** Neocities only serves files.
- **Keep videos on YouTube, Vimeo or imgur**, as the rest of the site does. Neocities does not accept video files on a free account.
- **Avoid heights based on the window**, such as `100vh`. The panel is sized to fit the page, not the other way around.
- **Design for about 770 to 1100 px wide on a computer**, and make sure it still stacks on a phone. The panel is 60% of the window width at most. A page wider than the panel gets a horizontal scrollbar of its own.
- **A page has no scrollbar inside the panel.** The panel is always exactly as tall as the page, including while its images arrive, and it follows when the window is resized.

## Links inside a page

- **To another page of the site:** use `index.html#` followed by what you see in the address bar after the `#` when that page is open. For example `index.html#Portfolio/Perso/2026/Chaines`. A link to another subsite can also use its file name, for example `Ma page.html`.
- **To a section of the same page:** give the section an `id` and link to it with `#`, for example `#bas`. The main window scrolls to it.
- **To another website:** a normal link. It opens in a new tab, like the links of the Markdown pages.

## Match the frame

| What | Value |
| --- | --- |
| Page background | `#0f1214` |
| Text | `#e6e2d6` |
| Links | `#e5f5ff` |
| Borders, lines | `#555` |
| Body text | 18px, Calibri |
| Big titles | Space Grotesk (a Google Font) |

## Preview on your computer

In a terminal, from the folder of the project:

```
python scripts\scan-ressources.py public
python -m http.server 8000 --directory public
```

Then open http://localhost:8000 in a browser. The first line updates the tree, the second one shows the site. Close the terminal to stop it.

Opening `index.html` by double-clicking it does not work: the site needs to be served.
