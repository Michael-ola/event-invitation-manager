from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
import qrcode
import json
import pandas as pd
import pymongo
from .utils.dbClient import usersCollection
from .utils.dbClient import verificationCollection
from .utils.generateId import generateId
from bson.objectid import ObjectId

path = 'Event/statics/QRs'


def homepage(requests):
    return render(requests, 'index.html')


# first API call


def storeGuest(request):
    data = pd.read_csv('Event/statics/guest.csv')
    guest_list = json.loads(data.to_json(orient='records'))
    num_guests = len(guest_list)
    for i in range(num_guests):
        guest_name = guest_list[i]['Name']
        guestId = generateId(guest_name)
        guest_list[i]['ID'] = guestId
    usersCollection.insert_many(guest_list)
    return HttpResponse('stored')


def createQRCode(url, name):
    image = qrcode.make(url)
    name = f'{name}.jpg'
    image.save(path+'/'+name)

# Second API call


def qrGenerator(request):
    guest_list = usersCollection.find()
    for guest in guest_list:
        # print(guest['ID'])
        guest_name = guest['Name']
        guest_ID = guest['ID']
        url = f'http://localhost:8000/Event/qrVerifier?find={guest_ID}'
        createQRCode(url, guest_name)
    return HttpResponse('created')

# Last API call


def qrVerifier(request):
    verificationState = verificationCollection.find_one()
    if (verificationState['state']):
        guestID = request.GET.get('find')
        guest = usersCollection.find_one({'ID': guestID})
        if (guest):
            return render(request, 'verified.html', {'name': guest['Name']})
        else:
            return render(request, 'unverified.html')
    else:
        return HttpResponse(status=404)


id = ObjectId('6665caa55678c56b4481c0ee')


def startVerification(request):
    verificationCollection.update_one({'_id': id}, {'$set': {'state': True}})
    return HttpResponse('verification started')


def stopVerification(request):
    verificationCollection.update_one({'_id': id}, {'$set': {'state': False}})
    return HttpResponse('verification stopped')
