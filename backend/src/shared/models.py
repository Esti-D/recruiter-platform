from pydantic import BaseModel
from datetime import date, datetime

# ---------- OFFERS ----------
class OfferIn(BaseModel):
    companyName: str
    contactPerson: str
    endDate: date
    role: str
    salary: str | int
    modality: str
    location: str | None = None
    description: str | None = None
    mustHave: list[str] = []
    niceToHave: list[str] = []
    notes: str | None = None

class OfferOut(OfferIn):
    offerId: str
    createdAt: datetime

class OfferUpdate(BaseModel):
    companyName: str | None = None
    contactPerson: str | None = None
    endDate: date | None = None
    role: str | None = None
    salary: str | int | None = None
    modality: str | None = None
    location: str | None = None
    description: str | None = None
    mustHave: list[str] | None = None
    niceToHave: list[str] | None = None
    notes: str | None = None


# ---------- PROCESS ----------
class ProcessIn(BaseModel): offerId:str; recruiter:str|None=None; notes:str|None=None
class CandidateInProcess(BaseModel):
    candidateId:str; name:str; role:str; experience:str|None=None; strength:str|None=None; salaryRange:str|None=None
    state:str="PENDING"; phase:str="INITIAL"; notes:str|None=None
class ProcessOut(BaseModel):
    processId:str; offerId:str; roleOffer:str; similarRoles:list[str]=[]; recruiter:str|None=None; notes:str|None=None
    status:str="OPEN"; createdAt:datetime; closedAt:datetime|None=None; candidates:list[CandidateInProcess]=[]
class ProcessUpdate(BaseModel): recruiter:str|None=None; notes:str|None=None; status:str|None=None; similarRoles:list[str]|None=None



# ---------- CANDIDATES ----------
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CandidateIn(BaseModel):
    dni: str
    name: str
    role: str
    experience: str | None = None
    location: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    status: str | None = None      # p.ej. "OPEN","QUIET","BLOCKED"
    strength: str | None = None    # fortaleza
    salaryRange: str | None = None
    notes: str | None = None

class CandidateOut(CandidateIn):
    candidateId: str
    createdAt: datetime

class CandidateUpdate(BaseModel):
    dni: str | None = None; name: str | None = None; role: str | None = None
    experience: str | None = None; location: str | None = None
    email: EmailStr | None = None; phone: str | None = None
    status: str | None = None; strength: str | None = None
    salaryRange: str | None = None; notes: str | None = None

class RoleIn(BaseModel):
    name: str

class RoleOut(RoleIn):
    roleId: str
    createdAt: datetime

class RoleUpdate(BaseModel):
    name: str | None = None
