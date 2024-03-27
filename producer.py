import pika
import json #json objesi göndermek için


connectionParameters=pika.ConnectionParameters('localhost')
#Pika kütüphanesini kullanarak localde çalışan rabbitmq sunucusuna bağlandım
#burası direkt bağlantı sağlamıyor sadece sunucu konumu vb olarak düşünebilirim


connection=pika.BlockingConnection(connectionParameters)
#Burada bağlantıyı direkt olarak kurdum.
#BlockingConnection bağlantı kurulana kadar bir sonraki adıma geçmez
#Burada  bağlantı başarılı olursa connection değişkenine otomatik olarak
#bir bağlantı nesnesi atanır ve bu nesneyi kullanarak mesaj alma ve verme gerçekleşir

channel=connection.channel()
#şimdi bir kanal oluşturdum.Kanallar sayesinde mesaj iletimi gerçekleşir
#Bir bağlantı üzerinde birden fazla kanal oluşturulabilir ve
#her kanal ayrı bir iletişim yolu sağlar
#Kanallar mesajlar arasında bağımsızlık sağlar ve
#aynı bağlantı üzerinde farklı işlemlerin paralel olarak gerçekleştirilmesine olanak tanır
channel.queue_delete(queue='deneme')
channel.queue_declare(queue='deneme',arguments={'x-max-priority': 5})
#burada artık bir tane queue oluşturdum

with open("veri.json","r",) as file:
        json_data=json.load(file) #json dosyasını okudum

with open("veri2.json","r") as file2:
        json_data2=json.load(file2)



channel.basic_publish(exchange="",routing_key="deneme",body=json.dumps(json_data),properties=pika.BasicProperties(priority=2))
channel.basic_publish(exchange="",routing_key="deneme",body=json.dumps(json_data2),properties=pika.BasicProperties(priority=4))



#mesajı queueya pushlamak için.
# exchange parametresi, mesajın iletilme mekanizmasını belirler
#ve mesajın nasıl işleneceğini kontrol ede
#burada defaul exchange kullandım o yüzden exchange kısmı boş
print(f"Messages send.")


connection.close()




