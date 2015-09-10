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
    self.nl = self.tweets()

    self.next_slide = 0

    self.head = graphics.TextSprite('#MAGSign', x=0, y=0, width=5, height=7)
    self.sprites.add(self.head)
    self.body = graphics.TextSprite('allan please add text', x=112, y=8, width=5, height=7)
    self.sprites.add(self.body)

  def update_body(self, text):
    self.sprites.clear()

    self.sprites.add(self.head)
    self.body.set_text(text)
    self.body.x = 112
    self.sprites.add(self.body)
    self.sprites.add(graphics.Animator(self.body, attr="x", max=(5 if self.body.size() > 102 else 107),
                                       min=(107 - self.body.size() if self.body.size() > 102 else 5), reverse=True,
                                       delay=.06, step=-2))

  def tweets(self):
    tweets = {}
    while True:
      yield "Tweet #MAGsign", "Make this sign say stuff!", 20

      try:
        tweet_res = t.search(q='#magsign OR #magclassic', count=10)
        #tweet_res = t.search(q='#magsign', count=10)
        tweets = tweet_res['statuses']
      except twython.exceptions.TwythonError:
        pass

      twats = {x['id']:(x['user']['screen_name'], ' '.join(x['text'].split("\n"))) for x in tweets}
      for twat in twats.values():
        yield '@' + twat[0], twat[1], 15

  def loop(self):
    super().loop()

    if time.time() >= self.next_slide:
      name, text, delay = next(self.nl)

      self.head.set_text(name)
      self.update_body(text)
      self.next_slide = time.time() + delay

GAME = Twitter
