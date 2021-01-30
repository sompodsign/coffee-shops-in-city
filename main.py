from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Mapts (URL)', validators=[DataRequired()])
    open_time = StringField('Opening Time e.g. 8AM')
    close_time = StringField('Closing Time e.g. 8PM')
    rating = SelectField('Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕"])
    wifi = SelectField('Wifi', choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "X"])
    power = SelectField('Power', choices=["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌"])


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=("GET", "POST"))
def add_cafe():
    form = CafeForm()
    if request.method == "GET":
        return render_template('add.html', form=form)
    else:
        if form.validate_on_submit():
            cafe_name = form.cafe.data
            cafe_location = form.location.data
            open_time = form.open_time.data
            close_time = form.close_time.data
            rating = form.rating.data
            wifi_availability = form.wifi.data
            power_availability = form.power.data
            new_row = [cafe_name, cafe_location, open_time, close_time,
                       rating, wifi_availability, power_availability]
            with open('cafe-data.csv', 'a', newline="", encoding="UTF-8") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(new_row)
            return redirect('cafes')
        else:
            return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
