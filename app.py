from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
import numpy as np
import pandas
import sklearn
import pickle
from flask import Flask, render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
app = Flask(__name__)

CORS(app, resources={r"/predict": {"origins": "http://localhost:5173"}})
model = pickle.load(open('model.pkl','rb'))
sc = pickle.load(open('standscaler.pkl','rb'))
ms = pickle.load(open('minmaxscaler.pkl','rb'))





@app.route("/",methods=['GET'])
def out():
    return jsonify(
        {
            "aa":"dfsdsf"
        }
    )



@app.route("/predict",methods=['POST'])
def predict():
    print(request.form)

    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['ph']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        
        return jsonify({"result" : "{} is the best crop to be cultivated right there".format(crop)})
    else:
        return jsonify({"result" : "Sorry, we could not determine the best crop to be cultivated with the provided data."})



app = Flask(__name__, template_folder='templates')
cors = CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///./database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SMS_API_KEY'] = 'thisisthesecretsmsapikey'
# sms=SMS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    phoneNum = db.Column(db.Integer,nullable=False,unique=True)
    # phone_verified = db.Column(db.Boolean, default=False)
    # OTP = db.Column(db.Integer,nullable=False)
    
    # def check_otp(self, otp):
    #     return self.otp == otp
    
    def __repr__(self):
        return f'User with name {self.name} with phone number {self.phoneNum}'
    
# class RegisterForm(FlaskForm):
#     name = StringField(validators=[InputRequired(),Length(min=3,max=20)], render_kw={"placeholder": "Full Name"})
#     phoneNum = IntegerField(validators=[InputRequired(), Length(min=10,max=12)], render_kw={"placeholder":"Phone Number"})
#     otp = IntegerField(validators=[InputRequired(), Length(max=6)], render_kw={"placeholder":"OTP"})
    
#     submit = SubmitField("Register")
    
#     def validate_name(self,name):
#         existing_name = User.query.filter_by(name=name.data).first()
#         if existing_name:
#             raise ValidationError("This name is already registered")
        
# class LoginForm(FlaskForm):
#     phoneNum = IntegerField(validators=[InputRequired(), Length(min=10,max=12)], render_kw={"placeholder":"Phone Number"})    
#     submit = SubmitField("Enter OTP")
    
# class OTPForm(FlaskForm):
#     otp = IntegerField(validators=[InputRequired(), Length(max=6)], render_kw={"placeholder":"OTP"})
#     submit = SubmitField("Verify OTP")


# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     return render_template('ArgicultureApp/Signin.html', form=form)

# @app.route('/verify_otp', methods=['GET', 'POST'])
# def verify_otp():
#     if request.method == 'POST':
#         phone_number = request.form.get('phone_number')
#         otp = request.form.get('otp')
#         user = User.query.filter_by(phone_number=phone_number).first()
#         if user and user.check_otp(otp):
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid OTP.', 'danger')
#             return redirect(url_for('send_otp'))
#     return render_template('verify_otp.html')

# @app.route('/send_otp', methods=['POST'])
# def send_otp():
#     form = OTPForm()
#     if form.validate_on_submit():
#         phone_number = form.phone_number.data
#         otp = generate_otp() # You need to implement this function to generate OTP
#         message = f'Your OTP is {otp}'
#         sms.send(message, phone_number)
#         flash('OTP has been sent to your phone number.', 'success')
#         return redirect(url_for('verify_otp'))
#     return render_template('otp.html', form=form)

@app.route('/register',methods=['POST'])
def register():
    print("\n\n\n",request.form)
    firstname = request.form.get('firstname') 
    lastname = request.form.get('lastname')
    phone_num = request.form.get('phoneNum')
    user = User(firstname=firstname, lastname=lastname, phoneNum=phone_num)
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict()})
            
# @app.route('/home.html',methods=['GET','POST'])
# def home():
#     if request.method == "GET":
#         user = User.query.all()
#         return render_template()
    
class LearningRoadmap:
    def __init__(self, crop, amount, location):
        self.crop = crop
        self.amount = amount
        self.location = location

    def get_planting_dates(self):
        
        planting_dates = {
            'wheat': 'October - December',
            'rice': 'June - July',
            'corn': 'April - May'
        }
        

    def get_tasks(self):
        pass
    
@app.route('/learning-roadmap', methods=['GET', 'POST'])
def learning_roadmap():
    if request.method == 'POST':
        crop = request.form.get('crop')
        amount = request.form.get('amount')
        location = request.form.get('location')

        learning_roadmap = LearningRoadmap(crop=crop, amount=amount, location=location)
        db.session.add(learning_roadmap)
        db.session.commit()

       # roadmap = generate_roadmap(crop, amount, location)

        return render_template('learning-roadmap.html', roadmap=roadmap)

    return render_template('learning-roadmap.html')

if __name__ == '__main__':
    app.run(debug=True)
