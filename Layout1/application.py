from flask import Flask, render_template, request
import pymongo
import boto3
from botocore.exceptions import NoCredentialsError
import io
import numpy as np
import os
from skimage.transform import resize
from PIL import Image
import random


application = Flask(__name__)

application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

## USE YOUR OWN MONGODB USER AND PASSWORD
myclient = pymongo.MongoClient('mongodb+srv://<USER>:<PASSWORD>@cluster0-kam8g.mongodb.net/test?retryWrites=true&w=majority')
mydb = myclient["IVA"]

## AWS CREDENTIALS HERE
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

messages = ["🍫 تم الإرسال ✅ شكرًا لمساعدتك، تفضل شوكولاتة", 
"💐 تم الإرسال ✅ شكرًا لمساعدتك، تفضل ورد",
"🍉 تم الإرسال ✅ شكرًا لمساعدتك، تفضل بطيخ",
"🍰 تم الإرسال ✅ شكرًا لمساعدتك، تفضل كعكة",
"🍨 تم الإرسال ✅ شكرًا لمساعدتك، تفضل آيس كريم",
"🍕 تم الإرسال ✅ شكرًا لمساعدتك، تفضل بيتزا",
"🍟 تم الإرسال ✅ شكرًا لمساعدتك، تفضل بطاطس",
"🌹 تم الإرسال ✅ شكرًا لمساعدتك، تفضل وردة",
"🌖 تم الإرسال ✅ شكرًا لمساعدتك، تفضل قمرًا",
"⭐ تم الإرسال ✅ شكرًا لمساعدتك، تفضل نجمة",
"🏆 تم الإرسال ✅ شكرًا لمساعدتك، تفضل كأسًا",
]

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        ## Get captions, questions, and answers from form:
        d = dict()
        d['captions'] = []
        d['questions'] = []
        d['answers'] = []

        for i in range(1, 7):
            name = 'caption'+str(i)
            ins = request.form.get(name)
            if ins != None and len(ins):
                d['captions'].append(request.form.get(name))
        
        for i in range(1, 7):
            name = 'question'+str(i)
            ins = request.form.get(name)
            if ins != None and len(ins):
                d['questions'].append(request.form.get(name))
        
        for i in range(1, 7):
            name = 'answer'+str(i)
            ins = request.form.get(name)
            if ins != None and len(ins):
                d['answers'].append(request.form.get(name))

        ## Get the next id name for the image and add the sample to the collection
        col = mydb['caption_and_vqa_samples']
    
        id = 1
        x = col.find_one()
        id = x['image_count']+1

        imageName = "IVA"
        for i in range(7-len(str(id))):
            imageName += '0'

        imageName += str(id)

        x = {}
        x['_id'] = id
        x['image'] = imageName
        x['data'] = d

        col.insert(x)
        myquery = { "_id": 0 }
        newvalues = { "$set": { "image_count": id } }

        col.update_one(myquery, newvalues)

        ## Get the uploaded image and upload it to S3

        if request.files:
            f = request.files['inpFile']
            img = Image.open(f.stream)
            imageName = imageName + '.jpg'

            # Scale down image
            scale_percent = 50 # percent of original size
            w, h = img.size
            width = int(w * scale_percent / 100)
            height = int(h * scale_percent / 100)
            if(width < 600 or height < 600):
                width = w
                height = h

            dim = (width, height)
            img = img.resize(dim)
            img = img.convert('RGB')
            img.save(imageName)

            upload_to_aws(imageName, 'iva-website-samples', imageName)
            os.remove(imageName)

        num = random.randint(0, 10)
        return render_template("IVA.html", message=messages[num])


    return render_template("IVA.html")
