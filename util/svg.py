"""
File: svg.py
Author: Chuncheng Zhang
Date: 2025-06-17
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Load and use SVG objects.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-17 ------------------------
# Requirements and constants
import os
from svglib.svglib import svg2rlg
from reportlab.lib.units import inch
from reportlab.graphics import shapes

# %% ---- 2025-06-17 ------------------------
# Function and class


class SVGCache:
    cache: dict[str, shapes.Drawing] = {}

    def insert(self, key: str, drawing: shapes.Drawing):
        '''Insert the drawing into the cache by key'''
        self.cache[key] = drawing
        return drawing

    def checkout(self, key: str):
        '''Read the svg by key(in env) and insert it'''
        if key in self.cache:
            return self.cache[key]
        path = os.environ[key]
        drawing: shapes.Drawing = svg2rlg(path)
        return self.insert(key, drawing)

    def resize_drawing_by_height(self, key: str, height: float):
        '''
        Resize the drawing by given height (in inch).
        '''
        h = height * inch
        if drawing := self.checkout(key):
            k = h / drawing.height
            drawing.scale(k, k)
            return drawing


# %% ---- 2025-06-17 ------------------------
# Play ground


# %% ---- 2025-06-17 ------------------------
# Pending


# %% ---- 2025-06-17 ------------------------
# Pending
