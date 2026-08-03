"""
Twitter Deep Diagnosis Test
"""
from config import *
import tweepy, sys

print("=" * 55)
print("  Twitter Deep Diagnosis")
print("=" * 55)
print(f"\nAPI Key    : {TWITTER_API_KEY}")
print(f"API Secret : {TWITTER_API_SECRET[:15]}...")
print(f"Token      : {TWITTER_ACCESS_TOKEN}")
print(f"Secret     : {TWITTER_ACCESS_SECRET[:15]}...")

try:
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )
    response = client.create_tweet(text="🤖 Test")
    print(f"\n✅ SUCCESS! Tweet ID: {response.data['id']}")

except tweepy.TweepyException as e:
    print(f"\n❌ Tweepy Error Type : {type(e).__name__}")
    print(f"   Error Message    : {e}")
    # Print full exception details
    if hasattr(e, 'response') and e.response is not None:
        print(f"   HTTP Status      : {e.response.status_code}")
        print(f"   Response Text    : {e.response.text}")
    if hasattr(e, 'api_codes'):
        print(f"   API Error Codes  : {e.api_codes}")
    if hasattr(e, 'api_messages'):
        print(f"   API Messages     : {e.api_messages}")

except Exception as e:
    print(f"\n❌ General Error: {type(e).__name__}: {e}")

print()
