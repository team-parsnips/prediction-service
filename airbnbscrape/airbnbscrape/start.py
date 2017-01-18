from flask import Flask
from flask import request

# from spider import BnbspiderSpider

import subprocess

app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
  # cmd = ['scrapy', 'crawl', 'airspider', '-a', 'city=irvine', '-a', 'country=usa', '-o', 'irvineairbnb.csv']

  # return subprocess.check_output(cmd)
  print request.get_data()
  return 'hello'

if __name__ == '__main__':
  app.run()