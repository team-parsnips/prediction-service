from flask import Flask

import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
  print ('hello friend')
  cmd = ['scrapy', 'crawl', 'airspider', '-a', 'city=irvine', '-a', 'country=usa', '-o', 'irvineairbnb.csv']

  return subprocess.check_output(cmd)
  # return 'hello world'

if __name__ == '__main__':
  app.run(host='172.20.0.2', port='5000')