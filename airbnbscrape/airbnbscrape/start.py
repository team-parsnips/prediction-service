from flask import Flask

# from spider import BnbspiderSpider

import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
  cmd = ['scrapy', 'crawl', 'airspider', '-a', 'city=irvine', '-a', 'country=usa', '-o', 'irvineairbnb.csv']

  return subprocess.check_output(cmd)
  # subprocess.check_output(["echo", "Hello World!"])
  # subprocess.CompletedProcess( args=['python', 'hello.py'], returncode=0 )
    # with open('seattleairbnb.csv') as items_file:
    #   return items_file.read()

if __name__ == '__main__':
  app.run()