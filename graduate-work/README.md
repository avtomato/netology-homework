# UniGrouper - finder of user's unique groups #

Get a list of user's groups, that exclude user's friends

## How to install dependencies ##

```
pip install -r requirements.txt
```

## How to use ##

```
python unigrouper.py -h

usage: UniGrouper - finder of user's unique groups [-h] [-n NUMBERS] [-p PATH]
                                                   [--debug] [-v] [-V]
                                                   [user]

Get a list of user's groups, that exclude user's friends

positional arguments:
  user                  username or user_id to search his unique groups

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBERS, --numbers NUMBERS
                        allowable number of user's friends in group (positive
                        integer, default n = 0)
  -p PATH, --save-path PATH
                        path to directory where to save files
  --debug               print debug log
  -v, --verbose         print a detailed log
  -V, --version         print version info and exit
```