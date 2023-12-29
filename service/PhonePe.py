import os
import sys
import requests
import hashlib
import json
import base64
import uuid
sys.path.append('../models')
from dotenv import load_dotenv
load_dotenv()
class PhonePe:
    def __init__(self):
        self.conn = None
        #self.url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
        self.url = "https://api.phonepe.com/apis/hermes/pg/v1/pay"
        #self.checkStatusUrl = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status"
        self.checkStatusUrl = "https://api.phonepe.com/apis/hermes/pg/v1/status"
        
    
    def payRequest(self, request):
        transactionId = uuid.uuid4().hex
        requestBody = {"merchantId":os.getenv("QA_MERCHANT_ID") ,"merchantTransactionId":transactionId,"merchantUserId":request['user_id'], "amount": request['amount'],"callbackUrl": "https://webhook.site/callback-url","mobileNumber": "9999999999","deviceContext": {"deviceOS": "ANDROID"},"paymentInstrument": {"type":"PAY_PAGE"}}
        byteRequestBody = json.dumps(requestBody).encode('utf-8')
        base64RequestBody = base64.b64encode(byteRequestBody)
        
        xVerify = str(base64RequestBody , encoding='utf-8') + "/pg/v1/pay"  +os.getenv("QA_SALT_KEY") 
        xVerify = str(hashlib.sha256(xVerify.encode()).hexdigest()) + "###" + "1"
        headers = {"Content-Type":"application/json" , "accept":"application/json" , "X-VERIFY":xVerify}
        encodedRequest = {"request":str(base64RequestBody , encoding='utf-8')}
        print(headers , encodedRequest)
        response = None
        try:
            response = requests.post(self.url ,headers=headers ,json=encodedRequest)
            # Insert into database with state as initiated transaction
            print(response.json())
        except Exception as e:
            return e
        return response.json()

    def checkPayStatus(self , transactionId):
        byteSHA = "/pg/v1/status/" + os.getenv("QA_MERCHANT_ID") + "/" + transactionId + os.getenv("QA_SALT_KEY")
        xVerify  =str(hashlib.sha256(byteSHA.encode()).hexdigest())+"###" + "1"
        headers = {"Content-Type":"application/json" , "accept":"application/json" , "X-VERIFY":xVerify , "X-MERCHANT-ID":os.getenv("QA_MERCHANT_ID")}
        print(headers)
        print(self.checkStatusUrl+"/" + os.getenv("QA_MERCHANT_ID") + "/" + transactionId)

        response = None
        try:
            response = requests.get(self.checkStatusUrl+"/" + os.getenv("QA_MERCHANT_ID") + "/" + transactionId , headers= headers)
            print(response)
        
        except Exception as e:
            return response.json()

        return response.json()


