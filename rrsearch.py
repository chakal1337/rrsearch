#!/usr/bin/python3
import sys
import socket
import requests
import time
import threading
import random
import string
import re
import argparse
from urllib.parse import urljoin

targets = []
wordlist = []
regex_match = ""
code_match = 0
string_match = ""
regex_exclude = ""
code_exclude = 0
string_exclude = ""
threadcount = 10

debug = 0

parser = argparse.ArgumentParser(prog = 'RRSearch', description = 'Round robin search for files across many urls', epilog = '')

parser.add_argument('-w', '--wordlist')
parser.add_argument('-mr', '--match-regex')
parser.add_argument('-er', '--exclude-regex')
parser.add_argument('-mc', '--match-code')
parser.add_argument('-ec', '--exclude-code')
parser.add_argument('-ms', '--match-string')
parser.add_argument('-es', '--exclude-string')
parser.add_argument('-t', '--threads') 

args = parser.parse_args()

if args.wordlist:
 with open(args.wordlist, "rb") as file:
  wordlist = file.read().decode().splitlines()
else:
 with open("default.txt", "rb") as file:
  wordlist = file.read().decode().splitlines()

if args.match_regex:
 regex_match = args.match_regex

if args.exclude_regex:
 regex_exclude = args.exclude_regex
 
if args.match_code:
 code_match = int(args.match_code)

if args.exclude_code:
 code_exclude = int(args.exclude_code)

if args.threads:
 threadcount = int(args.threads)
 
if args.match_string:
 string_match = args.match_string

if args.exclude_string:
 string_exclude = args.exclude_string

for line in sys.stdin:
 line = line.strip()
 if not line in targets: targets.append(line)

def scan_url(url, word):
 headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"}
 url = urljoin(url, word)
 with requests.get(url=url, headers=headers, allow_redirects=False, stream=True, timeout=5) as r:
  if r.status_code == code_exclude: return False
  if r.status_code == code_match: return True
  if string_match != "" and string_match in r.text: return True
  if string_exclude != "" and string_match in r.text: return False
  if regex_match != "" and re.match(regex_match, r.text): return True
  if regex_exclude != "" and re.match(regex_exclude, r.text): return False  
  return False

def start_scan():
 global wordlist
 while len(wordlist):
  with threading.Lock(): word = wordlist.pop(0)
  targets_l = list(targets)
  random.shuffle(targets_l)
  for url in targets_l:
   try:
    if scan_url(url, word):
     print(urljoin(url, word))
   except Exception as error:
    if debug == 1: print(error)
    
for i in range(threadcount):
 t=threading.Thread(target=start_scan)
 t.start()
