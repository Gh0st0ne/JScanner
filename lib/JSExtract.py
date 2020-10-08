from traceback import print_exc
from re import search, IGNORECASE
from termcolor import colored
from urllib.parse import urlparse

from lib.Engine import Engine
from lib.Globals import dom_sources_regex, dom_sinks_regex
from lib.Globals import url_regex, subdomain_regex
from lib.Globals import ColorObj
from lib.Functions import manage_output
from lib.PathFunctions import PathFunction

JSE = Engine()
FPathApp = PathFunction()

class JSExtract:
    def __init__(self, argv):
        self.continuer = 0
        self.argv = argv

    def extract_from_url(self, url) -> bool:
        try:
            output_list = []
            jsurl = FPathApp.urler(url)
            print(f"{ColorObj.information} Getting data from {colored(jsurl, color='yellow', attrs=['bold'])}")
            output_list.append((f"URL: {colored(jsurl, color='yellow', attrs=['bold'])}\n\n"))
            parsed_url = urlparse(jsurl)
            (lambda __after: [__after() for self.argv.domain in [(parsed_url.netloc)]][0] if parsed_url.netloc and not self.argv.domain else __after())(lambda: None)
            if search(".*\.js$", parsed_url.path):
                jstext = JSE.returnjs_fromjs(jsurl)
                jscomments = None
            elif not search(".*\.js$", parsed_url.path):
                jstext, jscomments = JSE.returnjs_fromhtml(jsurl)
            if jscomments:
                for jscomment in jscomments:
                    print(f"{ColorObj.good} Comments: {colored(jscomment.strip(' '), color='red', attrs=['bold'])}")
                    output_list.append(manage_output(f"{jscomment.strip(' ')} <--- Comments\n"))
            for line in jstext:
                line = line.strip(' ').rstrip('{').rstrip(' ').lstrip('}').lstrip(' ')
                for dom_source in dom_sources_regex:
                    if search(dom_source, line, IGNORECASE):
                        print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                        output_list.append(manage_output(f"{line.strip(' ')} <--- DomXSS Source {dom_source}\n", color=dom_source))
                        self.continuer = 1
                        break
                if self.continuer:
                    self.continuer = 0
                    continue
                for dom_sink in dom_sinks_regex:
                    if search(dom_sink, line, IGNORECASE):
                        print(f"{ColorObj.good} Found Dom XSS Sink: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                        output_list.append(manage_output(f"{line.strip(' ')} <--- DomXSS Sink {dom_sink}\n", color=dom_sink))
                        self.continuer = 1
                        break
                if self.continuer:
                    self.continuer = 0
                    continue
                if search(url_regex, line):
                    print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                    output_list.append(manage_output(f"{line.strip(' ')} <--- Endpoint \n"))
                    continue
                if self.argv.domain:
                    subdomain = subdomain_regex(self.argv.domain)
                    if search(subdomain, line, IGNORECASE):
                        actual_sub = [word for word in line.split(' ') if search(subdomain, word, IGNORECASE)][0].replace(';', '').strip('"').strip("'")
                        print(f"{ColorObj.good} Found subdomain: {colored(actual_sub, color='red', attrs=['bold'])}")
                        output_list.append(manage_output(f"{actual_sub} <--- SubRegex {subdomain}\n", color=actual_sub))
                        continue
                if self.argv.enable_entropy:
                    for word in line.split(' '):
                        if len(word) > 5:
                            if float(shannon_entropy(word, base64char)) > float(3.5) or float(shannon_entropy(word, hexchar)) > float(3.6):
                                print(f"{ColorObj.good} Suspicious data: {colored(word, color='red', attrs=['bold'])}")
                                output_list.append(manage_output(f"{word} <--- Entropy \n"))
            return output_list
        except Exception:
            print_exc()
