from datetime import datetime
from db import db

class LoanModel(db.Model):

    __tablename__='loan'

    loanId=db.Column(db.Integer,primary_key=True)
    requestDate=db.Column(db.Date,default=datetime.now())
    loanOfficerResponse=db.Column(db.String(1000),nullable=True)
    committeResponse=db.Column(db.String(100),nullable=True)
    document=db.Column(db.String(100),nullable=True)
    loanType=db.Column(db.String(40),nullable=True)
    requestStatus=db.Column(db.String(50), default='loanOfficer',nullable=True)
    loanOfficerEmail=db.Column(db.String(100),db.ForeignKey('administration.email'),nullable=True)
    clientEmail=db.Column(db.String(100),db.ForeignKey('client.email'),nullable=True)
    monthlySalary=db.Column(db.Integer,nullable=True)
    requestedLoan=db.Column(db.Integer,nullable=True)
    paymentPeriod=db.Column(db.String(8),nullable=True)
    monthlyPaybackAmount=db.Column(db.Integer,nullable=True)


    client=db.relationship('ClientModel',back_populates="loans")
    loanOfficer=db.relationship('AdministrationModel',back_populates="loans")


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, loanId: int) -> "LoanModel":
        return cls.query.get_or_404(loanId)