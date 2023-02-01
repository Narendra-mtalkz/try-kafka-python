from flask import *
from flask import Flask
from kafka import KafkaConsumer, KafkaProducer

app = Flask(__name__)
# Kafka Consumer
KAFKA_VERSION = (0, 10)
consumer = KafkaConsumer('my_topic',
                         bootstrap_servers=['kafka:9092'],
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: x.decode('utf-8'),api_version=KAFKA_VERSION)


print("mai bhi kam karunga")
for message in consumer:
    print("Consumed message: ", message.value)

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: x.encode('utf-8'),api_version=KAFKA_VERSION)
@app.route('/',method=['GET','POST'])
def home():
    try:
        if request.method == 'GET':
            print("working on home endpoint")
            producer.send('my_topic', value='Hello, World!')
            return jsonify({"status":True}), 200
        else:
            return {}
    except Exception as e:
        print(e)

producer.send('my_topic', value='Hello, World!')
# producer.flush()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)