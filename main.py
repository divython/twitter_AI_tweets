import tweepy
import google.generativeai as genai
 # Used to securely store your API key 
from psycopg2 import connect
import re

GOOGLE_API_KEY=''
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Set up environment variables
api_key = ""
api_secret = ""
access_token = ""
access_token_secret = ""
bearer_token=r""

client= tweepy.Client(bearer_token,api_key,api_secret,access_token,access_token_secret)

# Initialize Tweepy
auth= tweepy.OAuth1UserHandler(api_key,api_secret,access_token,access_token_secret)
api=tweepy.API(auth)

db_host ='localhost'
db_name =''
db_user =''
db_password =''
conn = connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()


def is_valid_tweet(text):
    # Basic filtering criteria (adjust as needed)
    if re.match(r"^https?://", text):  # Exclude links
        return False
    if len(text) > 280:  # Enforce character limit
        return False
    return True

# Generate and filter text until a valid tweet is found
while True:
    response = model.generate_content(["write few amazing tweets on given topics,tech,techtwitter.AI,Machine learning,layoffs"])
    generated_texts = response.text.splitlines()  # Split into lines

    for text in generated_texts:
        # Remove leading digits, dots, and spaces (enhanced filtering)
        text = re.sub(r"^\d+\.", "", text)

        # Check if the filtered text is a valid tweet
        if is_valid_tweet(text):
            # Store the valid tweet in a variable
            tweet = text
            try:
                with conn.cursor() as cursor:
                        cursor.execute("INSERT INTO tweets (content) VALUES (%s)", (tweet,))
                conn.commit()
            except conn.Error as e:
                print("Error storing tweet:", e)
            finally:
                conn.close()
            break

    # Exit loop if valid tweet is found
    if tweet:
        break

# Print the stored tweet
print(tweet)
client.create_tweet(text=tweet)

