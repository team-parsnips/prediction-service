from flask import Flask
from flask import request
from predict import Predict
import json
import subprocess

app = Flask(__name__)


@app.route('/', methods=['POST'])
def scrape_predict():
  request_body = request.get_json()

  # initiate scrape request based on specified location
  def scrape():
    cmd = ['scrapy', 
            'crawl', 
            'airspider', 
            '-a', 
            'city=' + request_body['location'], 
            '-a', 
            'country=usa', 
            '-o', 
            'airbnb.csv']
    return subprocess.check_output(cmd)
    # return

  # pass rental characteristics to prediction analysis
  def predict(params):
    predictor = Predict()
    return predictor.predict_price(params)

  # invoke scrape operation followed by prediction, returns predicted price
  scrape()
  return predict(request_body)

if __name__ == '__main__':
  app.run(threaded = True, host='localhost', port='5000')