# PyQT Dashboard

This project is a Python application that serves as a multi-purpose dashboard built with PyQt5. It fetches and displays real-time data from various sources. The app is designed to provide a convenient location where users can access news, weather, and cryptocurrency prices.

## 🌟 Features

- **News View:** Fetches news from various sources using the ContextualWeb API.
- **Weather View:** Fetches real-time weather data of a particular city using the OpenWeatherMap API.
- **Crypto View:** Displays a mock of real-time price data of a chosen cryptocurrency.

## 🚀 Getting Started

##  - Prerequisites

You need to have Python installed along with the following packages:
- PyQt5
- numpy
- pyqtgraph
- requests
- python-dotenv

You can install these packages using pip:
Save to grepper

```bash
pip install PyQt5 numpy pyqtgraph requests python-dotenv
```
### Setting up your .env file
This project requires two API keys:
- ContextualWeb API key for news fetching.
- OpenWeatherMap API key for weather fetching.

After obtaining these keys, create a .env file in your project directory and add your API keys as follows:

### note Replace the text with your API key
```python
CONTEXTUAL_WEB_API_KEY='your-contextual-web-api-key'
OPEN_WEATHER_MAP_API_KEY='your-open-weather-map-api-key'
```
Replace 'your-contextual-web-api-key' and 'your-open-weather-map-api-key' with your respective API keys.

### Running the Project
After setting up the prerequisites and .env file, run the project using the following command:

```bash
python your-python-file.py
```
Replace your-python-file.py with the name of the python file that contains the project code.

## 🛠 Expanding on the Project

- **Adding more Views:** You can create more views by extending the QWidget class, similar to how it's done in the current views. After creating a new view, add an instance of it to the self.stack QStackedWidget in the App class.
- **Adding more APIs:** Implement more API calls to fetch data from more sources. Create more methods similar to the current get_news and get_weather methods.
- **Enhancing UI/UX:** There's ample room for improvement in terms of UI/UX. Modify the app's stylesheet or implement new PyQt5 features to make the app more user-friendly.

## 📝 Known Limitations
- Cryptocurrency prices are mocked instead of being fetched from an actual API.
- The application might not display properly on different screen resolutions.

## 🤝 Contributing
Feel free to fork this project and make your own changes. If you come up with something interesting, you're welcome to open a pull request. Please make sure to update the tests as appropriate.

## 📜 License
MIT

```bash
Please copy the entire block and replace the placeholders (like 'your-python-file.py', 'your-contextual-web-api-key', etc.) with your specific project details.

```