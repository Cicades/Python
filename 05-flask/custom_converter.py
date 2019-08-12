from flask import Flask
from werkzeug.routing import BaseConverter

class ReConverter(BaseConverter):
		def __init__(self, url_map, *args):
				super().__init__(url_map)
				self.regex = args[0]

app = Flask(__name__)
app.url_map.converters['re'] = ReConverter
@app.route('/hello/<re(r"[\d\w]+@.*"):mail>')
def hello(mail):
		return 'your email is {}'.format(mail)
