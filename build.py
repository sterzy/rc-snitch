#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

summary      = "A utility to interact with an Arduino based 433MHz transceiver."
name         = "rc-snitch"
authors      = [ Author("Stefan Sterz", "hi@sterzy.com") ]
default_task = "publish"
license      = "MIT"

@init
def initialize(project):
    project.depends_on_requirements("requirements.txt")
    project.set_property("distutils_entry_points", {
        "console_scripts" : [
            "rc-snitch = main:main"
        ]
    })
    pass
