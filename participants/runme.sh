#!/bin/bash

# abort on errors
set -u -e -o errexit

# process participants
python participants.py list > participants.tex
python participants.py html > participants.html
python participants.py tags > ../nametags/participants.tex

# LaTeX PDFs
for i in {1..3}; do xelatex list; done
(cd ../nametags; for i in {1..3}; do xelatex tags; done)
