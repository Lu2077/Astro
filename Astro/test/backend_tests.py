"""
Backend-tests module
for incrementally testing -
- from core modules to full setup -
 --proyecto-astro/Astro/Astro/test/test_celes_trak.py
"""

import os
from pathlib import Path

import pytest

from Astro.test.test_celes_trak import celes_trak_starlink_tle_test

def test_celes_trak_starlink_tle_test():
    return celes_trak_starlink_tle_test()
