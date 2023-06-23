import requests
import os
from dotenv import load_dotenv
load_dotenv()

import sys
import numpy
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QStackedWidget, QScrollArea, QHBoxLayout)
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QColor
import pyqtgraph as pg


from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

contextual_web_api_key = os.getenv("CONTEXTUAL_WEB_API_KEY")
open_weather_map_api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")



def get_news(api_key: str, query: str):
    base_url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    params = {
        'q': query,
        'pageNumber': '1',
        'pageSize': '5',
        'autoCorrect': 'true',
        'fromPublishedDate': 'null',
        'toPublishedDate': 'null'
    }
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'contextualwebsearch-websearch-v1.p.rapidapi.com'
    }
    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()
    if 'value' in data:
        return data['value']
    else:
        return []
    
def get_weather(city: str, api_key: str):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if 'weather' in data and 'main' in data:
        return data
    else:
        return None
    
def get_crypto_price(crypto):
    # Here you can replace it with actual API call
    # For the purpose of this example, I'm using a mock price
    return 10000.0 if crypto == 'bitcoin' else 2000.0

class NewsCard(QWidget):
    def __init__(self, article):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel(article['title'])
        self.title.setObjectName("news_title")
        self.title.setWordWrap(True)
        layout.addWidget(self.title)

        self.description = QLabel(article['description'])
        self.description.setWordWrap(True)
        layout.addWidget(self.description)

        self.link_button = QPushButton("Read More")
        self.link_button.setObjectName("read_more_button")
        self.link_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(article['url'])))
        layout.addWidget(self.link_button)


class NewsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # fetch news from three sources
        self.api_key = contextual_web_api_key  # replace with your actual ContextualWeb API key
        self.sources = ["bbc", "cnn", "the-wall-street-journal"]
        self.fetch_news()

    def fetch_news(self):
        for source in self.sources:
            articles = get_news(self.api_key, source)
            for article in articles[:5]:  # Limit to 5 articles per source
                card = NewsCard(article)
                self.scroll_layout.addWidget(card)





class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel("London Weather")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.date_label)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        self.weather_label = QLabel()
        self.weather_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_label)

        self.show_weather_button = QPushButton("Refresh Weather")
        self.show_weather_button.clicked.connect(self.show_weather)
        layout.addWidget(self.show_weather_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every second

        self.show_weather()

    def show_weather(self):
        api_key = open_weather_map_api_key  # Replace with your actual API key
        city = "London"  # Get city name from the text entry field
        weather = get_weather(city, api_key)
        if weather is not None:
            self.weather_label.setText(
                f"Weather in {city}: {weather['weather'][0]['description']}, Temperature: {weather['main']['temp']}°C")
        else:
            self.weather_label.setText(f"Weather data for {city} is not available.")
        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.time_label.setText(current_time.toString('hh:mm:ss'))
        self.date_label.setText(current_date.toString('dd.MM.yyyy'))





class View1(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title = QLabel("View 1")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)


class View2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title = QLabel("View 2")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)





class CryptoView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        button_layout = QHBoxLayout()

        self.button1 = QPushButton("Bitcoin Price")
        self.button1.setObjectName("crypto_button")
        self.button1.clicked.connect(lambda: self.update_graph('bitcoin'))
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Ethereum Price")
        self.button2.setObjectName("crypto_button")
        self.button2.clicked.connect(lambda: self.update_graph('ethereum'))
        button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Random Crypto Price")
        self.button3.setObjectName("crypto_button")
        self.button3.clicked.connect(lambda: self.update_graph('random'))
        button_layout.addWidget(self.button3)

        layout.addLayout(button_layout)

        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        self.x = list(range(100))  # 100 time points
        self.y = [numpy.sin(x/10) for x in self.x]  # initial values for y (price)

        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Price', color='black', size=30)
        self.graphWidget.setLabel('bottom', 'Time', color='black', size=30)
        self.graphWidget.addLegend(size=(50,30))

        self.pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=self.pen, name="Price Data")

    def update_graph(self, crypto_name):
        # here we would typically fetch new crypto price data
        # but for this example, we'll just generate new random data
        self.y = [numpy.sin(x/10 + numpy.random.rand()/2) for x in self.x]
        self.data_line.setData(self.x, self.y)

class App(QWidget):    
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget(self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create instances of our page views
        self.view1 = View1()
        self.view2 = View2()
        self.weather_view = WeatherApp()
        self.news_view = NewsView()
        self.crypto_view = CryptoView()

        # Add to stack
        self.stack.addWidget(self.view1)
        self.stack.addWidget(self.view2)
        self.stack.addWidget(self.weather_view)
        self.stack.addWidget(self.news_view)
        self.stack.addWidget(self.crypto_view)

        # Create the navigation buttons
        button_layout = QHBoxLayout()

        self.button1 = QPushButton("View 1")
        self.button1.setObjectName("navigation_button")
        self.button1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("View 2")
        self.button2.setObjectName("navigation_button")
        self.button2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button_layout.addWidget(self.button2)

        self.weather_button = QPushButton("Weather")
        self.weather_button.setObjectName("navigation_button")
        self.weather_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        button_layout.addWidget(self.weather_button)

        self.news_button = QPushButton("News")
        self.news_button.setObjectName("navigation_button")
        self.news_button.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        button_layout.addWidget(self.news_button)

        self.crypto_button = QPushButton("Crypto")
        self.crypto_button.setObjectName("navigation_button")
        self.crypto_button.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        button_layout.addWidget(self.crypto_button)

        layout.addLayout(button_layout)

        card_widget = QWidget()
        card_layout = QVBoxLayout(card_widget)
        card_layout.addWidget(self.stack)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_widget.setStyleSheet('''
            QWidget {
                border-radius: 10px;
                border: 1px solid #2c2f33;
            }
        ''')
        layout.addWidget(card_widget)

        self.stack.setCurrentWidget(self.news_view) # Add this line to make News page default

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())



app = QApplication(sys.argv)

# Modify the app.setStyleSheet section
app.setStyleSheet('''
    * {
        font-family: Arial, sans-serif;
    }
    
    QWidget {
        background-color: #36393f;
        border-radius: 10px;
        padding: 20px;
    }
    
    QLabel#news_title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #fff;
    }
    
    QPushButton {
        background-color: #7289da;
        color: #fff;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #677bc4;
    }
    
    QPushButton:pressed {
        background-color: #5767a8;
    }
    
    QPushButton:focus {
        outline: none;
    }
    
    pg.PlotWidget {
        border: none;
    }
    
    QPushButton#navigation_button {
        background-color: #2c2f33;
        color: #fff;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 8px 12px;
        margin-right: 10px;
    }
    
    QPushButton#navigation_button:hover {
        background-color: #23272a;
    }
    
    QPushButton#navigation_button:focus {
        outline: none;
    }
    
    QPushButton#navigation_button:pressed {
        background-color: #23272a;
    }
    
    QPushButton#navigation_button:checked {
        background-color: #7289da;
    }
    
    QScrollArea {
        border: none;
    }

    QScrollBar:vertical {
        border: none;
        background: #36393f;
        width: 15px;
        margin: 22px 0 22px 0;
    }

    QScrollBar::handle:vertical {
        background: #7289da;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
''')

window = App()
window.show()

sys.exit(app.exec_())
