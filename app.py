from flask import Flask, render_template
from kafka import KafkaConsumer


app = Flask(__name__)
consumer = KafkaConsumer('quickstart-events')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get")
def get():
    return "Bye"
