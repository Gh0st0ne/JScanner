from termcolor import colored

from lib.Globals import ColorObj

def banner():
    from pyfiglet import print_figlet
    print_figlet('JScanner', font='larry3d', colors='BLUE')
    print(colored('JScanner: Find secrets and vulnerabilites!', color='red', attrs=['bold']))

def starter(argv):
    from sys import stdin
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

def output_writer(filename, to_write, filepath=None):
    from lib.PathFunctions import PathFunction
    from lib.Globals import tag_dict
    if filepath:
        output_file = open(path_fn.slasher(filepath) + filename + '.jscan', 'a')
    else:
        output_file = open(filename, 'a')
    path_fn = PathFunction()
    for jsresults in to_write:
        jarray = sorted(jsresults.result(), key=lambda x: x[1])
        for jsresult in jarray:
            output_file.write(jsresult[0])
        #for tag in tag_dict.items():
            #for jsresult in jarray:
                #print(f"JR1: {jsresult[1]}, Tag0: {tag[0]}")
                #if not tag[1] and tag[0] == jsresult[1]:
                #    output_file.write(f"{tag[0]}:\t")
                #    tag_dict[tag[0]] = True
                #else:
                #    print("Writing content", end=" ")
                #    print(f"Jresult[0] {jsresult[0]}")
                #    output_file.write(jsresult[0])
                #else:
                #    print(f"T0: {tag[0]},J1: {jsresult[1]}")
            #output_file.write('\n')
    output_file.close()

def manage_output(line, color=None) -> tuple:
    if '<-' in line:
        text, appendtext = line.split('<---')
        appendtext = '<---' + appendtext
        appendtext = appendtext.rjust(148-len(text))
        text = text + appendtext
    else:
        text = line
    if not color:
        return text
    elif color:
        return text
        joinedtext = text.lower()
        newtext = joinedtext.split(color.lower())
        newtext = newtext[0] + colored(color, color='red') + newtext[1]
        return newtext + appendtext

def shannon_entropy(data, iterator):
    from math import log
    if not data:
        return 0
    entropy = 0
    for val in iterator:
        p_x = float(data.count(val))/len(data)
        if p_x > 0:
            entropy += - p_x * log(p_x, 2)
    return float(entropy)
