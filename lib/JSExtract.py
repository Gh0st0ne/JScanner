from termcolor import colored
from traceback import print_exc
from re import search, IGNORECASE
from urllib.parse import urlparse

from lib.Engine import Engine
from lib.PathFunctions import PathFunction
from lib.Globals import ColorObj, base64char, hexchar
from lib.Globals import dom_sources_regex, dom_sinks_regex
from lib.Globals import url_regex, subdomain_regex, path_regex
from lib.Globals import single_path_regex, library_regex
from lib.Globals import web_services_regex, custom_sensitive, custom_insensitive
from lib.Functions import manage_output, shannon_entropy

# (DONT REMOVE COMMENTS)
# Web services combined in url_extract function 

JSE = Engine()
FPathApp = PathFunction()

class JSExtract:
    def __init__(self, argv):
        self.continuer = 0
        self.argv = argv

    def extract_from_url(self, url: str) -> bool:
        try:
            output_list = []
            jsurl = FPathApp.urler(url)
            parsed_url = urlparse(jsurl)
            print(f"{ColorObj.information} Getting data from {colored(jsurl, color='yellow', attrs=['bold'])}")
            output_list.append((f"URL: {colored(jsurl, color='yellow', attrs=['bold'])}\n\n"))
            (lambda __after: [__after() for self.argv.domain in [(parsed_url.netloc)]][0] if parsed_url.netloc and not self.argv.domain else __after())(lambda: None)
            if search(".*\.js$", parsed_url.path):
                jstext = JSE.returnjs_fromjs(jsurl)
                jscomments = None
                js_exlines = None
                js_hidden = None
            elif not search(".*\.js$", parsed_url.path):
                jstext, js_other = JSE.returnjs_fromhtml(jsurl)
                jscomments, js_exlines, js_hidden = js_other
            if jscomments:
                for jscomment in jscomments:
                    jscomment = '"' + jscomment +'"'
                    print(f"{ColorObj.good} Comments: {colored(jscomment.strip(' '), color='red', attrs=['bold'])}")
                    output_list.append([manage_output(f"{jscomment.strip(' ')} <--- Comments\n"), 'Comments'])
            if js_exlines:
                for exline in js_exlines:
                    output_list.append(self.exline_extract(exline['src']))
                    if self.continuer: self.continuer = 0; continue
            if js_hidden:
                print(f"{ColorObj.good} Hidden input parameters: {colored(js_hidden, color='red', attrs=['bold'])}")
                output_list.append([manage_output(f"{js_hidden} <--- Hidden parameters\n"), 'Hidden'])
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
                output_list.append(self.custom_extract(line))
                if self.continuer: self.continuer = 0; continue
                output_list.append(self.shannon_extract(line))
                if self.continuer: self.continuer = 0; continue
            return tuple(filter(lambda x: x != [], output_list)) # [e for e in output_list if e]
        except Exception:
            print_exc()

    def exline_extract(self, line: str) -> list:
        output_list = []
        anydigit = lambda x: any(map(str.isdigit, x))
        lib = line.split('/')[-1]
        for library in library_regex:
            if search(library, line, IGNORECASE):
                print(f"{ColorObj.good} Found {library} library: {colored(lib + ' from ' + line, color='red', attrs=['bold'])}")
                if anydigit(line):
                    print("Version extraction is in development")
                output_list = [manage_output(f"{line.rstrip(' ')} <--- Library\n", color=library), 'Exline']
                self.continuer = 1
                return output_list
        return []

    def domsource_extract(self, line: str) -> list:
        output_list = []
        for dom_source in dom_sources_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- DomXSS Source\n", color=dom_source), 'Source']
                self.continuer = 1
                return output_list
        return []

    def domsink_extract(self, line: str):
        output_list = []
        for dom_source in dom_sinks_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{ColorObj.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- DomXSS Source\n", color=dom_source), 'Sink']
                self.continuer = 1
                return output_list
        return []

    def subdomain_extract(self, line: str) -> list:
        output_list = []
        if not self.argv.domain:
            return output_list
        subdomain = subdomain_regex(self.argv.domain)
        if search(subdomain, line, IGNORECASE):
            sub = [w for w in line.split(' ') if search(subdomain, w, IGNORECASE)][0].replace(';', '').strip('"').strip("'")
            print(f"{ColorObj.good} Found subdomain: {colored(sub, color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{sub} <--- Subdomain\n", color=sub), 'Subdomain']
            self.continuer = 1
            return output_list
        return []
    
    def url_extract(self, line: str) -> list:
        output_list = []
        for web_service in web_services_regex:
            if search(web_service, line):
                line = search(url_regex, line).group()
                print(f"{ColorObj.good} Found web service/storage: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- Web service\n"), 'Webservice']
                self.continuer = 1
                return output_list
        if search(url_regex, line):
            line = search(url_regex, line).group()
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Url"]
            self.continuer = 1
            return output_list
        return []
    
    def path_extract(self, line: str) -> list:
        output_list = []
        if search(path_regex, line):
            line = search(path_regex, line).group()
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Endpoint"]
            self.continuer = 1
        elif search(single_path_regex, line):
            line = self.reduce_string(search(single_path_regex, line).group(), args=['"', "'"])
            print(f"{ColorObj.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Endpoint"]
            self.continuer = 1
            return output_list
        return []

    def shannon_extract(self, line: str) -> list:
        output_list = []
        if self.argv.enable_entropy:
            for word in line.split(' '):
                if len(word) > 5:
                    if float(shannon_entropy(word, base64char)) > float(3.43) or float(shannon_entropy(word, hexchar)) > float(3.5):
                        word = self.reduce_string(word.rstrip(';'), args=['"', "'"])
                        print(f"{ColorObj.good} Suspicious data: {colored(word, color='red', attrs=['bold'])}")
                        output_list = [manage_output(f"{word} <--- Entropy \n"), "Entropy"]
                        self.continuer = 1
                        return output_list
        return []
    
    def custom_extract(self, line: str) -> list:
        output_list = []
        for custom in custom_sensitive:
            if search(custom, line):
                print(f"{ColorObj.good} Custom regex match: {colored(line, color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line} <--- Custom regex \n"), "Custom"]
                self.continuer = 1
                return output_list
        for custom in custom_insensitive:
            if search(custom, line, IGNORECASE):
                print(f"{ColorObj.good} Custom regex match: {colored(line, color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line} <--- Custom regex \n"), "Custom"]
                self.continuer = 1
                return output_list
        return []

    
    def reduce_string(self, line: str, args: list) -> str:
        if not line:
            return ""
        line = line.rstrip('//').rstrip(';')
        for arg in args:
            if arg in line and line[0] == arg and line[-1] == arg:
                return line[1:-1]
            elif arg == "(" or arg == ")":
                if line[0] == "(" and line[-1] == ")":
                    return line[1:-1]
        return line

