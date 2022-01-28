email you about new posts that fuzzymatch keywords. <br />
can be used to check for specific products in used product subreddits. <br />
secrets json: 
'''
{ 
  "CLIENT_ID": "CLIENT_ID",
  "CLIENT_SECRET": "CLIENT_SECRET",
  "USER_AGENT": "USER_AGENT",
  "USERNAME": "USERNAME",
  "PASSWORD": "PASSWORD",
  "SENDER_EMAIL": "SENDER_EMAIL",
  "SENDER_PASSWORD": "SENDER_PASSWORD",
  "RECEIVER_EMAIL": "RECEIVER_EMAIL",
  "SUBREDDITS": [
    "SUBREDDIT1",
    "SUBREDDIT2",
    ...
  ],
  "MUST_INCLUDE": [
    [
      "SUBREDDIT1_term1",
      "SUBREDDIT1_term1",
      ...
    ],
    [
      "SUBREDDIT1_term1",
      "SUBREDDIT1_term2",
      ...
    ]
  ],
  "CAN_INCLUDE": [
    [
      "SUBREDDIT1_term1",
      "SUBREDDIT1_term1",
      ...
    ],
    [
      "SUBREDDIT1_term1",
      "SUBREDDIT1_term2",
      ...
    ]
  ],
  "MONGO_CLIENT": "MONGO_CLIENT"
}
'''
