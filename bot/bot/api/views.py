from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from .config import PAGE_ACCESS_TOKEN
import json

#Function to access the Sender API
def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN #= config.PAGE_ACCESS_TOKEN

    payload = {
    'recipient': {'id': senderPsid},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)



#Function for handling a message from MESSENGER
def handleMessage(senderPsid, receivedMessage):
    #check if received message contains text
    print('We entered the HANDLE MESSAGE FUNCTION')
    if 'text' in receivedMessage:
        print('TEXT does exist in the RECEIVER MESSAGE')

        toSend = receivedMessage['text']

   

        chatbotResponse = "response"
        print('The Chatbot Response is: {}'.format(chatbotResponse))

        response = {"text": chatbotResponse }


        callSendAPI(senderPsid, response)
    else:
        response = {"text": 'This chatbot only accepts text messages'}
        callSendAPI(senderPsid, response)


# Create your views here.
def index(request):
    if request.method == 'GET':
        #do something.....
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"
        print(dir(request))
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if True:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                
                return JsonResponse(challenge,safe=False)
            else:
                return  JsonResponse('ERROR',safe=False)

        return JsonResponse('SOMETHING')


    if request.method == 'POST':
        #do something.....
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"

        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if True:

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')


                return JsonResponse(challenge,safe=False)
            else:
                return JsonResponse('ERROR',safe=False)



        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))


        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404

