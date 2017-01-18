from flask import Flask
from flask import request

import subprocess

app = Flask(__name__)

# Get request to python service needs to be structured '/scrape?city=<cityname>'
@app.route('/scrape')
def run_scraper():
  city = request.args.get('city')
  cmd = ['scrapy', 'crawl', 'airspider', '-a', 'city=' + city, '-a', 'country=usa', '-o', city + 'Airbnb.csv']

  return subprocess.check_output(cmd)

# If issues with prediction-server connecting in docker (exit 1 possibly)
# Verify docker ip with command 'docker inspect <container id>' container needs to be running so run express server
# Match host below with docker ip

# If running production, set spider to all pages

if __name__ == '__main__':
  app.run(host='172.20.0.2', port='5000')