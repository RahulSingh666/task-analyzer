#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_analyzer.settings')
    try:
        from importlib import import_module
        execute_from_command_line = import_module('django.core.management').execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not installed") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
