import json
import requests
import pika
import apikey
import subprocess

api_token = apikey.api_token


def query(requirement, in_model_name, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/smtnkc/{in_model_name}"
    payload = {"inputs": requirement}
    response = requests.post(API_URL, headers=headers, json=payload)
    response_data = response.json()
    # Assuming response is a dictionary and contains the key 'result'
    if isinstance(response_data, list) and len(response_data) > 0:
        return response_data[0]  # assuming the first element is the numeric result you need
    else:
        return response_data  # handle error or unexpected structure


def messageCallBack(ch, method, properties, body):
    json_data = json.loads(body)
    job_id = str(json_data["job_id"])
    job_priority = str(json_data["job_priority"])
    user_id = str(json_data["user_id"])
    project_name = str(json_data["project_name"])
    in_model_name = str(json_data["in_model_name"])
    target_metric = str(json_data["target_metric"])

    results = []

    for item in json_data["data"]:
        requirement = item["requirement"]
        try:
            result = query(requirement, in_model_name, api_token)
            results.append({
                "requirement": requirement,
                target_metric: result
            })
        except Exception as e:
            print(f"An error occurred while making inference: {e}")

    json_data["predictions"] = results

    # Save data to a temporary JSON file
    with open('temp_results.json', 'w') as f:
        json.dump(json_data, f)

    # Call the script.py to process and create the final JSON
    subprocess.run([
        "python", "script.py",
        "--job_id", job_id,
        "--job_priority", job_priority,
        "--user_id", user_id,
        "--project_name", project_name,
        "--in_model_name", in_model_name,
        "--target_metric", target_metric
    ])

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


connectionParameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connectionParameters)
channel = connection.channel()

channel.queue_declare(queue='deneme', arguments={'x-max-priority': 5})
channel.basic_consume(queue='deneme', on_message_callback=messageCallBack, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


