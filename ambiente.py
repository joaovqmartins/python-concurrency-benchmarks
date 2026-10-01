import os, sys

print("Python:", sys.version)
print("GIL está habilitado:", sys._is_gil_enabled())
print("CPUs disponíveis:", os.cpu_count())
