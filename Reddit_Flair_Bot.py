'''
Author: John B Huttlinger
Purpose: Auto post flair checking bot for reddit.
Date last modified: 12:56:18 PM Thursday, February 27, 2014

Actions required to implement:
	1. A reddit account with moderator status of your subreddit. (This account will need at least 2 link karma in order to function correctly. /r/FreeKarma is a great sub to use for this.)
	2. The PRAW module will need to be installed on the machine running this bot. Praw can be found here: https://praw.readthedocs.org/en/latest/
		If you are not familiar with installing a python module, this video will help you (At least for a Windows installation): http://www.youtube.com/watch?v=ddpYVA-7wq4
'''
# necessary imports 
import praw
from time import time, sleep
from sys import exc_clear
from urllib import quote

# define function main()
def main():
	username = "username"
	password = "password"
	subreddit_name = "your_subreddit"

	sleep_time = 300 # time (in seconds) the bot sleeps before performing a new check
	time_until_message = 180 # time (in seconds) a person has to add flair before a warning message is sent
	time_until_remove = 3600 # time (in seconds) after a message is sent that a person has to add flair before the post is removed

	post_grab_limit = 20 # how many new posts to check at a time. needs to be greater than the number of submissions that could be made in the amount of time the bot sleeps (sleep_time)
	post_memory_limit = 100 # how many posts the bot should "remember".

	# customizable warning message asking poster to add flair
	add_flair_subject_line = "You have not tagged your post."
	add_flair_message = "[Your recent post]({post_url}) in /r/" + subreddit_name + " does not have any flair.\n\nPlease add flair to your post. If you do not add flair within **" + formatTimeString( time_until_remove ) + "**, your post will be removed."
	
	# customizable mod mail template
	custom_mod_mail_subject_line = "Flair Added"
	custom_mod_mail_message = "Replace this text with your post's url"

	# customizable warning message informing poster their submission was removed
	remove_post_subject_line = "You have not tagged your post within the allotted amount of time."
	remove_post_message = "[Your recent post]({post_url}) in /r/" + subreddit_name + " still does not have any flair and has been removed. Please add flair to your post and [message the moderators](" + createCustomModMailUrl( subreddit_name, custom_mod_mail_subject_line, custom_mod_mail_message ) + ") with a link to your post."

	# don't change anything below this line unless you know what you're doing!
	no_flair = []
	already_done = []
	post_age = time_until_message + time_until_remove
	user_agent = ( "Auto flair moderator for /r/" + subreddit_name ) # tells reddit the bot's purpose.
	session = praw.Reddit( user_agent = user_agent )
	session.login( username = username, password = password )
	subreddit=session.get_subreddit( subreddit_name )

	# start endless loop
	while True:
		# memory clean up code
		# keeps arrays at reasonable sizes
		if len( already_done ) >= post_memory_limit:
			i = 0
			posts_to_forget = post_memory_limit - post_grab_limit
			while i < posts_to_forget:
				already_done.pop( 0 )
				i += 1
		if len( no_flair ) >= post_memory_limit:
			i = 0
			while i < posts_to_forget:
				no_flair.pop( 0 )
				i += 1
		# try-catch runtime issues. Prevents bot from crashing when a problem is encountered. 
		# Most frequent trigger is a connection problem (reddit is down)
		try:
			# get newest 20 submissions
			for submission in subreddit.get_new( limit = post_grab_limit ):
				# if post is older than specified age
				if( ( time() - submission.created_utc ) > time_until_message ):
					# if post has not already been processed
					if submission.id not in already_done:
						# if post has not already been flagged for not having flair
						if submission.id not in no_flair:
							# if post does not have flair
							if ( submission.link_flair_text is None ):
								author = submission.author
								final_add_flair_message = add_flair_message.format( post_url = submission.short_link )
								#login and send user message
								session.login( username = username, password = password )
								session.send_message( author, add_flair_subject_line, final_add_flair_message )
								no_flair.append( submission.id )
							#if the post has flair, it is added to already_done
							else:
								already_done.append(submission.id)
					#checks if the post is in no_flair
					if submission.id in no_flair:
						#checks if the post is past the set age
						if ( ( time() - submission.created_utc ) > post_age ):
							#checks post for flair
							#posts without flair at this point will be removed
							if ( submission.link_flair_text is None ):
								author=submission.author
								final_remove_post_message = remove_post_message.format( post_url = submission.short_link )
								#login, send message, remove post
								session.login( username = username, password = password )
								session.send_message( author, remove_post_subject_line, final_remove_post_message )
								submission.remove()
								already_done.append( submission.id )
							else:
								already_done.append( submission.id )
		#handles runtime errors.
		except Exception:
			#clears the exception
			exc_clear()
		sleep( sleep_time )

# turn a time in seconds into a human readable string
def formatTimeString(time_in):
     minutes, seconds = divmod( time_in, 60 )
     hours, minutes = divmod( minutes, 60 )
     time_string = ""
     if hours > 0:
          time_string += "{0} hour".format(hours)
          if hours > 1:
               time_string += "s"
          time_string += " "
     if minutes > 0:
          time_string += "{0} minute".format(minutes)
          if minutes > 1:
               time_string += "s"
          time_string += " "
     if seconds > 0:
          time_string += "{0} second".format(seconds)
          if seconds > 1:
               time_string += "s"
          time_string += " "
     return time_string[:-1]

# create a custom mod mail message url
def createCustomModMailUrl( subreddit, subject, message ):
     url = "http://www.reddit.com/message/compose/?to=/r/" + subreddit + "&subject=" + quote( subject, '' ) + "&message=" + quote( message, '' )
     return url



#call main
main()