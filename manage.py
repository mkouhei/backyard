# -*- coding: utf-8 -*-
"""backyard.manage."""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "backyard.core.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
