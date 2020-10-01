#!/usr/bin/python3

from termcolor import colored
from urllib.parse import urlparse
from re import search, IGNORECASE
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Globals import *
from lib.Engine import Engine
from lib.Functions import starter, manage_output, shannon_entropy
from lib.Functions import output_directory_writer, output_writer
from lib.PathFunctions import PathFunction

parser = ArgumentParser(description=colored('Javascript Scanner', color='yellow'), epilog=colored("Enjoy bug hunting", color='yellow'))
input_group = parser.add_mutually_exclusive_group()
output_group = parser.add_mutually_exclusive_group()
input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
input_group.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
input_group.add_argument('-u', '--url', type=str, help="URL to scan (-d not necessary when -u specified)")
parser.add_argument('-d', '--domain', type=str, help="URL")
output_group.add_argument('-oD', '--output-directory', type=str, help="Output directory")
output_group.add_argument('-o', '--output', type=str, help="Output file")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

JSE = Engine()
input_wordlist = starter(argv)
FPathApp = PathFunction()

def scan_url(url) -> bool:
    jsurl = FPathApp.urler(url)
    output_list = []
    print(f"{ColorObj.information} Getting data from {colored(jsurl, color='cyan')}")
    output_list.append((f"URL: {colored(jsurl, color='yellow', attrs=['bold'])}\n\n"))
    urlparser = urlparse(jsurl)
    (lambda __after: [__after() for argv.domain in [(urlparser.netloc)]][0] if urlparser.netloc and not argv.domain else __after())(lambda: None)
    if search(".*\.js$", urlparser.path):
        jstext = JSE.returnjs_fromjs(jsurl)
        jscomments = None
    elif not search(".*\.js$", urlparser.path):
        jstext, jscomments = JSE.returnjs_fromhtml(jsurl)
    if jscomments:
        for jscomment in jscomments:
            print(f"{ColorObj.good} Comments: {colored(jscomment.strip(' '), color='cyan')}")
            output_list.append(manage_output(f"{jscomment.strip(' ')} <--- Comments\n"))
    for line in jstext:
        line = line.strip(' ').rstrip('{').rstrip(' ').lstrip('}').lstrip(' ')
        for dom_source in dom_sources_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='cyan')}")
                output_list.append(manage_output(f"{line.strip(' ')} <--- DomXSS Source {dom_source}\n", color=dom_source))
                continue
        for dom_sink in dom_sinks_regex:
            if search(dom_sink, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Sink: {colored(line.strip(' '), color='cyan')}")
                output_list.append(manage_output(f"{line.strip(' ')} <--- DomXSS Sink {dom_sink}\n", color=dom_sink))
                continue
        if argv.domain:
            subdomain = subdomain_regex(argv.domain)
            if search(subdomain, line, IGNORECASE):
                actual_sub = [word for word in line.split(' ') if search(subdomain, word, IGNORECASE)][0].replace(';', '').strip('"').strip("'")
                print(f"{ColorObj.good} Found subdomain: {colored(actual_sub, color='cyan')}")
                output_list.append(manage_output(f"{actual_sub} <--- SubRegex {subdomain}\n", color=actual_sub))
                continue
        for word in line.split(' '):
            if len(word) > 5:
                if float(shannon_entropy(word, base64char)) > float(3.3) or float(shannon_entropy(word, hexchar)) > float(3.3):
                    print(f"{ColorObj.good} Found sensitive data: {colored(word, color='cyan')}")
                    output_list.append(manage_output(f"{word} <--- Entropy \n"))
    return output_list
    
def main():
    with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
        future_objects = [submitter.submit(scan_url, inputs) for inputs in input_wordlist]
    (lambda __after: (output_writer(argv.output_directory, argv.domain, future_objects), __after())[1] if argv.output_directory else __after())(lambda: (lambda __after: (output_writer(argv.output, future_objects), __after())[1] if argv.output else __after())(lambda: None)) #Output

if __name__ == "__main__":
    try:
        main()
    except Exception as E:
        print(E,E.__class__)
