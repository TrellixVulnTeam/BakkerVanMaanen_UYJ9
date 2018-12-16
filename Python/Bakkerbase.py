import pyrebase
import datetime

#   Our firebase config
config = {
    'apiKey': 'AIzaSyBDKtBSkTW31bnxjtMiow8v7PVp3XL32Ks',
    'authDomain': 'bakkerbase-9bd8b.firebaseapp.com',
    'databaseURL': 'https://bakkerbase-9bd8b.firebaseio.com',
    'projectId': 'bakkerbase-9bd8b',
    'storageBucket': 'bakkerbase-9bd8b.appspot.com',
    'messagingSenderId': '341606402913'
}


#   Intialize firebase using pyrebase module
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_klanten():
    return db.child('/klanten').get().val()

#   Get all light sensor data
def get_lights():
    return db.child('/lights').get().val()


#   Get all temperature / humidity data
def get_temperature():
    return db.child('/temperature').get().val()


#   Get all vitrine data
def get_vitrine():
    return db.child('/vitrine').get().val()


#   Save new entry
#       - Interval for sending data should be determined
#       - Temperature model may need work
#       - Timestamp works correctly and updates on front-end!
def save_temperature(sensors_data):
    data = {
            'temperature_sensors': sensors_data,
            'timestamp': datetime.datetime.now().__str__()
        }
    return db.child('/temperature').push(data)


#   Save light sensor entry
def save_lights(lights_dict):
    data = {
            'lights': lights_dict,
            'timestamp': datetime.datetime.now().__str__()
        }
    return db.child('/lights').push(data)


#   Save current vitrine state
def save_vitrine(products_dict):
    data = {
            'products': products_dict,
            'timestamp': datetime.datetime.now().__str__()
        }
    return db.child('/vitrine').push(data)

#   Save klanten data
def save_klanten(klanten_dict):
    data = {
            'klanten_data': klanten_dict,
            'timestamp': datetime.datetime.now().__str__()
        }
    return db.child('/klanten').push(data)
