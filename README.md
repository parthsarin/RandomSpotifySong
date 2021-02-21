# Random Spotify Song

# How to use:

This project allows you to play a random song from Spotify by looking up the top thirty songs for a random three-letter string (char schema) or commonly used word and picking one of them (word schema).

## For windows:

To run the program, double click on `RandomSpotifySong.bat`. You can also follow the instructions for other operating sytems, they will also work.

## For other operating systems:

In order to allow the program to authenticate with Spotify, you will need to install the `spotipy` module for Python. You can install the latest version with the command:

pip install git+https://github.com/plamere/spotipy.git --upgrade

After this has been done, you can now run `randomsong.py` to use the program.

## Running from command line:

The program can also be run with the command line like this: `python randomsong.py --num-songs 10 -word`.
Replace `-word` with `-char` to use the char schema
You can also include `-q` to stop program output.

## Authenticating with spotify:

The first time you run the program, it will prompt you for your username (and store that value locally) and then it should redirect you to a web browser and authenticate with Spotify. Once authenticated, you will be redirected to a `localhost` address that will probably not load. You should paste the url you are redirected to into the terminal. This authenticates the program with Spotify.

# For use in other python programs:

The `RandomPlayer` class works is designed to work as per the following template:

```Python
player = RandomPlayer(random_song_schema='word') # random_song_schema is either 'word' or 'char' depending on how you want to generate random songs (see above)
player.authenticate()
player.playRandomSong(numSongs = 10) # Will throw an AuthenticationError if player isn't authenticated
```

That code would start playback of 10 random songs on Spotify.

# So... why?

I feel like sometimes we get trapped in routines that are very similar. We take the same routes every day, consume the same kind of media every day, etc. Music is one of those routines: people don't really get exposed to new kinds of music very frequently. Spotify recommends music based on a user's past listening history, so it's difficult to discover *truly* new kinds of music with Spotify's default tools and auto-generatred playlists. 

A Google search for "random Spotify song" will reveal that I'm not the first person to think of this. There are other websites and apps that try to do the same thing but none of the other services I found were really random. Most were just curated playlists which were very diverse in genre. This tool incorporates several layers of randomness to try to get as close to random songs as possible.
