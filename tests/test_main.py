from py_openweather_tray import main


def test_get_weather_data():
    assert (main.get_weather_data(
        'https://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b6907d289e10d714a6e88b30761fae22')
            ['main']['temp'] == 300.15)


def test_kelvin_to_celsius():
    assert (main.kelvin_to_celsius(1) == -272.15)
    assert (main.kelvin_to_celsius(273.15) == 0.0)


def test_kelvin_to_fahrenheit():
    assert (main.kelvin_to_fahrenheit(1) == -457.8714388489209)
    assert (main.kelvin_to_fahrenheit(273.15) == 31.606978417266077)


def test_convert_temperature_test():
    assert (main.convert_temperature(1, 'C') == -272.15)
    assert (main.convert_temperature(1, 'F') == -457.8714388489209)


def test_deg_to_cardinal():
    assert (main.deg_to_cardinal(0) == 'N')
    assert (main.deg_to_cardinal(25) == 'NNE')
    assert (main.deg_to_cardinal(50) == 'NE')
    assert (main.deg_to_cardinal(75) == 'ENE')
    assert (main.deg_to_cardinal(100) == 'E')
    assert (main.deg_to_cardinal(110) == 'ESE')
    assert (main.deg_to_cardinal(125) == 'SE')
    assert (main.deg_to_cardinal(150) == 'SSE')
    assert (main.deg_to_cardinal(175) == 'S')
    assert (main.deg_to_cardinal(200) == 'SSW')
    assert (main.deg_to_cardinal(225) == 'SW')
    assert (main.deg_to_cardinal(250) == 'WSW')
    assert (main.deg_to_cardinal(275) == 'W')
    assert (main.deg_to_cardinal(300) == 'WNW')
    assert (main.deg_to_cardinal(325) == 'NW')
    assert (main.deg_to_cardinal(335) == 'NNW')
    assert (main.deg_to_cardinal(350) == 'N')
    assert (main.deg_to_cardinal(360) == 'N')
    assert (main.deg_to_cardinal(365) == 'N')
    assert (main.deg_to_cardinal(385) == 'NNE')


def test_clouds_percentage_to_text():
    assert (main.clouds_percentage_to_text(5) == 'Clear sky')
    assert (main.clouds_percentage_to_text(86) == 'Overcast clouds')


def test_extract_hour_and_minute_from_epoch():
    assert (main.extract_hour_and_minute_from_epoch(1585283921) == '04:38 UTC')


def test_get_color():
    colors = {'0': '#9bbcff', '223': '#9bbcff', '228': '#9dbdff',
              '233': '#9dbeff', '238': '#9fbfff', '243': '#a1c0ff',
              '248': '#a5c2ff', '253': '#a8c5ff', '258': '#afc9ff',
              '263': '#b9d0ff', '268': '#cedcff', '273': '#fef9ff',
              '278': '#fff3ef', '283': '#ffece0', '288': '#ffe3ca',
              '293': '#ffd9b6', '298': '#ffcc99', '303': '#ffbe7e',
              '308': '#ffad5e', '313': '#ff932c', '318': '#ff7300',
              '323': '#ff3300'}
    assert (main.get_color(colors, -100) == '#9bbcff')
    assert (main.get_color(colors, 0) == '#9bbcff')
    assert (main.get_color(colors, 100) == '#9bbcff')
    assert (main.get_color(colors, 115) == '#9bbcff')
    assert (main.get_color(colors, 226) == '#9dbdff')
    assert (main.get_color(colors, 238) == '#9fbfff')
    assert (main.get_color(colors, 9999) == '#ff3300')


def test_find_closest():
    assert (main.find_closest([1, 2, 3, 10, 20, 50, 100], 5) == 3)
    assert (main.find_closest([1, 2, 3, 10, 20, 50, 100], -100) == 1)
    assert (main.find_closest([1, 2, 3, 10, 20, 50, 100], 9999) == 100)
