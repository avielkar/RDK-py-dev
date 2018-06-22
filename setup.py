from distutils.core import setup
import py2exe
setup(console=['init_rdk.py'], requires=['matplotlib', 'psychopy', 'pandas', 'numpy'])
