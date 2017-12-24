from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_script import Manager
from wtforms import SubmitField, StringField, TextField, RadioField, FileField, TextAreaField
from wtforms.validators import Required, Optional, DataRequired
import sys
sys.path.append("../")
from Segmentation import init, cut_into_sentense, segment_for_sentense, segment_for_text

app = Flask(__name__)
app.config["SECRET_KEY"] = "The beacon."

bootstrap = Bootstrap(app)
manage = Manager(app)


class TextForm(FlaskForm):
    raw_text = TextAreaField("Please input the raw text here.", validators=[Required(), ])
    mode = RadioField("Please select the mode.",
                      choices=(("0", "Cut into sentenses first"), ("1", "Segment directly")),
                      validators=[DataRequired()]
                      )
    submit = SubmitField("Submit")


class FileForm(FlaskForm):
    file = FileField("Please upload your file.", validators=[Required()])
    mode = RadioField("Please select the mode.",
                      choices=(("0", "Cut into sentenses first"), ("1", "Segment directly")),
                      validators=[DataRequired()]
                      )
    submit = SubmitField("Submit")


class ResultForm(FlaskForm):
    result_text = TextAreaField()


class SentenseForm(FlaskForm):
    pass


@app.route("/sentense", methods=["GET", "POST"])
def sentense():
    global raw_text
    # print(raw_text)
    sentenses = cut_into_sentense(raw_text)
    # print(sentenses)
    num = len(sentenses)
    if num > 50:
        flash("Too many sentenses to display. Only display the first 50 sentenses.")
        num = 50
    result_sentenses = [segment_for_sentense(sentenses[i]) for i in range(num)]
    return render_template("sentense.html", sentenses=sentenses[0:num], result_sentenses=result_sentenses, num=num)


@app.route("/", methods=["GET", "POST"])
def index():
    by_file = request.args.get('by_file', False, type=bool)
    print("FUCK!!!")
    input_form = FileForm() if by_file else TextForm()
    result_form = ResultForm()
    if input_form.validate_on_submit():
        mode = input_form.mode.data
        print(mode, type(mode))
        global raw_text
        raw_text = ""
        if isinstance(input_form, TextForm):
            raw_text = input_form.raw_text.data
        else:
            raw_text = input_form.file.data.read().decode("utf-8")
        #print("raw_text", raw_text)
        if mode == "0":
            return redirect(url_for("sentense"))
        result_form.result_text.data = segment_for_text(raw_text, mode="sentense")
    else:
        try:
            if input_form.raw_text.data:
                flash("Please select whether to cut into sentenses first!")
        except:
            pass
        try:
            if input_form.file.data:
                flash("Please select whether to cut into sentenses first!")
        except:
            pass
    return render_template("index.html", by_file=by_file, input_form=input_form, result_form=result_form)


@app.route("/seg", methods=["GET", "POST"])
def segment():
    pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init(folder="../Result/sentense/Sentense_TrainingResult/")
    manage.run()
