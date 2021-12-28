try:
    from .itemnetwork import LinkedNetwork, Hashable, HashType
except ImportError as ie:
    raise ie

try:
    from .visualization import quick_plot
except ImportError as ie:
    from importlib.util import find_spec as _find_spec

    if _find_spec("matplotlib") is None:
        print("""LinkedNetwork imported correctly""")
        print("""module matplotlib is not available, install with "pip install matplotlib" for visualisation.""")
        print("""To hide this message call "from itemnetwork import itemnetwork" """)