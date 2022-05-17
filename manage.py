#!/usr/bin/env python

import os
import sys
from pathlib import Path

import environ


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    env = environ.Env()
    env.read_env(Path(__file__).resolve().parent / '.env')
    sys.dont_write_bytecode = env.get_value('DEBUG', cast=bool, default=False)
    main()
