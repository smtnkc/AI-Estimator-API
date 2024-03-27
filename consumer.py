import json

import pika
import subprocess   #farklı bir py uzantılı dosyayı çağırmak için kullanabilirim


def messageCallBack(ch,method,properties,body):
    #print(f"received new message: {body}")
    #print(f"Received new message with priority {properties.priority}: {body}")
    json_data=json.loads(body)
    user_id=str(json_data["user"]["user_id"])
    project_name=str(json_data["user"]["project_name"])
    in_model=str(json_data["user"]["in_model"])
    in_column=str(json_data["user"]["in_column"])
    out_column=str(json_data["user"]["out_column"])
    out_model=str(json_data["user"]["out_model"])

    #parse JSON  USER'IN İÇİNDEKİLER SCRİPT.PY ARGÜMANLARI SCRİPT PYNİN YANINA ARGÜMAN --
    subprocess.run(["python","script.py","--user_id",user_id,"--project_name",project_name
                    ,"--in_model",in_model,"--in_column",in_column,"--out_column",out_column
                    ,"--out_model",out_model])





#conenction parametreleri producer'ın aynısı

connectionParameters=pika.ConnectionParameters('localhost')
connection=pika.BlockingConnection(connectionParameters)
channel=connection.channel()


channel.queue_declare(queue='deneme',arguments={'x-max-priority': 5})
#ilk başta producerda oluşturduğumuz için rabbitmq kendisi otomatik
#olarak queuyu tanıyacak ikinci bir queue oluşturmayacak aslında burada ayrıca queue oluşturmama gerek yok
#basic consume methodunda zaten o queue name belirledim.

channel.basic_consume(queue='deneme',auto_ack=True,on_message_callback=messageCallBack)

#rabbitmq'nun queue ya bağlanıp mesajı alması
#priority bak consume durumunda.

#print("Starting consuming")



channel.start_consuming()
