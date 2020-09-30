from sys import stdin
from math import log
from termcolor import colored

from lib.Globals import ColorObj
from lib.PathFunctions import PathFunction

FPathApp = PathFunction()
def banner():
    from pyfiglet import print_figlet
    print_figlet('JScanner', font='larry3d', colors='BLUE')
    print(colored('JScanner: Find secrets and vulnerabilites!', color='red', attrs=['bold']))

def starter(argv):
    if argv.banner:
        banner()
        exit(0)
    if argv.output_directory:
        if not argv.domain:
            print(f"{ColorObj.bad} Output directory provided but not domain")
    if not argv.wordlist:
        if not argv.url:
            if not argv.stdin:
                print(f"{ColorObj.bad} Use --help")
                exit()
            else:
                stdinarray = stdin.read().split('\n')
                return [line.rstrip('\n').strip(' ') for line in stdinarray if line]
        else:
            return [argv.url.strip(' ')]
    else:
        return [line.rstrip('\n').strip(' ') for line in open(argv.wordlist) if line]

def output_directory_writer(filepath, filename, to_write):
    output_file = open(FPathApp.slasher(argv.output_directory) + argv.domain + '.jscan', 'a')
    for jsresults in to_write:
        for jsresult in jsresults.result():
            output_file.write(jsresult)
    output_file.close()

def output_writer(filename, to_write):
    output_file = open(filename, 'a')
    for jsresults in to_write:
        for jsresult in jsresults.result():
            output_file.write(jsresult)
    output_file.close()

def manage_output(line, color=None) -> tuple:
    text, appendtext = line.split('<---')
    appendtext = '<---' + appendtext
    appendtext = appendtext.rjust(148-len(text))
    if not color:
        return str(text + appendtext)
    elif color:
        joinedtext = text
        newtext = joinedtext.split(color)
        newtext = newtext[0] + colored(color, color='red') + newtext[1]
        return newtext + appendtext

def shannon_entropy(data, iterator):
    if not data:
        return 0
    entropy = 0
    for val in iterator:
        p_x = float(data.count(val))/len(data)
        if p_x > 0:
            entropy += - p_x * log(p_x, 2)
    return float(entropy)
