#!/usr/bin/env python3
"""
Plays random songs on Spotify.
"""

import random # for choosing random songs
import sys # for verbose mode
import string # for random queries
import pickle # for storing the username
import pathlib # for storing the username
from errors import AuthenticationError

### Spotify-specific ###
import spotipy # Spotify API
import spotipy.util as util # for authorized requests

class RandomPlayer:
	def __init__(self):
		self.AUTH_SCOPE = 'user-read-currently-playing user-modify-playback-state user-read-playback-state streaming'
		self.REDIRECT_URI = 'http://localhost/randomsong/authenticate'
		self.CLIENT_ID = 'f2063b1303a240e5a5a1757ab364332e'
		self.CLIENT_SECRET = 'ef9b4fccdeb34f67b703febcf1670d1b'
		self.authenticated = False

	def _getUsername(self):
		"""Gets the Spotify username for the user and stores
		it as a cached file.
		"""
		usernameFile = pathlib.Path(".cache-username")
		if usernameFile.is_file():
			with usernameFile.open('rb') as f:
				return pickle.load(f)
		else:
			username = input("Spotify username? ")
			with usernameFile.open('wb') as f:
				pickle.dump(username, f)
			return username

	def authenticate(self, verbose = False):
		"""Authenticates with the Spotify API by prompting the user for
		information that we need.

		:verbose: Enables verbose mode.
		:returns: The authentication token, if it was successful.
		"""
		# Get the username
		self.username = self._getUsername()

		# Authenticate with the web API if it's not already provided.
		token = util.prompt_for_user_token(self.username, self.AUTH_SCOPE, client_id = self.CLIENT_ID, client_secret = self.CLIENT_SECRET, redirect_uri = self.REDIRECT_URI)

		if token:
			if verbose: print("Authenticated successfully.")

			self.token = token
			self.sp = spotipy.Spotify(auth=token)
			self.authenticated = True

		else:
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

	if '--num-songs' in sys.argv:
		index = sys.argv.index('--num-songs')
		numSongs = int(sys.argv[index+1])
	else:
		numSongs = 10

	player = RandomPlayer()
	player.authenticate(verbose=verbose)
	player.playRandomSong(numSongs=numSongs, verbose=verbose)
