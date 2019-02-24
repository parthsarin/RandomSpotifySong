"""
Plays random songs on Spotify.
"""

import random # for choosing random songs
import sys # for verbose mode
import string # for random queries
from errors import AuthenticationError

### Spotify-specific ###
import spotipy # Spotify API
import spotipy.util as util # for authorized requests
import keys # unique information about the account to link to

class RandomPlayer:
	def __init__(self):
		self.AUTH_SCOPE = 'user-read-currently-playing user-modify-playback-state user-read-playback-state streaming'
		self.REDIRECT_URI = 'http://localhost/randomsong/authenticate'
		self.authenticated = False

	def authenticate(self, verbose = False):
		"""Authenticates with the Spotify API by prompting the user for
		information that we need.

		:verbose: Enables verbose mode.
		:returns: The authentication token, if it was successful.
		"""
		# Prompt for the username if we don't already have it.
		if not keys.USERNAME:
			username = input("Spotify username? ")
		else:
			username = keys.USERNAME

		# Authenticate with the web API if it's not already provided.
		if keys.CLIENT_ID:
			token = util.prompt_for_user_token(username, self.AUTH_SCOPE, client_id = keys.CLIENT_ID, client_secret = keys.CLIENT_SECRET, redirect_uri = self.REDIRECT_URI)
		else:
			token = util.prompt_for_user_token(username, self.AUTH_SCOPE, redirect_uri = self.REDIRECT_URI)

		if token:
			if verbose: print("Authenticated successfully.")
			self.token = token
			self.sp = spotipy.Spotify(auth=token)
			self.authenticated = True
		else:
			if verbose: print("Authentication unsuccessful.")
			raise AuthenticationError("Authentication unsuccessful")

	def checkAuthentication(self):
		"""Raises an error if the instance is not authenticated.
		"""
		if not self.authenticated:
			raise AuthenticationError("The instance is not authenticated.")

	def playRandomSong(self, numSongs=1, verbose=False):
		"""Plays random songs.

		:numSongs: The number of random songs to play.
		:verbose: Enables verbose mode.
		"""
		self.checkAuthentication()

		songs = [ self.getRandomSong(verbose) for i in range(numSongs) ]
		uris = [ song['uri'] for song in songs ]
		self.sp.start_playback(uris = uris)

		if verbose: print("Started playback...")

	def getRandomSong(self, verbose=False):
		"""Returns a random song by searching for a random three
		character string and picking a random song from the top
		30 songs.

		:verbose: Enables verbose mode.
		"""
		self.checkAuthentication()
		alphabet = string.ascii_lowercase + string.digits

		while True:
			randSearchString = random.choice(alphabet) + random.choice(alphabet) + random.choice(alphabet)

			if verbose: print("Retrieving songs for query '{}'...".format(randSearchString))
			randSongs = self.sp.search(randSearchString, limit=30)
			if verbose: print("Retrieved {} songs.".format(len(randSongs['tracks']['items'])))

			if randSongs['tracks']['items']:
				output = random.choice(randSongs['tracks']['items'])
				if verbose:
					artists = [ artist['name'] for artist in output['artists'] ]
					print("There are valid songs. Choosing {} by {}.".format(output['name'], ', '.join(artists)))
				return output
			elif verbose:
				print("There are no valid songs. Trying again.")

if __name__ == '__main__':
	if '-v' in sys.argv:
		verbose = True
	else:
		verbose = False

	if '--numSongs' in sys.argv:
		index = sys.argv.index('--numSongs')
		numSongs = int(sys.argv[index+1])
	else:
		numSongs = 10

	player = RandomPlayer()
	player.authenticate(verbose=verbose)
	player.playRandomSong(numSongs=numSongs, verbose=verbose)
