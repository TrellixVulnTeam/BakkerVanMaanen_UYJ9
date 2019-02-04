import Bakkerbase
from random import randint
def save():
    idle = 2.20
    a_klanten = 26
    coords_x = [randint(200, 400) for x in range(0, 9)]
    coords_y = [randint(200, 303) for x in range(0, 9)]
    Bakkerbase.save_klanten(idle, a_klanten, coords_x, coords_y)

save()
