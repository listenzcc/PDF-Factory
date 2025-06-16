"""
File: main.py
Author: Chuncheng Zhang
Date: 2025-06-16
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Main entrance for the project.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-16 ------------------------
# Requirements and constants
import os
from rich import print

from config import CONF
from util.pdf import PDFGenerator

# %% ---- 2025-06-16 ------------------------
# Function and class


# %% ---- 2025-06-16 ------------------------
# Play ground
generator = PDFGenerator()


# ----------------------------------------
# ---- First Page ----
# generator.insert_paragraph('Auto Generated PDF', style='cTitle')
# generator.insert_paragraph('Author: Listenzcc', style='cCenteredText')
generator.insert_page_break()


# ----------------------------------------
# ---- Content of Styles ----
generator.insert_paragraph('Styles (样式集)', style='cSubTitle')

styles = generator.styles
for name in styles.byName:
    generator.insert_paragraph(name, style='cCenteredText')
    lst = []
    for k in [e for e in dir(styles[name]) if not e.startswith('_')]:
        v = getattr(styles[name], k)
        lst.append(f'{k}: {v}')
    generator.insert_paragraph('{'+',\t'.join(lst)+'}', style='code')


# ----------------------------------------
# ---- Build and Save ----
generator.build()
generator.save('pdf/a.pdf')


# %% ---- 2025-06-16 ------------------------
# Pending


# %% ---- 2025-06-16 ------------------------
# Pending
