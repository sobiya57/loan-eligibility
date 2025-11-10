from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    Gender: str = Field(..., examples=["Male","Female"])
    Married: str = Field(..., examples=["Yes","No"])
    Dependents: str = Field(..., examples=["0","1","2","3+"])
    Education: str = Field(..., examples=["Graduate","Not Graduate"])
    Self_Employed: str = Field(..., examples=["Yes","No"])
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float = Field(..., examples=[1.0, 0.0])
    Property_Area: str = Field(..., examples=["Urban","Rural","Semiurban"])

class PredictionOut(BaseModel):
    approved: bool
    probability: float
