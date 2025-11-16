# frontend/src/main.py
from PySide6.QtWidgets import QApplication; from app import MainWindow; import sys
app=QApplication(sys.argv); w=MainWindow(); w.show(); sys.exit(app.exec())