"""Encaminha execução para src/farm.py (código-fonte no padrão de pastas FIAP)."""
import os
import runpy
import sys

_root = os.path.dirname(os.path.abspath(__file__))
_src_dir = os.path.join(_root, "src")
sys.path.insert(0, _src_dir)
runpy.run_path(os.path.join(_src_dir, "farm.py"), run_name="__main__")
