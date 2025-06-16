"""
File: config.py
Author: Chuncheng Zhang
Date: 2025-06-16
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Register the configuration.

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
from omegaconf import OmegaConf
from util.log import logger

CONF = OmegaConf.load('config.yaml')

# %% ---- 2025-06-16 ------------------------
# Function and class

# %% ---- 2025-06-16 ------------------------
# Play ground
projectEnvName = 'pdfFactory'

font = {'font.cn.path': CONF.Font.CN.Path}
svg = {'svg.logo.path': CONF.Svg.Logo.Path,
       'svg.frame.path': CONF.Svg.Frame.Path}

updates = {}
for dct in [font, svg]:
    updates.update({'.'.join([projectEnvName, k]): v for k, v in dct.items()})

os.environ.update(updates)

logger.info(f'Using environments: {updates}')

# %% ---- 2025-06-16 ------------------------
# Pending


# %% ---- 2025-06-16 ------------------------
# Pending
