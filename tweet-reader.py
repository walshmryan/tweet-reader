'''
tweet-reader.py
Author: Ryan Walsh
Version: .11

A script using tweepy.py that analyzes tweets of a given twitter account
and identifies most commonly used words

'''
import tweepy

# number of tweets script searches through
numTweets = 500


'''
Gets the auth and access codes for Twitter API

codes.txt is organized as follows:
	-consumer key
	-consumer secret
	-access token
	-access secret

'''
def getCodes():

	file = open('codes.txt')

	return (file.readline().replace('\n', ''), file.readline().replace('\n', ''), file.readline().replace('\n', ''), file.readline().replace('\n', ''))
	

'''
Replaces all punctuation to help better hash words
'''
def process_tweet(status):

	return status.text.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('"', '').replace('-', ' ').lower().split()


'''
Adds all words to a dictionary, incrementing their values for every unique appearance
'''
def hashTweets(api, twitterID):

	if(twitterID == ''):
		twitterID = 'realDonaldTrump'

	print('\nSearching tweets of ' + twitterID + '...')
	dic = {}

	# for each tweet in timeline
	for status in tweepy.Cursor(api.user_timeline, id=twitterID).items(numTweets):

		# look at each word and add/increment value in dictionary
		for word in process_tweet(status):

			# add all words to dic count
			if(word not in dic):
				dic[word] = 1
			else:
				dic[word]+= 1

	return dic


'''
Reads through dictionary and presents the top words and their rarity
'''
def printTopWords(dic, topWords):

	print('\nSearched Words of last ' + str(numTweets) + ' tweets:')

	# prints given searched words and finds rarity of them
	for topWord in topWords.split():

		# tries to find top word in dictionary
		try:
			value = dic[topWord]
			print('    -' + topWord + ': ' + str(value) + ', %' + str(value * 100 / numTweets) + ' of tweets')

		# if word is not in it
		except:
			print('    -Top word \'' + topWord + '\' not found in tweets')

	if(topWords == ''):
		print('    -No words searched!')



	print('\nOther Top Words:')

	count = 0

	# prints 10 other non-searched words
	for w in sorted(dic, key=dic.get, reverse=True):

		if count > 10: break

		# ignores very common words
		if w not in ('the', 'a', 'it', 'to', 'so', 'be', 'it', 'i', 'is', 'of', 'in', 'and', 'https://t', 'on', 'for', 'was', 'with'):
			print('    -' + w + ': ' + (str)(dic[w]))
			count+= 1


if __name__ == "__main__":

	codes = getCodes()

	auth = tweepy.OAuthHandler(codes[0], codes[1])
	auth.set_access_token(codes[2], codes[3])

	api = tweepy.API(auth)

	# while used continues to want to search names
	while(True):
		twitterID = input('Enter the person you are looking for (\'q\'/\'quit\' to end)\n')

		if(twitterID == 'quit' or twitterID == 'q'):
			break

		topWords = input('Enter the words you are searching for (with spaces inbetween each)\n').lower()

		res = hashTweets(api, twitterID)

		printTopWords(res, topWords)
