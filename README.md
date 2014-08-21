Reddit-Flair-Bot
================
This is a reddit bot designed to check submission flair. It uses the PRAW library.

###What it does:  
* Messages users if their post does not have flair within a preset amount of time
* Removes posts that do not have flair within a preset amount of time

###Features:  
* Customize time until message is sent and time until post is removed
* Customize number of posts checked at a time and number of posts the bot "remembers".
* Customize time between checks
* Customizable messages (Includes a function to create a url leading to a preset mod mail message)

###Requiremnts:
* The PRAW library (found [here](https://praw.readthedocs.org/en/v2.1.16/))
* A reddit account with moderator status on your subreddit. This account must have at least 2 link karma to function properly. [/r/freekarma](http://www.reddit.com/r/freekarma) is a great place to achieve this.

###Instructions
