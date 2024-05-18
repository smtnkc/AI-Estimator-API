import pika
import json


connectionParameters=pika.ConnectionParameters('localhost')

connection=pika.BlockingConnection(connectionParameters)

channel=connection.channel()

channel.queue_delete(queue='deneme')
channel.queue_declare(queue='deneme',arguments={'x-max-priority': 5})


with open("JSON/predict.json","r",) as file:
        predictJSON=json.load(file)


channel.basic_publish(exchange="",routing_key="deneme",body=json.dumps(predictJSON),properties=pika.BasicProperties(priority=2))


print(f"Messages send.")



connection.close()




