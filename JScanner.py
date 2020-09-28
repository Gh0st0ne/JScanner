#!/usr/bin/python3

from re import search
from requests import get
from faster_than_requests import get
from termcolor import colored
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from jsbeautifier import beautify
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Functions import starter, manage_output
from lib.Functions import output_directory_writer, output_writer
from lib.PathFunctions import PathFunction
from lib.Globals import *

parser = ArgumentParser(description=colored('Javascript Scanner', color='yellow'), epilog=colored("Enjoy bug hunting", color='yellow'))
input_group = parser.add_mutually_exclusive_group()
output_group = parser.add_mutually_exclusive_group()
input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
input_group.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
parser.add_argument('-d', '--domain', type=str, help="Domain name")
output_group.add_argument('-oD', '--output-directory', type=str, help="Output directory")
output_group.add_argument('-o', '--output', type=str, help="Output file")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()
input_wordlist = starter(argv)

def scan_js(url: str) -> bool:
    FPathApp = PathFunction()
    output_list = []
    urlparser = urlparse(url)
    if search(".*\.js$", urlparser.path):
        try:
            jsurl = FPathApp.slasher(FPathApp.urler(urlparser.netloc)) + FPathApp.payloader(urlparser.path)
            print(f"{ColorObj.information} Trying to get data from {colored(jsurl, color='cyan')}")
            output_list.append(manage_output(f"{jsurl}  <--- URL\n"))
            jsresp = get(jsurl)
            jstext = str(beautify(jsresp["body"])).split('\n')
            for jsline in jstext:
                for dom_source in dom_sources_regex:
                    if search(dom_source, jsline):
                        print(f"{ColorObj.good} Found Dom XSS Source: {colored(jsline.strip(' '), color='cyan')}")
                        output_list.append(manage_output(f"{jsline.strip(' ')} <--- DomXSS Source {dom_source}\n"))
                for dom_sink in dom_sinks_regex:
                    if search(dom_sink, jsline):
                        print(f"{ColorObj.good} Found Dom XSS Sink: {colored(jsline.strip(' '), color='cyan')}")
                        output_list.append(manage_output(f"{jsline.strip(' ')} <--- DomXSS Sink {dom_sink}\n"))
            return output_list
        except Exception as E:
            print(f"{ColorObj.bad} Exception {E},{E.__class__} occured")
            return False
    if not search(".*\.js$", urlparser.path):
        try:
            jsurl = FPathApp.slasher(FPathApp.urler(urlparser.netloc)) + FPathApp.payloader(urlparser.path)
            print(f"{ColorObj.information} Trying to get data from {colored(jsurl, color='cyan')}")
            output_list.append(manage_output(f"{jsurl} <--- URL\n"))
            jsresp = get(jsurl)
            jsx = BeautifulSoup(jsresp["body"], 'html.parser')
            jssoup = jsx.find_all("script")
            for jscript in jssoup:
                if jscript != None:
                    jstext = str(beautify(jscript.string)).split('\n')
                    for jsline in jstext:
                        for dom_source in dom_sources_regex:
                            if search(dom_source, jsline):
                                print(f"{ColorObj.good} Found Dom XSS Source: {colored(jsline.strip(' '), color='cyan')}")
                                output_list.append(manage_output(f"{jsline} <--- DomXSS Source {dom_source}\n"))
                        for dom_sink in dom_sinks_regex:
                            if search(dom_sink, jsline):
                                print(f"{ColorObj.good} Found Dom XSS Sink: {colored(jsline.strip(' '), color='cyan')}")
                                output_list.append(manage_output(f"{jsline} <--- DomXSS Sink {dom_sink}\n"))
            return output_list
        except Exception as E:
            print(f"{ColorObj.bad} Exception {E},{E.__class__} occured")
            return False
def main():
    global input_wordlist
    with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
        future_objects = [submitter.submit(scan_js, inputs) for inputs in input_wordlist]
        if argv.output_directory:
            output_writer(argv.output_directory, argv.domain, future_objects)
        if argv.output:
            output_writer(argv.output, future_objects)

if __name__ == "__main__":
    try:
        main()
    except Exception as E:
        print(E,E.__class__)
