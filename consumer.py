import json
import requests
import pika
import apikey

api_token = apikey.api_token

def query(requirement, in_model_name, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/smtnkc/{in_model_name}"
    payload = {"inputs": requirement}
    response = requests.post(API_URL, headers=headers, json=payload)
    return str(response.json())


with open('JSON/predict_results.json', 'r') as f:
    predict_results = json.load(f)


requirement_to_metric = {}
for prediction in predict_results['predictions']:
    requirement_to_metric[prediction['requirement']] = prediction[predict_results['target_metric']]

def messageCallBack(ch, method, properties, body):
    json_data = json.loads(body)
    in_model_name = str(json_data["in_model_name"])
    target_metric = str(json_data["target_metric"])
    #print(in_model_name)

    for item in json_data["data"]:
        requirement = item["requirement"]
        #print(requirement)

        try:
            result = query(requirement, in_model_name, api_token)
            target_value = requirement_to_metric.get(requirement, "Not found")
            print(f"Requirement: {requirement}, Result: {result}, {target_metric}: {target_value}")
        except Exception as e:
            print(f"An error occurred while making inference: {e}")

connectionParameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connectionParameters)
channel = connection.channel()

channel.queue_declare(queue='deneme', arguments={'x-max-priority': 5})
channel.basic_consume(queue='deneme', auto_ack=True, on_message_callback=messageCallBack)
channel.start_consuming()
