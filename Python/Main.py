import pyrebase
import datetime
import Bakkerbase

#   Main loop here
def main():
    fake_products = [
        { 'product_name': 'Ananas Taart', 'available': False },
        { 'product_name': 'Something Else Taart', 'available': False },
        { 'product_name': 'Something Lekker', 'available': True },
        { 'product_name': 'Something Vies', 'available': False },
        { 'product_name': 'Fucking Taart', 'available': True },
        { 'product_name': 'Lekkere Taart', 'available': False },
        { 'product_name': 'Reza Taart', 'available': True },
        { 'product_name': 'Murtaza Taart', 'available': True }]
    Bakkerbase.save_vitrine(fake_products)
    return 0


if __name__ == '__main__':
    #   Load while true here for collecting sensor data
    #       - Do we need to run several python scripts for collecting from different sensors?
    #       - Should we build classes?
    main()
