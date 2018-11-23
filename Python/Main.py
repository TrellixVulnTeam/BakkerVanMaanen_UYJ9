import pyrebase

config = {
    "apiKey": "AIzaSyBDKtBSkTW31bnxjtMiow8v7PVp3XL32Ks",
    "authDomain": "bakkerbase-9bd8b.firebaseapp.com",
    "databaseURL": "https://bakkerbase-9bd8b.firebaseio.com",
    "projectId": "bakkerbase-9bd8b",
    "storageBucket": "bakkerbase-9bd8b.appspot.com",
    "messagingSenderId": "341606402913"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_temp():
    return db.child("/temp").get().val()


def get_vitrine():
    return db.child("/vitrine/products_states").get().val()

print(get_vitrine())