# -*- coding: utf-8 -*-
# Author: Parrot Developers
# License: MPL 2.0 https://www.mozilla.org/en-US/MPL/2.0/

from .utils.resolve import Resolver
from .plugins import *

def resolve(module, imdbid, episode=None):
    """
    Args:
        module (str): Plugin to use
        imdbid (str): imdbid to grab

    Returns:
        rmf (ResolvedMediaFile): use .url or .headers to get data, .test() to test if stream works
    """

    # Filename / Classname in python cannot start with int
    if module[0].isdigit(): module = f"N{module}"

    return Resolver().resolve(module, imdbid, episode)
    