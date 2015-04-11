import graphics
import requests
import driver
import game
import json
import time

SYMBOLS = ["TCS", "T", "CSCO", "BAH", "RHT", "MSFT", "IBM", "TWTR", "GS"]
URL = "http://finance.yahoo.com/webservice/v1/symbols/{}/quote?format=json"

class Stocks(game.Game):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.st = iter([])
    
  def scroll(self, title, text):
    titlesprite = graphics.TextSprite(title, x=112, y=0, width=5, height=7)
    self.sprites.add(titlesprite)
    sprite = graphics.TextSprite(text, x=112, y=8, width=5, height=7)
    self.sprites.add(sprite)
    while (-1)*((sprite.width+1)*len(text)) < sprite.x:
      yield
      sprite.x -= 1
      titlesprite.x -= 1
    self.sprites.remove(sprite)
    self.sprites.remove(titlesprite)

  def stockticker(self, results):
    stocks = []
    for res in results["list"]["resources"]:
      stocks.append((res["resource"]["fields"]["symbol"], round(float(res["resource"]["fields"]["price"]), 2)))

    stocks_top = stocks[::2]
    stocks_bottom = stocks[1::2]
    for symbol, price in stocks:
      a = '    '.join([' '.join((s, str(v))) for s, v in stocks_top])
      b = '    '.join([' '.join((s, str(v))) for s, v in stocks_bottom])
      if len(b) < len(a):
        a, b = b, a
        yield from self.scroll(a, b)    
    
  def loop(self):
    try:
      next(self.st)
    except StopIteration:
      results = json.loads(requests.get(URL.format(','.join(SYMBOLS))).text)
      self.st = self.stockticker(results)
      time.sleep(2)

    super().loop()

GAME = Stocks
