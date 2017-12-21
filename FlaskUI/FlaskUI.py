from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_script import Manager
from wtforms import SubmitField, StringField

app = Flask(__name__)
app.config["SECRET_KEY"] = "The beacon."

bootstrap = Bootstrap(app)
manage = Manager(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manage.run()
