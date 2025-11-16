from PySide6.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QToolBar
from views.CandidatesView import CandidatesView
from views.OffersView import OffersView
from views.ProcessView import ProcessView
from views.RolesView import RolesView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recruiter Desktop"); self.resize(1000,700)

        self.stack = QStackedWidget(); self.setCentralWidget(self.stack)
        self.view_candidates = CandidatesView()
        self.view_offers = OffersView()
        self.view_process = ProcessView()
        self.view_roles = RolesView()
        self.stack.addWidget(self.view_candidates)   # index 0
        self.stack.addWidget(self.view_offers)       # index 1
        self.stack.addWidget(self.view_process)      # index 2
        self.stack.addWidget(self.view_roles)        # index 3

        tb = QToolBar("Nav"); self.addToolBar(tb)
        btn_c = QPushButton("Candidates"); btn_c.clicked.connect(lambda: self.stack.setCurrentIndex(0)); tb.addWidget(btn_c)
        btn_o = QPushButton("Offers");     btn_o.clicked.connect(lambda: self.stack.setCurrentIndex(1)); tb.addWidget(btn_o)
        btn_p = QPushButton("Process");    btn_p.clicked.connect(lambda: self.stack.setCurrentIndex(2)); tb.addWidget(btn_p)
        btn_r = QPushButton("Roles");      btn_r.clicked.connect(lambda: self.stack.setCurrentIndex(3)); tb.addWidget(btn_r)
