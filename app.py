from flask import Flask, render_template, request
from kafka import KafkaConsumer
from turbo_flask import Turbo
import logging
import threading
import time


app = Flask(__name__)
turbo = Turbo(app)
list = []

SERVER = 'rover-cluster-kafka-bootstrap:9092'
# SERVER = 'localhost:9092'

# TOPIC = 'quickstart-events'
TOPIC = 'rover-metrics'

consumer = KafkaConsumer(bootstrap_servers=SERVER,
                        auto_offset_reset='earliest',   
                        )
                        
consumer.subscribe([TOPIC])


@app.route("/")
def index():
    return render_template('index.html')


@app.context_processor
def inject_load():
    try:
        list.append(next(consumer).value.decode("utf-8"))
    except:
        pass
    print(list)
    return {'msg': list }

def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('index.html'), 'load'))


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


if __name__ == '__main__':
    logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
            '%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO)

    app.run()



