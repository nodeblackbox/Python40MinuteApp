import requests
import os
from dotenv import load_dotenv
load_dotenv()



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QHBoxLayout, QScrollArea
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np




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
        'X-RapidAPI-Key': contextual_web_api_key,
        'X-RapidAPI-Host': 'contextualwebsearch-websearch-v1.p.rapidapi.com'
    }
    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()
    if 'value' in data:
        return data['value']
    else:
        return []


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


def get_weather(city: str, api_key: str):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': open_weather_map_api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if 'weather' in data and 'main' in data:
        return data
    else:
        return None


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


def get_crypto_price(crypto):
    # Here you can replace it with actual API call
    # For the purpose of this example, I'm using a mock price
    return 10000.0 if crypto == 'bitcoin' else 2000.0


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


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up stacked widget and views
        self.stacked_widget = QStackedWidget()
        self.newsView = NewsView()  # Initialize NewsView
        self.cryptoView = CryptoView()
        self.weatherApp = WeatherApp()

        self.stacked_widget.addWidget(self.newsView)  # Add NewsView to the stacked_widget
        self.stacked_widget.addWidget(self.cryptoView)
        self.stacked_widget.addWidget(self.weatherApp)

        layout.addWidget(self.stacked_widget)

        # Set up buttons
        button_layout = QHBoxLayout()

        self.newsButton = QPushButton("News")  # Button for the NewsView
        self.newsButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.newsView))
        button_layout.addWidget(self.newsButton)

        self.cryptoButton = QPushButton("Crypto View")  # Button for the CryptoView
        self.cryptoButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.cryptoView))
        button_layout.addWidget(self.cryptoButton)

        self.weatherButton = QPushButton("Weather")
        self.weatherButton.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.weatherApp))
        button_layout.addWidget(self.weatherButton)

        layout.addLayout(button_layout)


class CryptoView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set up buttons
        button_layout = QHBoxLayout()

        self.button1 = QPushButton("Bitcoin Price")
        self.button1.clicked.connect(lambda: self.update_graph('bitcoin'))
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Ethereum Price")
        self.button2.clicked.connect(lambda: self.update_graph('ethereum'))
        button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Random Crypto Price")
        self.button3.clicked.connect(lambda: self.update_graph('randomcrypto'))
        button_layout.addWidget(self.button3)

        layout.addLayout(button_layout)

        # Set up plot
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

    def update_graph(self, crypto):
        # Clear the previous plot
        self.plot_widget.clear()

        # Get the price and generate some random data for the plot
        price = get_crypto_price(crypto)
        data = np.random.normal(size=100) * price
        self.plot_widget.plot(data)


app = QApplication(sys.argv)

# Apply custom styling
app.setStyleSheet('''
    * {
        font-family: Arial, sans-serif;
    }
    
    QWidget {
        background-color: #fff;
        border-radius: 20px;
        padding: 20px;
    }
    
    QLabel#news_title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    QPushButton {
        background-color: #000;
        color: #fff;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #333;
    }
    
    QPushButton:pressed {
        background-color: #666;
    }
    
    QPushButton:focus {
        outline: none;
    }
    
    pg.PlotWidget {
        border: none;
    }
    
    QPushButton#newsButton, QPushButton#cryptoButton, QPushButton#weatherButton {
        background-color: transparent;
        color: #000;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 8px 12px;
        margin-right: 10px;
    }
    
    QPushButton#newsButton:hover, QPushButton#cryptoButton:hover, QPushButton#weatherButton:hover {
        text-decoration: underline;
    }
    
    QPushButton#newsButton:focus, QPushButton#cryptoButton:focus, QPushButton#weatherButton:focus {
        outline: none;
    }
    
    QPushButton#newsButton:pressed, QPushButton#cryptoButton:pressed, QPushButton#weatherButton:pressed {
        background-color: rgba(0, 0, 0, 0.1);
    }
''')

window = App()
window.show()

sys.exit(app.exec_())