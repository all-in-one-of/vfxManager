try:
	from PySide2.QtCore import * 
	from PySide2.QtGui import * 
	from PySide2.QtWidgets import *
	from PySide2 import __version__
except ImportError:
	from PySide.QtCore import * 
	from PySide.QtGui import * 
	from PySide import __version__