from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',)
def login():
	return render_template("login.html") 

@app.route('/analysis')
def analysis():
	return render_template('analysis.html')  

@app.route('/about')
def about():
	return render_template('about.html') 

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/doctors')
def doctors():
	return render_template('doctors.html')

@app.route('/appointment')
def appointment():
	return render_template('book-appointment.html')

if __name__=="__main__":
	app.run()
