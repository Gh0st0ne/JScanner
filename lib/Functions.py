from sys import stdin
from termcolor import colored
from lib.Globals import ColorObj

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
        if not argv.domain:
            if not argv.stdin:
                print(f"{ColorObj.bad} Use --help")
                exit()
            else:
                stdinarray = stdin.read().split('\n')
                return [line.rstrip('\n').strip(' ') for line in stdinarray if line]
        else:
            return [argv.domain]
    else:
        return [line.rstrip('\n').strip(' ') for line in open(argv.wordlist) if line]

def output_writer(filepath, filename, to_write):
    output_file = open(FPathApp.slasher(argv.output_directory) + argv.domain + '.jscan', 'a')
    for jsresult in to_write:
        output_file.write(jsresult)
    output_file.close()

def output_writer(filename, to_write):
    output_file = open(filename, 'a')
    for jsresult in to_write:
        output_file.write(jsresult)
    output_file.close()

def manage_output(line) -> tuple:
    text, appendtext = line.split('<---')
    appendtext = '<---' + appendtext
    appendtext = appendtext.rjust(148-len(text))
    return str(text + appendtext)

