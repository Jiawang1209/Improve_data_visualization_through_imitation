import dash

from config import AppConfig

app = dash.Dash(__name__,
                title=AppConfig.app_title,
                suppress_callback_exceptions=True)