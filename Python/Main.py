import Bakkerbase as bs


def main():
    fake_klanten_data = { 'klanten_count': 22, 'klanten_idle_time': 5.22 }
    bs.save_klanten(fake_klanten_data)
    return 0


if __name__ == "__main__":
    main()
