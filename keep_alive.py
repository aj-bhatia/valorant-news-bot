from flask import Flask
from threading import Thread
#from reddit import scrape

app = Flask('')

@app.route('/')
def home():
    return "Web Server up!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# scrape()