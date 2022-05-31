from flask import render_template, current_app as app, jsonify
import numpy
#from app.data import rf_model_pkl
from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, IntegerField, SubmitField
from wtforms.validators import InputRequired
from wtforms.widgets import html5
import pickle



class FieldsRequiredForm(FlaskForm):
    """Require all fields to have content. This works around the bug that WTForms radio
    fields don't honor the `DataRequired` or `InputRequired` validators.
    """
    class Meta:
        def render_field(self, field, render_kw):
            if field.type == "_Option":
                render_kw.setdefault("required", True)
            return super().render_field(field, render_kw)
        
        

class DiagnoseForm(FieldsRequiredForm):
    age = IntegerField('Age',
                       widget=html5.NumberInput(min=1, max=140),
                       validators=[InputRequired()])
    gender = RadioField('Label',
                        choices=[(True, 'Male'),
                                 (False, 'Female')],
                        validators=[InputRequired()])
    polyuria = BooleanField('Polyuria')
    polydipsia = BooleanField('Polydipsia')
    sudden_weight_loss = BooleanField('Sudden Weight Loss')
    weak_ness = BooleanField('weak ness')
    polyphagia = BooleanField('Polyphagia')
    genital_thrush = BooleanField('genital thrush')
    visual_blurring = BooleanField('visual blurring')
    itching = BooleanField('Itching')
    irritability = BooleanField('Irritability')
    delayed_heading = BooleanField('delayed heading')
    partial_paresis = BooleanField('partial paresis')
    muscle_stiffness = BooleanField('muscle stiffness')
    alopecia = BooleanField('Alopecia')
    obesity = BooleanField('Obesity')
    submit = SubmitField('Get result')        

@app.route("/", methods=['GET'])
def home():
    return render_template("home.html", title='Home')


@app.route("/diagnose", methods=['GET'])
def diagnose():
    form = DiagnoseForm()
    return render_template("diagnose.html",
                           form=form,
                           title='Diagnose')


@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    form = DiagnoseForm()
    if form.validate_on_submit():
        form_dict = form.data
        form_dict.pop('csrf_token')
        form_dict.pop('submit')
        form_dict['gender'] = (form_dict['gender'] == 'True')  
        print(str(form_dict))
        features = list(form_dict.values())  
        print(features)
        rf_model = pickle.load(open('app/data/rf_model_pkl', 'rb'))
        print(rf_model.predict([features]))
        prediction = 'Positive' if rf_model.predict([features]) else 'Negative'
        accuracy = "{:.2f}".format(round((numpy.max(rf_model.predict_proba([features])) / 1), 2))
        results = {'prediction': prediction,
                  'accuracy': accuracy}#       
        return results




