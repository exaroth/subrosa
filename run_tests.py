#!/usr/bin/env python
import os

os.environ["CI"] = "True"

import nose
nose.run()
