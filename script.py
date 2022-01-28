import praw
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fuzzywuzzy import fuzz
import pymongo

f = open("secrets.json")
secrets = json.load(f)
client = pymongo.MongoClient(secrets["MONGO_CLIENT"])

def save_data_to_mongo(post_id, title):
  db = client["redditNotifier"]
  collection = db["posts"]
  response = collection.find_one({"post_id": post_id})
  if response is None:
    collection.insert_one({"post_id": post_id,
                            "title": title})
    return True
  else:
    return False

def is_match(x, str):
  for keyword in secrets["MUST_INCLUDE"][x]:
    if keyword not in str:
      return False 
  for keyword in secrets["CAN_INCLUDE"][x]:
    if fuzz.partial_ratio(str, keyword) > 70:
      return True
  return False

def get_reddit_posts():
  reddit = praw.Reddit(client_id=secrets["CLIENT_ID"],
                      client_secret=secrets["CLIENT_SECRET"],
                      user_agent=secrets["USER_AGENT"],
                      username=secrets["USERNAME"],
                      password=secrets["PASSWORD"])
  matching_posts = []
  for x in range(len(secrets["SUBREDDITS"])):
    subreddit = reddit.subreddit(secrets["SUBREDDITS"][x])
    for submission in subreddit.new(limit=100):
      url = submission.url
      post_id = submission.id
      title = submission.title
      if is_match(x, title.lower()):
        if (save_data_to_mongo(post_id, title)):
          post = (title, url)
          matching_posts.append(post)
  return matching_posts

def send_email():
  posts = get_reddit_posts()
  if(len(posts) != 0):
    email_content = ''
    for title, url in posts:
      email_content += title +'<br>' + url + '<br>'
    subject = 'is this what you wanted?'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(secrets["SENDER_EMAIL"], secrets["SENDER_PASSWORD"])
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = secrets["SENDER_EMAIL"]
    msg['To'] = secrets["RECEIVER_EMAIL"]
    msg.attach(MIMEText(email_content, "plain"))
    html = '''\
    <html>
      <head></head>
      <body>
        <p>
            <b style='font-size:20px'>________<br>
        </p>
        %s
        <p>
            <b style='font-size:20px'>________</span></b>
        </p>
      </body>
    </html>
    ''' % email_content
    msg.attach(MIMEText(html, 'html'))
    server.sendmail(secrets["SENDER_EMAIL"], secrets["RECEIVER_EMAIL"], msg.as_string())
    server.quit()

if __name__ == "__main__":
  send_email()


