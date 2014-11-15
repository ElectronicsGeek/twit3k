# twit3k - Displays timeline tweets live on a pimoroni dot3k display
# Gregory "ElectronicsGeek" Parker - 2014

import tweepy
from tweepy.error import TweepError
import time
from dot3k import lcd, backlight

### TWITTER AUTH:

# Replace these with your own keys. You can get these from:
# https://dev.twitter.com//
API_KEY = ""
API_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

def display_tweet(lcd, tweet, scroll_speed):
    """Displays a tweet as a scrolling marquee with its author's name
       written underneath."""
    
    # Remove '\n' characters because dot3k displays them wierdly!   
    s = tweet.text.replace("\n", " ")
    
    # Append 16 spaces to the tweet for scrolling. This stops the
    # author's handle from spilling into the tweet.
    s += " " * 16
    lcd.clear()

    for i in range(0, len(s)-16):
        lcd.write(s[i : i + 16]) # 16 = Width of Dot3k display in chars.

        # Add the author's handle below the tweet
        lcd.write("@" + tweet.author.screen_name)

        time.sleep(scroll_speed)
        lcd.clear()

### Twitter Authentication:
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

### LCD Setup:

# Displays a nice shade of blue to show the fact we're dealing with
# twitter!
backlight.rgb(86,188,216)

while True:
    try:
        lcd.write("Please Wait" + " " * 5 + "Fetching Tweets")
        most_recent_tweet = api.home_timeline()[0]
        display_tweet(lcd, most_recent_tweet, 0.3)
        
    except TweepError as error:
        lcd.clear()
        lcd.write("Twitter API     limit reached")
        print "Rate Limit Exceeded", error
        time.sleep(600) # Wait for ten minutes, then try again.
