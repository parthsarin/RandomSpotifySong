# Random Spotify Song

This project contains Python files that will play a random song from Spotify by looking up the top thirty songs for a random three-letter string and picking one of them.

In order to allow the program to authenticate with Spotify, you will need to install the `spotipy` module for Python. You can install the latest version with the command:

```
pip install git+https://github.com/plamere/spotipy.git --upgrade
```

The first time you instantiate `RandomPlayer`, it will prompt you for your username (and store that value locally) and then it should redirect you to a web browser and authenticate with Spotify. Once authenticated, you will be redirected to a `localhost` address that will probably not load. You should paste the url you are redirected to into the terminal. This authenticates the program with Spotify.

The `RandomPlayer` class works is designed to work as per the following template:

```Python
player = RandomPlayer()
player.authenticate()

player.playRandomSong(numSongs = 10) # Will throw an AuthenticationError if player isn't authenticated
```

That code would start playback of 10 random songs on Spotify.

You can also do the same thing by executing the following command:
```
python randomsong.py --num-songs 10
```
