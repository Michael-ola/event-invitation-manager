from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import qrcode
import json
import pandas as pd
import pymongo
from .utils.dbClient import usersCollection
from .utils.dbClient import verificationCollection
from .utils.dbClient import passwordCollection
from .utils.generateId import generateId
from bson.objectid import ObjectId
import bcrypt

path = 'Event/statics/QRs'
# domain = 'http://localhost:8000'
domain = 'michaelCypher.pythonanywhere.com'


def admin(request):
    return render(request, 'admin.html')


def storePassword(request):
    if (request.method == 'POST'):
        password = request.POST['password']
        salt = bcrypt.gensalt(rounds=15)
        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
        passwordCollection.update_one(
            {}, {'$set': {'password': hashed_password}})
        return HttpResponseRedirect(redirect_to="/Event/")
    else:
        return HttpResponse(status=404)


def Authentication(request):
    if (request.method == 'POST'):
        password = request.POST['password']
        hashed_password = passwordCollection.find_one()
        password_verified = bcrypt.checkpw(
            password.encode('utf8'), hashed_password['password'])
        print(password, password_verified, hashed_password['password'])
        if (password_verified):
            resp = render(request, 'index.html')
            resp.set_cookie('state', True)
            return resp
        else:
            resp = HttpResponseRedirect(redirect_to="/Event/")
            resp.delete_cookie('csrftoken')
            resp.delete_cookie('state')
            return resp
    else:
        return HttpResponse(status=404)


def homepage(request):
    return render(request, 'authentication.html')


# first API call


def storeGuest(request):
    data = pd.read_csv('Event/statics/guest.csv')
    guest_list = json.loads(data.to_json(orient='records'))
    num_guests = len(guest_list)
    for i in range(num_guests):
        guest_name = guest_list[i]['Name']
        guestId = generateId(guest_name)
        guest_list[i]['ID'] = guestId
        guest_list[i]['scanned_state'] = False
    usersCollection.insert_many(guest_list)
    return HttpResponseRedirect(redirect_to='/Event/admin/')


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
        url = f'{domain}/Event/qrVerifier?find={guest_ID}'
        createQRCode(url, guest_name)
    return HttpResponseRedirect(redirect_to='/Event/admin/')

# Last API call


def qrVerifier(request):
    if (request.COOKIES.get('state') and request.COOKIES.get('csrftoken')):
        verificationState = verificationCollection.find_one()
        if (verificationState['state']):
            guestID = request.GET.get('find')
            guest = usersCollection.find_one({'ID': guestID})
            if (guest and not guest['scanned_state']):
                usersCollection.update_one(
                    {'ID': guestID}, {'$set': {'scanned_state': True}})
                return render(request, 'verified.html', {'name': guest['Name']})
            elif (guest and guest['scanned_state']):
                return render(request, 'alreadyScanned.html', {'name': guest['Name']})
            else:
                return render(request, 'unverified.html')
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponseRedirect(redirect_to='/Event/')


id = ObjectId('6665caa55678c56b4481c0ee')


def startVerification(request):
    verificationCollection.update_one({'_id': id}, {'$set': {'state': True}})
    return HttpResponse('verification started')


def stopVerification(request):
    verificationCollection.update_one({'_id': id}, {'$set': {'state': False}})
    return HttpResponse('verification stopped')
