# wheel_of_fortune
A simple Python 3 text based word guessing game that can be played during a video conference session.

You need to supply it a JSON file containing a list of dictionary with "number", "items" and "sources". Example:

```
    {
        "number":1,
        "input":"May the Force be with you.", 
        "source":"Star Wars, 1977"
    }, 
```

Example JSON files are given in `movie_quotes.json` and `bible_verses.json`.

Usage:
```
python3 wheel_of_fortune.py -i movie_quotes.json
```
Required argument:
```
    -i, --input_file    Specifies the input JSON file
```

Other optional arguments are:
```
    -t, --title         Specifies the title to display in a text box at the top of a game.
    -w, --screen_width  The number of characters you want to be your screen width 
```