data_path = os.path.join(os.path.dirname(__file__), 'data.ini')

    data = configparser.ConfigParser()
    data.read(data_path)

    print(data.get_section('ser'))