import Bakkerbase as bs


def main():
    klanten_count = 5
    klanten_idle_time = 2.32
    bs.save_klanten(klanten_count, klanten_idle_time)
    return 0


if __name__ == "__main__":
    main()
