# from kafka import KafkaConsumer, KafkaProducer
# import json
# print("working in producer")
# def producer_message(data):
#     try:
#         print("producer_message called ::::::::::::::")
#         KAFKA_VERSION = (0, 10)
#         producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
#                          value_serializer=lambda x: json.dumps(x).encode('utf-8'),api_version=KAFKA_VERSION)
#         producer.send('my_topic', value=data)
#     except Exception as e:
#             print("error in producer",e)

