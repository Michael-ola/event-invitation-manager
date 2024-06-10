import os
import hashlib


def generateId(guest_name):
    id = hashlib.sha256(os.urandom(
        1024) + f'{guest_name} akwa-ibom'.encode('utf-8')).hexdigest()
    return id
