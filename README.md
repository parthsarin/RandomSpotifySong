# Random Spotify Song

This project contains Python files that will play a random song from Spotify by looking up the top ten songs for a random three-letter string and picking one of them.

In order to allow the program to authenticate with Spotify, create a file called `keys.py` and store the following information in it:

```Python
USERNAME = 'your-spotify-usernamd'
CLIENT_ID = 'spotify-client-id'
CLIENT_SECRET = 'spotify-client-secret'
```

The first time you execute the program, it should redirect you to a web browser and authenticate with Spotify and then ask you to paste the url you are redirected to into the terminal. This authenticates the program with Spotify.

The `RandomPlayer` class works is designed to work as per the following template:

```Python
player = RandomPlayer()
player.authenticate()

player.playRandomSong(numSongs = 10)
```

That code would start playback of 10 random songs on Spotify.