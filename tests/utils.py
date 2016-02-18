# -*- coding: utf-8 -*-
import os
import sys
from tg import AppConfig


def make_appcfg_for_controller(root_controller):
    # Add testing dir to path, so that we can import fakeapp
    sys.path.append(os.path.dirname(__file__))

    config = AppConfig(minimal=True, root_controller=root_controller)
    config['package'] = __import__('fakeapp')
    return config
