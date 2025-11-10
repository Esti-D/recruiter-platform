from pydantic import BaseModel
class OfferIn(BaseModel): offerId:str; role:str; tags:list[str]=[]; createdBy:str
class OfferOut(BaseModel): offerId:str; status:str="CREATED"

class ProcessIn(BaseModel): offerId: str
class ProcessOut(BaseModel): processId: str; offerId: str; status: str = "READY"

class CandidateOut(BaseModel):
    candidateId: str
    name: str
    role: str
    skills: list[str]
