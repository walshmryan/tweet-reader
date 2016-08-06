'''
tweet-reader.py

Version: .1

'''
import tweepy

auth = tweepy.OAuthHandler('---', '---')
auth.set_access_token('---', '---')

api = tweepy.API(auth)

twitterID = input('Enter the person you are looking for\n')

topWords = input('Enter the words you are searching for (with spaces inbetween each)\n').lower()


numTweets = 500
#public_tweets = api.user_timeline(id = 'realDonaldTrump', count = numTweets)


def process_tweet(status):

	return status.text.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('"', '').replace('-', ' ').lower().split()


Hash = {}

# hash all tweets
for status in tweepy.Cursor(api.user_timeline, id='realDonaldTrump').items(numTweets):

	for word in process_tweet(status):

		# add all words to hash count
		if(word not in Hash):
			Hash[word] = 1
		else:
			Hash[word]+= 1


print('\nSearched Words of last 200 tweets:')

for topWord in topWords.split():

	value = Hash[topWord]

	print('    ' + topWord + ': ' + str(value) + ', %' + str(value * 100 / numTweets) + ' of tweets')



print('\nOther Top Words:')

count = 0

for w in sorted(Hash, key=Hash.get, reverse=True):

	if count > 10: break

	if w not in ('the', 'a', 'it', 'to', 'so', 'be', 'it', 'i', 'is', 'of', 'in', 'and', 'https://t', 'on', 'for', 'was', 'with'):
		print('    ' + w + ': ' + (str)(Hash[w]))
		count+= 1
