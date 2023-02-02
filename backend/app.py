from json import dumps
from flask import Flask
from flask import *
from kafka import KafkaProducer
app = Flask(__name__)

KAFKA_VERSION = (0, 10)
topic_name='my_topic'
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),api_version=KAFKA_VERSION)


@app.route('/',methods=['POST','GET'])
def home():
    try:
        if request.method == 'GET':
            print("working in home endpoint.....")
            return "hello get"
        else:
            return "hello post"
    except Exception as e:
        print(e)

@app.route('/producer', methods=['GET', 'POST'])
def index():
    try:
        if request.method == "POST":
            payload = request.get_json(silent=True)
            data = payload
            # print(data)
            producer.send(topic_name, value=data)
            print("data send succesfully")
            return jsonify({"status": True, "message":"data sent succesfully"})
        else:
            return jsonify({}), 200
    except Exception as e:
        print(e)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)