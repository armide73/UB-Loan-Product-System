import functools
from flask import Flask, jsonify,request,render_template,redirect,flash, send_from_directory,session, url_for
from flask_migrate import Migrate
from db import db
from werkzeug.utils import secure_filename
from model import ClientModel,AdministrationModel,LoanModel
from sqlalchemy import and_
import os
from dotenv import load_dotenv
from zipfile import ZipFile
import shutil
from sendmail import ToSendMail

load_dotenv()



app = Flask(__name__)

app.secret_key='oBQ4GBTlzpSwE2OCGzRCGcXVANO9bsYZL_Cf3CSEXPs'
app.config["SQLALCHEMY_DATABASE_URI"] =os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate=Migrate(app,db)


def login_required(route):
    @functools. wraps(route)
    def route_wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for("home"))
        return route(*args, **kwargs)
    return route_wrapper


@app.route("/committe-view-client")
@login_required
def committeAllClient():
    clienLoans=LoanModel.query.all()
    return render_template("committeeAllClient.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))


@app.route("/loanofficer-client-report")
@login_required
def loanOfficerReport():
    clienLoans=LoanModel.query.all()
    return render_template("loanOfficerReport.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))


@app.route("/loanofficer-allclient")
@login_required
def loanOfficerAllClient():
    clienLoans=LoanModel.query.all()
    return render_template("loanOfficerAllClient.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))


@app.route("/administration_profile_picture", methods=["POST"])
def administration_profile_picture():
    
    # Get the file from the request
    file = request.files["file"]
    
    # Save the file to the filesystem
    filename = secure_filename(file.filename)
    filename=session['email']+'.'+ filename.split('.')[1]
    file.save(os.path.join("./static/public/assets/profile", filename))
    
    # Update the user's profile picture in the database
    administationUser=AdministrationModel.find_by_id(session.get('email'))
    administationUser.profilePic=filename
    try:
        administationUser.save_to_db()
        session['profilePic']=filename
        flash('Profile Updated')
    except:
        flash('An error occurred! Please try again')
    # Return the success response
    return jsonify({"success": True})


@app.route("/client_profile_picture", methods=["POST"])
def client_profile_picture():
    
    # Get the file from the request
    file = request.files["file"]
    
    # Save the file to the filesystem
    filename = secure_filename(file.filename)
    filename=session['email']+'.'+ filename.split('.')[1]
    file.save(os.path.join("./static/public/assets/profile", filename))
    
    # Update the user's profile picture in the database
    client_user=ClientModel.find_by_id(session.get('email'))
    client_user.profilePic=filename
    try:
        client_user.save_to_db()
        session['profilePic']=filename
        flash('Profile Updated')
    except:
        flash('An error occurred! Please try again')
    # Return the success response
    return jsonify({"success": True})


@app.route("/client-profile", methods=["POST","GET"])
@login_required
def clientProfile():
    client=ClientModel.find_by_id(session.get('email'))
    if request.method == "POST":
        client.firstName=request.form.get("firstName")
        client.lastName=request.form.get("lastName")
        client.phone=request.form.get("phone")
        client.gender=request.form.get("gender")
        client.accountNumber=request.form.get("accountNumber")
        try:
            client.save_to_db()
            flash('Profile Updated')
        except:
            flash('An error occurred! Please try again')

    return render_template('clientProfile.html',profilePic=session.get('profilePic'),client=client)


@app.route("/administration-profile", methods=["POST","GET"])
@login_required
def administrationProfile():
    administration=AdministrationModel.find_by_id(session.get('email'))
    if request.method == "POST":
        administration.firstName=request.form.get("firstName")
        administration.lastName=request.form.get("lastName")
        administration.phone=request.form.get("phone")
        administration.gender=request.form.get("gender")
        try:
            administration.save_to_db()
            flash('Profile Updated')
        except:
            flash('An error occurred! Please try again')

    return render_template('administrationProfile.html',profilePic=session.get('profilePic'),client=administration)


@app.route("/client-check-response/<string:loanId>", methods=["POST","GET"])
@login_required
def clientCheckResponse(loanId):
    loan=LoanModel.find_by_id(loanId)
    if request.method == "POST":
        loan.requestStatus='loanOfficer'
        loan.loanType=request.form.get("loanType")
        requestReason=request.files.get("requestReason")
        employmentContract=request.files.get("employmentContract")
        salaryCertificate=request.files.get("salaryCertificate")
        latestTwoMonthsCertified=request.files.get("latestTwoMonthsCertified")
        commitmentLetter=request.files.get("commitmentLetter")
        IDCopy=request.files.get("IDCopy")
        valuationReport=request.files.get("valuationReport")
        proofOfLegalStatus=request.files.get("proofOfLegalStatus")
        lifeInsurance=request.files.get("lifeInsurance")
        
        temp_dir = "temp_zip"
        os.makedirs(temp_dir, exist_ok=True)

        try:
        # Save each file to the temporary directory
            files_to_zip = [
                (requestReason.filename, requestReason),
                (employmentContract.filename, employmentContract),
                (salaryCertificate.filename, salaryCertificate),
                (latestTwoMonthsCertified.filename, latestTwoMonthsCertified),
                (commitmentLetter.filename, commitmentLetter),
                (IDCopy.filename, IDCopy),
                (valuationReport.filename, valuationReport),
                (proofOfLegalStatus.filename, proofOfLegalStatus),
                (lifeInsurance.filename, lifeInsurance),
            ]
            
            for filename, file_content in files_to_zip:
                if file_content:
                    filepath = os.path.join(temp_dir, filename)
                    file_content.save(filepath)
            # Create a zip file in the "loanFile" directory
            loanfile_dir = "loanFiles"
            os.makedirs(loanfile_dir, exist_ok=True)
            zip_filename = f"client_files_{loan.loanId}.zip"
            zip_filepath = os.path.join(loanfile_dir, zip_filename)
            with ZipFile(zip_filepath, "w") as zipf:
                for filename, _ in files_to_zip:
                    filepath = os.path.join(temp_dir, filename)
                    zipf.write(filepath, os.path.basename(filepath))

            loan.document=zip_filename
            loan.save_to_db()

            # delete temporary files and directory
            shutil.rmtree(temp_dir)
            flash("you request have successfully created")
        except:
            flash("Loan Request is not created")

    return render_template("clientCheckResponse.html",username=session.get('username'),clientName=f'{loan.client.firstName} {loan.client.lastName}',loan=loan,profilePic=session.get('profilePic'))


@app.route("/create-administration-account", methods=["POST","GET"])
@login_required
def createCommitteeAccount():
    administration=AdministrationModel()
    if request.method == "POST":
        administration.firstName=request.form.get("firstName")
        administration.lastName=request.form.get("lastName")
        administration.email=request.form.get("email")
        administration.phone=request.form.get("phone")
        administration.gender=request.form.get("gender")
        administration.password=request.form.get("password")
        administration.status=request.form.get("status")
        try:
            administration.save_to_db()
            flash('New account created')
        except:
            flash('An error occurred! Please try again')

    return render_template('createCommitteeAC.html',profilePic=session.get('profilePic'))


@app.route("/")
@app.route("/home")
def home():
    return render_template('pages/index.html')


@app.errorhandler(404)
def pageNoFound(error):
    return render_template('pages/404page.html'), 404


@app.route("/committee-reject/<string:loanId>", methods=["POST","GET"])
@login_required
def committeeReject(loanId):
    loan=LoanModel.find_by_id(loanId)
    if request.method == "POST":
        loan.requestStatus='denied'
        loan.committeResponse=request.form.get('committeResponse')
        try:
            loan.save_to_db()
            flash(f'{loan.client.firstName} {loan.client.lastName} received your response')
            return redirect(url_for("committeeDashboard"))
        except:
            flash('Error happen')
    return render_template("committeeReject.html",username=session.get('username'),clientName=f'{loan.client.firstName} {loan.client.lastName}',profilePic=session.get('profilePic'))


@app.route("/committee-approval/<string:loanId>", methods=["POST","GET"])
@login_required
def committeeApproval(loanId):
    loan=LoanModel.find_by_id(loanId)
    loan.requestStatus='approved'
    try:
            loan.save_to_db()
            flash(f'{loan.client.firstName} {loan.client.lastName} received your response')
    except:
        flash('Error happen')
    return redirect(url_for("committeeDashboard"))


@app.route("/committee-dashboard", methods=["POST","GET"])
@login_required
def committeeDashboard():
    clienLoans=LoanModel.query.filter(LoanModel.requestStatus=='committee').all()
    return render_template("committeeDashboard.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))


@app.route("/loan-officer-reject/<string:loanId>", methods=["POST","GET"])
@login_required
def loanOfficerReject(loanId):
    loan=LoanModel.find_by_id(loanId)
    if request.method == "POST":
        loan.requestStatus=request.form.get('requestStatus')
        loan.loanOfficerResponse=request.form.get('loanOfficerResponse')
        try:
            loan.save_to_db()
            flash(f'{loan.client.firstName} {loan.client.lastName} received your response')
            return redirect(url_for("loanOfficerDashboard"))
        except:
            flash('Error happen')
    return render_template("loanOfficerReject.html",username=session.get('username'),clientName=f'{loan.client.firstName} {loan.client.lastName}',profilePic=session.get('profilePic'))


@app.route("/loan-officer-to-committee/<string:loanId>", methods=["POST","GET"])
@login_required
def loanOfficerToCommittee(loanId):
    loan=LoanModel.find_by_id(loanId)
    loan.requestStatus='committee'
    loan.loanOfficerEmail=session.get('email')
    try:
            loan.save_to_db()
            flash(f'{loan.client.firstName} {loan.client.lastName} received your response')
    except:
        flash('Error happen')
    return redirect(url_for("loanOfficerDashboard"))


@app.route("/loan-officer-dashboard", methods=["POST","GET"])
@login_required
def loanOfficerDashboard():
    clienLoans=LoanModel.query.filter(LoanModel.requestStatus=='loanOfficer').all()
    return render_template("loanOfficerDashboard.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))


@app.route("/administation-login", methods=["POST","GET"])
def administationLogin():
    
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")

        try:
            adminInfo=AdministrationModel.find_by_id(email)
            if(adminInfo.password == password):
                session['email']=adminInfo.email
                session['status']=adminInfo.status
                session['username']=f'{adminInfo.firstName} {adminInfo.lastName}'
                session['profilePic']=adminInfo.profilePic
                if adminInfo.status=='committee':
                    return redirect(url_for("committeeDashboard"))
                elif adminInfo.status=='loan officer':
                    return redirect(url_for("loanOfficerDashboard"))
            else:
                flash('Invalid Email or Password')
        except:
            flash('Invalid Email or Password')
    return render_template("pages/administationLogin.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/loan-files-download/<string:loanId>')
def loanFilesDownload(loanId):
    test= LoanModel.find_by_id(loanId)
    return send_from_directory('./loanFiles',f'{test.document}',as_attachment=True,download_name=f'{test.client.firstName} {test.client.lastName} - {test.requestDate}.zip')


@app.route("/client-loan-form", methods=["POST","GET"])
@login_required
def clientLoanForm():

    if request.method == "POST":
        loan=LoanModel()
        loan.loanType=request.form.get("loanType")
        loan.monthlySalary=int(request.form.get("monthlySalary"))
        loan.requestedLoan=int(request.form.get("requestedLoan"))
        loan.monthlyPaybackAmount=int(request.form.get("monthlyPaybackAmount"))
        loan.paymentPeriod=request.form.get("paymentPeriod")
        requestReason=request.files.get("requestReason")
        employmentContract=request.files.get("employmentContract")
        salaryCertificate=request.files.get("salaryCertificate")
        latestTwoMonthsCertified=request.files.get("latestTwoMonthsCertified")
        commitmentLetter=request.files.get("commitmentLetter")
        IDCopy=request.files.get("IDCopy")
        valuationReport=request.files.get("valuationReport")
        proofOfLegalStatus=request.files.get("proofOfLegalStatus")
        lifeInsurance=request.files.get("lifeInsurance")

        loan.clientEmail=session.get("email")
        loan.save_to_db()
        
        temp_dir = "temp_zip"
        os.makedirs(temp_dir, exist_ok=True)

        try:
        # Save each file to the temporary directory
            files_to_zip = [
                (requestReason.filename, requestReason),
                (employmentContract.filename, employmentContract),
                (salaryCertificate.filename, salaryCertificate),
                (latestTwoMonthsCertified.filename, latestTwoMonthsCertified),
                (commitmentLetter.filename, commitmentLetter),
                (IDCopy.filename, IDCopy),
                (valuationReport.filename, valuationReport),
                (proofOfLegalStatus.filename, proofOfLegalStatus),
                (lifeInsurance.filename, lifeInsurance),
            ]
            
            for filename, file_content in files_to_zip:
                if file_content:
                    filepath = os.path.join(temp_dir, filename)
                    file_content.save(filepath)
            # Create a zip file in the "loanFile" directory
            loanfile_dir = "loanFiles"
            os.makedirs(loanfile_dir, exist_ok=True)
            zip_filename = f"client_files_{loan.loanId}.zip"
            zip_filepath = os.path.join(loanfile_dir, zip_filename)
            with ZipFile(zip_filepath, "w") as zipf:
                for filename, _ in files_to_zip:
                    filepath = os.path.join(temp_dir, filename)
                    zipf.write(filepath, os.path.basename(filepath))

            loan.document=zip_filename
            loan.save_to_db()

            # delete temporary files and directory
            shutil.rmtree(temp_dir)
            flash("you request have successfully created")
        except:
            flash("Loan Request is not created")

    return render_template("clientLoanForm.html",username=session.get('username'),email=session.get('email'),profilePic=session.get('profilePic'))


@app.route("/client-dashboard", methods=["POST","GET"])
@login_required
def clientDashboard():
    clienLoans=LoanModel.query.filter(LoanModel.clientEmail==session.get('email'))
    return render_template("clientLanding.html",username=session.get('username'),clienLoans=clienLoans,profilePic=session.get('profilePic'))



@app.route("/client-login", methods=["POST","GET"])
def clientLogin():
    
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")

        try:
            clientInfo=ClientModel.find_by_id(email)
            if(clientInfo.password == password):
                session['email']=clientInfo.email
                session['status']='client'
                session['username']=f'{clientInfo.firstName} {clientInfo.lastName}'
                session['profilePic']=clientInfo.profilePic
                return redirect(url_for("clientDashboard"))
            else:
                flash('Invalid Email or Password')
        except:
            flash('Invalid Email or Password')
    return render_template("pages/login.html")


@app.route("/client-create-account", methods=["POST","GET"])
def clientCreateAccount():
    client=ClientModel()
    if request.method == "POST":
        client.firstName=request.form.get("firstName")
        client.lastName=request.form.get("lastName")
        client.email=request.form.get("email")
        client.phone=request.form.get("phone")
        client.gender=request.form.get("gender")
        client.password=request.form.get("password")
        client.accountNumber=request.form.get("bankAccount")
        try:
            client.save_to_db()
            newAccountEmail= ToSendMail()
            newAccountEmail.send_simple_message(username=f'{client.firstName} {client.lastName}')
            flash('New account created')
            return redirect(url_for("clientLogin"))
        except:
            flash('An error occurred! Please try again')

    return render_template("pages/create-account.html")

