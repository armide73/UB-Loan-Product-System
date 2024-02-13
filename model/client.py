from db import db

class ClientModel(db.Model):
    __tablename__ = 'client'

    email=db.Column(db.String(100),primary_key=True)
    firstName=db.Column(db.String(100),nullable=True)
    lastName=db.Column(db.String(100),nullable=True)
    phone=db.Column(db.String(15),nullable=True)
    password=db.Column(db.String(100),nullable=True)
    gender=db.Column(db.String(7),nullable=True)
    accountNumber=db.Column(db.String(100),nullable=True)
    profilePic=db.Column(db.String(100),default='avatar-1.png')


    loans=db.relationship('LoanModel',back_populates="client",lazy="dynamic")


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, email: str) -> "ClientModel":
        return cls.query.get_or_404(email)