# JScanner
## Description
Who says python3 can't be fast! Download the JScanner binary and thats it! Fast and effective tool to find using custom and predefined regex for vulnerabilites and secrets. It scans concurrently and effectively on javascript files url for secrets and vulnerabilites. Scans JS even on non javascript endpoint. Output from other tools can be easily fed to it.

## Features
1. Fast :zap: when using compiled version!
2. Concurrent scanning of all any endpoints for javascript.
3. Predefined regex as well as custom regex definable in in lib/Globals.py.
4. Regex for DOM XSS sinks, sources, web services, interesting variable already included.
5. Shannon entropy to catch whats missed by regex.
6. Evenn though GIL might slow down its speed, its built with faster_than_requests, 39 times faster than original requests.

## Usage
```
usage: JScanner [-h] [--- | -w WORDLIST] [-d DOMAIN]
                [-oD OUTPUT_DIRECTORY | -o OUTPUT] [-t THREADS] [-b]

Javascript Scanner

optional arguments:
  -h, --help            show this help message and exit
  ---, ---              Stdin
  -w WORDLIST, --wordlist WORDLIST
                        Absolute path of wordlist
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -oD OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory
  -o OUTPUT, --output OUTPUT
                        Output file
  -t THREADS, --threads THREADS
                        Number of threads
  -b, --banner          Print banner and exit

Enjoy bug hunting
```

## Example
1. Scan a single URL/Domain/Subdomain  
* ```JScanner -d google.com``` or ```JScanner -u https://google.com/closurelibrary.js```
2. Scan from URLs
* ```JScanner -w /tmp/files.txt -oD `pwd` -t 10 -d domain.com```
3. Scan from stdin (subdomains)
* ```assetfinder google.com | JScanner --- -o results.txt```
4. Scan from stdin (hakrawler, gau both at same time)
* ```echo "uber.com" | tee >(hakrawler | JScanner --- -o hakrawler.txt -t 10) >(gau | JScanner --- -o gau.txt -t 10)```

## Caveats
1. Only scans inline javascript when non js endpoint is given
2. May provide duplicate info (URL Skipper is in progress)
3. Output need to be improved
4. Argument to scan .js file only
5. Shannon Entropy to be implemented.

## Warning
Currently under development and do contain bugs
