import pyrebase
import datetime
import Bakkerbase

#   Main loop here
def main():
    fake_temperature_data = [
            { 'temp_sensor_no': 1, 'temperatue': 5, 'humidity': 50 },
            { 'temp_sensor_no': 2, 'temperatue': 2, 'humidity': 45 },
            { 'temp_sensor_no': 3, 'temperatue': 1, 'humidity': 47 }
    ]
    Bakkerbase.save_temperature(fake_temperature_data)
    # fake_products = [
    #    { 'product_name': 'Ananas Taart', 'available': False },
    #    { 'product_name': 'Something Else Taart', 'available': False },
    #    { 'product_name': 'Something Lekker', 'available': True },
    #    { 'product_name': 'Something Vies', 'available': False },
    #    { 'product_name': 'Fucking Taart', 'available': True },
    #    { 'product_name': 'Lekkere Taart', 'available': False },
    #    { 'product_name': 'Reza Taart', 'available': True },
    #    { 'product_name': 'Murtaza Taart', 'available': True }]
    # Bakkerbase.save_vitrine(fake_products)
    # print(Bakkerbase.get_temperature())
    return 0


if __name__ == '__main__':
    #   Load while true here for collecting sensor data
    #       - Do we need to run several python scripts for collecting from different sensors?
    #       - Should we build classes?
    main()
