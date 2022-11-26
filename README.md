# rrsearch
round robin file search across multiple urls

usage examples:

default wordlist search

`cat targets.txt | python3 rrsearch.py`

search with custom wordlist

`cat targets.txt | python3 rrsearch.py -w wordlist.txt`

search and exclude code 404

`cat targets.txt | python3 rrsearch.py -w wordlist.txt --exclude-code 404`

match code 401

`cat targets.txt | python3 rrsearch.py -w wordlist.txt --match-code 401`

exclude string Not Found

`cat targets.txt | python3 rrsearch.py -w wordlist.txt --exclude-string "Not Found"`
