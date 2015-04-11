import graphics
import driver
import game
import twython
import time

TWITTER_APP_KEY = 'ntLFB6p6IApzcEECKF4NdHsdJ'
TWITTER_APP_KEY_SECRET = '9AkI8vTZwxPXFrBMzcENZUscp9TEAJyFdXwCVrN3fVFZLifalO' 
TWITTER_ACCESS_TOKEN = '808021956-h3pMy2nfM2afQE6aC8hDTl69bb0JDu2hutYUqdoY'
TWITTER_ACCESS_TOKEN_SECRET = 'RLozX4oMPu7rUpfehHGEv6WZXS8xgbV4RdjjfmgbIgboV'

t = twython.Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

class Twitter(game.Game):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
  def scroll(self, title, text):
    titlesprite = graphics.TextSprite(title, x=0, y=0, width=5, height=7)
    self.sprites.add(titlesprite)
    sprite = graphics.TextSprite(text, x=112, y=8, width=5, height=7)
    self.sprites.add(sprite)
    while (-1)*((sprite.width+1)*len(text)) < sprite.x:
      self.graphics.clear()
      for x in self.sprites:
        x.draw(self.graphics)
      time.sleep(0.02)
      sprite.x -= 1
      self.graphics.draw(self.serial)
    self.graphics.clear()
    self.sprites.remove(sprite)
    self.sprites.remove(titlesprite)

  def loop(self):
    search = t.search(q='#hackafe OR #bitcamp', count=10)
    tweets = search['statuses']
    twats = {x['id']:(x['user']['name'], ' '.join(x['text'].split("\n"))) for x in tweets}
    for i in twats.keys():
      self.scroll("@"+twats[i][0], twats[i][1])
    self.scroll("#Hackafe", "Tweet us to get your text here!")
    time.sleep(2)

GAME = Twitter
