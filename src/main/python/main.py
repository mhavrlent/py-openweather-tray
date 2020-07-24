from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import requests
import json
from datetime import datetime
from bisect import bisect_left


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, config, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        menu = QtWidgets.QMenu(parent)
        menu.addAction('Exit')
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)
        self.config = config
        self._update_secs = config.get('update_secs')
        self._start_update_timer()

    def do_update(self):
        update_tray(self.config, self)
        self._start_update_timer()

    def _start_update_timer(self):
        try:
            self._updateTimer.stop()
        except:
            pass
        self._updateTimer = QtCore.QTimer()
        self._updateTimer.timeout.connect(self.do_update)
        self._updateTimer.start(self._update_secs * 1000)

    def exit(self):
        QtCore.QCoreApplication.exit()


def deg_to_cardinal(deg):
    if deg is not None:
        points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(deg / (360. / len(points)))
        return points[index % len(points)]
    else:
        return 'Data missing'


def clouds_percentage_to_text(perc):
    if (perc >= 0) and (perc <= 10):
        return 'Clear sky'
    if (perc >= 11) and (perc <= 24):
        return 'Few clouds'
    if (perc >= 25) and (perc <= 50):
        return 'Scattered clouds'
    if (perc >= 51) and (perc <= 84):
        return 'Broken clouds'
    if (perc >= 85) and (perc <= 100):
        return 'Overcast clouds'


def extract_hour_and_minute_from_epoch(epoch):
    return datetime.utcfromtimestamp(epoch).strftime('%H:%M UTC')


def create_tooltip_text(wind_speed, wind_deg, humidity, clouds, sunrise, sunset):
    str_list = []
    str_list.append('Wind speed: %s m/s\n' % wind_speed)
    str_list.append('Wind direction: %s (%s)\n' %
                    (wind_deg, deg_to_cardinal(wind_deg)))
    str_list.append('Humidity: %s %%\n' % humidity)
    str_list.append('Sky: %s\n' % clouds_percentage_to_text(clouds))
    str_list.append('Sunrise: %s\n' %
                    extract_hour_and_minute_from_epoch(sunrise))
    str_list.append('Sunset: %s' % extract_hour_and_minute_from_epoch(sunset))
    return ''.join(str_list)


def get_weather_data(url):
    response = requests.get(url)
    return response.json()


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin / 0.556) - 459.67


def convert_temperature(temp, scale):
    if scale == 'C':
        return kelvin_to_celsius(temp)
    if scale == 'F':
        return kelvin_to_fahrenheit(temp)


def get_color(colors, temp):
    colors_keys = list(map(int, [*colors.keys()]))
    colors_keys.sort()
    closest_key = find_closest(colors_keys, temp)
    closest_value = colors.get('%s' % closest_key)
    return closest_value


def find_closest(sl, v):
    """
    Assumes sl is a sorted list. Returns closest value to v.
    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(sl, v)
    if pos == 0:
        return sl[0]
    if pos == len(sl):
        return sl[-1]
    before = sl[pos - 1]
    after = sl[pos]
    if after - v < v - before:
        return after
    else:
        return before


def draw_tray_icon(tray, text, color, font, font_size, icon_size, tooltip_text):
    px = QtGui.QPixmap(icon_size, icon_size)
    px.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(px)
    pen_color = QtGui.QColor(color)
    pen = QtGui.QPen(pen_color)
    painter.setPen(pen)
    painter.setFont(QtGui.QFont(font, font_size))
    painter.drawText(px.rect(), QtCore.Qt.AlignCenter, text)
    painter.end()
    qicon = QtGui.QIcon()
    qicon.addPixmap(px)
    tray.setIcon(qicon)
    tray.setToolTip(tooltip_text)


def update_tray(config, tray):
    url = config.get(
        'url', 'https://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b6907d289e10d714a6e88b30761fae22')
    weather_data = get_weather_data(url)
    temp = weather_data['main']['temp']
    converted_temp = round(convert_temperature(temp, config.get('scale', 'C')))
    draw_tray_icon(tray,
                   str(converted_temp),
                   get_color(config.get('colors'), temp),
                   config.get('font', 'Arial'),
                   int(config.get('font_size', 8)),
                   int(config.get('icon_size', 16)),
                   create_tooltip_text(weather_data['wind']['speed'],
                                       weather_data['wind']['deg'],
                                       weather_data['main']['humidity'],
                                       weather_data['clouds']['all'],
                                       weather_data['sys']['sunrise'],
                                       weather_data['sys']['sunset']))


def main():
    appctxt = ApplicationContext()
    w = QtWidgets.QWidget()
    with open('config.json') as json_file:
        config = json.load(json_file)
    tray = SystemTrayIcon(config, w)
    update_tray(config, tray)
    tray.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
