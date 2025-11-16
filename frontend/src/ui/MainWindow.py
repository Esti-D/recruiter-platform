from PySide6.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QToolBar
from views.CandidatesView import CandidatesView
from views.OffersView import OffersView
from views.ProcessView import ProcessView
from views.RolesView import RolesView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("Recruiter Desktop"); self.resize(1000,700)
        self.stack=QStackedWidget(); self.setCentralWidget(self.stack)
        self.candidates=CandidatesView()
        self.offers=OffersView() 
        self.process=ProcessView()
        self.roles=RolesView()

        for w in (self.candidates,self.offers,self.process,self.roles): 
            self.stack.addWidget(w)

        tb=QToolBar("Nav"); 
        self.addToolBar(tb)
        for i,name in enumerate(("Candidates","Offers","Process","Roles")):
            b=QPushButton(name); b.clicked.connect(lambda _,ix=i:self.stack.setCurrentIndex(ix)); 
            tb.addWidget(b)
