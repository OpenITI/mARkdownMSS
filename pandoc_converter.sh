#!/bin/sh

pandoc -s /Users/romanov/Dropbox/0_Zettelkasten/research_vault/mARkdownMSS\ -\ NOTES.md -o mARkdownMSS.html


# HTML fragment:
#pandoc MANUAL.txt -o example1.html

# Standalone HTML file:
#pandoc -s MANUAL.txt -o example2.html

# HTML with table of contents, CSS, and custom footer:
#pandoc -s --toc -c pandoc.css -A footer.html MANUAL.txt -o example3.html