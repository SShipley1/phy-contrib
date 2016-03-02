# -*- coding: utf-8 -*-

"""phycontrib."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import logging
import os
import os.path as op
import shutil
from textwrap import dedent

from . import kwik_gui  # noqa

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
# Default config and state files
#------------------------------------------------------------------------------

def _create_loader_file():
    """Create a Python script that imports phycontrib in the
    plugins directory. This ensures that phycontrib's plugins are always
    loaded by phy."""
    # Make sure the plugins directory exists.
    plugins_dir = op.expanduser('~/.phy/plugins/')
    if not op.exists(plugins_dir):
        os.makedirs(plugins_dir)
    # Create the script if it doesn't already exist.
    path = plugins_dir + 'phycontrib_loader.py'
    if op.exists(path):
        return
    with open(path, 'w') as f:
        f.write(dedent("""
                # Automatically generated by phycontrib's installer.
                # This imports all of phycontrib's plugins when loading phy.
                import phycontrib
                """).lstrip())


def _copy_gui_state(gui_name, module_name):
    """Copy the state.json file."""
    gui_dir = op.expanduser('~/.phy/%s/' % gui_name)
    if not op.exists(gui_dir):
        os.makedirs(gui_dir)
    # Create the script if it doesn't already exist.
    path = gui_dir + 'state.json'
    if op.exists(path):
        return
    curdir = op.dirname(op.realpath(__file__))
    from_path = op.join(curdir, module_name, 'static', 'state.json')
    logger.debug("Copy %s to %s" % (from_path, path))
    shutil.copy(from_path, path)


def _copy_all_gui_states():
    _copy_gui_state('KwikGUI', 'kwik_gui')
    _copy_gui_state('TemplateGUI', 'template')


# Copy default states when importing the package.
_copy_all_gui_states()
