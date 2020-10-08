from termcolor import colored
from traceback import print_exc
from re import search, IGNORECASE
from urllib.parse import urlparse

from lib.Engine import Engine
from lib.PathFunctions import PathFunction
from lib.Globals import ColorObj, base64char, hexchar
from lib.Globals import dom_sources_regex, dom_sinks_regex
from lib.Globals import url_regex, subdomain_regex, path_regex
from lib.Globals import single_path_regex
from lib.Functions import manage_output, shannon_entropy

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
                output_list.append(self.domsource_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.domsink_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.url_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.path_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.subdomain_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.shannon_extract(line))
                if self.continuer: self.continuer = 0; continue
            return output_list
        except Exception:
            print_exc()

    def domsource_extract(self, line):
        output_list = ""
        for dom_source in dom_sources_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = manage_output(f"{line.strip(' ')} <--- DomXSS Source {dom_source}\n", color=dom_source)
                self.continuer = 1
                return output_list
        return ""

    def domsink_extract(self, line):
        output_list = ""
        for dom_source in dom_sinks_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = manage_output(f"{line.strip(' ')} <--- DomXSS Source {dom_source}\n", color=dom_source)
                self.continuer = 1
                return output_list
        return ""

    def subdomain_extract(self, line):
        output_list = ""
        if not self.argv.domain:
            return ""
        subdomain = subdomain_regex(self.argv.domain)
        if search(subdomain, line, IGNORECASE):
            sub = [w for w in line.split(' ') if search(subdomain, w, IGNORECASE)][0].replace(';', '').strip('"').strip("'")
            print(f"{ColorObj.good} Found subdomain: {colored(sub, color='red', attrs=['bold'])}")
            output_list = manage_output(f"{sub} <--- SubRegex {subdomain}\n", color=sub)
            self.continuer = 1
            return output_list
        return ""
    
    def url_extract(self, line):
        output_list = ""
        if search(url_regex, line):
            line = search(url_regex, line).group()
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = manage_output(f"{line.strip(' ')} <--- Endpoint \n")
            self.continuer = 1
            return output_list
        return ""
    
    def path_extract(self, line):
        output_list = ""
        if search(path_regex, line):
            line = search(path_regex, line).group()
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = manage_output(f"{line.strip(' ')} <--- Endpoint \n")
            self.continuer = 1
        elif search(single_path_regex, line):
            line = self.reduce_string(search(single_path_regex, line).group(), args=['"', "'"])
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = manage_output(f"{line.strip(' ')} <--- Endpoint \n")
            self.continuer = 1
            return output_list
        return "" 

    def shannon_extract(self, line):
        output_list = ""
        if self.argv.enable_entropy:
            for word in line.split(' '):
                if len(word) > 5:
                    if float(shannon_entropy(word, base64char)) > float(3.43) or float(shannon_entropy(word, hexchar)) > float(3.5):
                        word = self.reduce_string(word.rstrip(';'), args=['"', "'"])
                        print(f"{ColorObj.good} Suspicious data: {colored(word, color='red', attrs=['bold'])}")
                        output_list = manage_output(f"{word} <--- Entropy \n")
                        self.continuer = 1
                        return output_list
        return ""
    
    def reduce_string(self, line, args):
        line = line.rstrip('//').rstrip(';')
        for arg in args:
            if arg in line and line[0] == arg and line[-1] == arg:
                line = line[1:-1]
                return line
            elif arg == "(" or arg == ")":
                if line[0] == "(" and line[-1] == ")":
                    line = line[1:-1]
                    return line
        return line
