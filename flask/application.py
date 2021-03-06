from flask import Flask,render_template,request,jsonify
from flask_mail import Mail,Message 
from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_mail import Mail,Message 
from flask import Flask,render_template,request
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
rf = pickle.load(open('/home/abhimat/Desktop/Case Files/Nemesis-main/flask/finalized_model.sav', 'rb'))


app=Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='nemesisunited01@gmail.com'
app.config['MAIL_PASSWORD']='Demo@123'
app.config['MAIL_DEFAULT_SENDER']='nemesisunited01@gmail.com'
mail=Mail(app)
email = 'abhimatg0004@gmail.com'


@app.route('/index')
def index():
	return render_template("index.html") 


@app.route('/index_doctors')
def index_doctors():
	return render_template("index_doctors.html") 


@app.route('/patient_query')
def patient_query():
	return render_template("patient_query.html") 


@app.route('/patient_appointments')
def patient_appointments():
	return render_template("patient_appointments.html") 


@app.route('/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		u_name = request.form['user_name']
		if len(u_name) != 0:
			if u_name == "abhi0444":
				return redirect(url_for("index"))
			else:
				return redirect(url_for("index_doctors"))
	return render_template('login.html')  



@app.route('/about')
def about():
	return render_template('about.html') 

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/analysis')
def doctors():
	return render_template('analysis.html')



@app.route('/order')
def order():
	return render_template('order.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
	if request.method == 'POST':
		#name = request.form['name']
		#email = request.form['email']
		i = request.form.get('age',type=int)
		race = request.form['race']
		ethnicity = request.form['eth']
		gender = request.form['gender']
		health = request.form['healthcare']

		X = pd.DataFrame()
		X['HEALTHCARE_COVERAGE'] = [health]
		if i >= 60:
			X['Age'] = [1]
		elif (i >= 25 and i < 60):
			X['Age'] = [2]
		else:
			X['Age'] = [3]
		
		if race == 'White':
			X['Race'] = [1]
		else:
			X['Race'] = [0]

		if ethnicity == 'Nonhispanic':
			X['ETHNICITY_nonhispanic'] = 1
		else:
			X['ETHNICITY_nonhispanic'] = 0
		
		if gender == 'F':
			X['GENDER_F'] = [1]
		else:
			X['GENDER_F'] = [0]
		
		arr = rf.predict(X)

		if arr[0] == 0:
			return render_template('predict.html',msg = "Patient Required Assistance")
		else:
			return render_template('predict.html',msg = "Patient Not Required Assistance")
	
	return render_template('predict.html',msg = "Fill Patient Details")


@app.route('/appointment')
def appointment():
	return render_template('book-appointment.html')


@app.route('/camail', methods=['POST', 'GET'])
def camail():
	global email
	try:
		msg1=Message(
			subject='Confirmed Appointment',
			recipients=[email],
			body="Your appointment is confirmed"
		)
		mail.send(msg1)
		return render_template("index_doctors.html")
	except Exception:
		return render_template("index_doctors.html")

@app.route('/uqmail', methods=['POST', 'GET'])
def uqmail():
	global email
	reply="There is no need to worry, keep taking medication for next 3 Days"
	try:
		msg1=Message(
			subject='Reply to query',
			recipients=[email],
			body="SSN Number: 78998789\nName: Abhimat Gupta\nEmail: abhimatg0004@gmail.com\nProblem Description: Fever doesn't respond well to medication\n\nReply: {} \n\n Thanks \n\n Get Well Soon".format(reply)
		)
		mail.send(msg1)
		return render_template("index_doctors.html")
	except Exception:
		return render_template("index_doctors.html")


@app.route('/remail', methods=['POST', 'GET'])
def remail():
	global email
	try:
		msg1=Message(
			subject='Reminder Set',
			recipients=[email],
			body="You will recieve medication reminder 10 minutes before its scheduled time"
		)
		mail.send(msg1)
		return render_template("index.html",text="Reminders Set")
	except Exception:
		return render_template("index.html",text="Something went wrong. Please try it later")


@app.route('/ordermail', methods=['POST', 'GET'])
def ordermail():
	global email
	try:
		msg1=Message(
			subject='Medicines Ordered',
			recipients=[email],
			body="Medicines ordered successfully.\nYou will receive order within 5 days."
		)
		mail.send(msg1)
		return render_template("index.html",text="Ordered Medicines")
	except Exception:
		return render_template("index.html",text="Something went wrong. Please try it later")


@app.route('/contactmail', methods=['POST', 'GET'])
def contactmail():
	fname=request.form.get("contact_fname")
	lname=request.form.get("contact_lname")
	emailid=request.form.get("contact_femail")
	problem=request.form.get("contact_fmsg")
	
	try:
		msg1=Message(
			subject='Problem Received',
			recipients=[emailid],
			body="{} {}, \n\n We successfully receieved your problem.\n\nThe problem specified below\n{}\n".format(fname,lname,problem)
		)
		mail.send(msg1)
		return render_template("index.html",text="Successfully Sent")
	except Exception:
		return render_template("index.html",text="Something went wrong. Please try it later")



@app.route('/MailMe', methods=['POST', 'GET'])
def MailMe():
	global email
	fname=request.form.get("app_fname")
	lname=request.form.get("app_lname")
	email=request.form.get("app_email")
	phone=request.form.get("app_phone")
	department=request.form.get("department_name")
	date=request.form.get("app_date")
	symptoms=request.form.get("app_texts")
	try:
		msg=Message(
			subject='Confirmation mail',
			recipients=[email],
			body="Recieved your request to setup up the appointment on 25/11/2021, doctor will confirm it soon"
		)
		mail.send(msg)

		msg1=Message(
			subject='Set Appointment Form',
			recipients=['nemesisunited01@gmail.com'],
			body="{} {} wanna set appointment 25/11/2021.\n\nHere are the details:\n\nEmail: {}\n\nPhone: {}\n\nDepartment:{}\n\nSymptoms:{}\n".format(fname,lname,email,phone,department,symptoms)
		)
		mail.send(msg1)
		return render_template("index.html",text="Your appointment is scheduled please add date and time to your calendars")
	
	except Exception:
		return render_template("index.html",text="Something went wrong. Please try it later")

if __name__=="__main__":
	app.run(debug=True)
