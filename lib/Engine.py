from jsbeautifier import beautify
from bs4 import BeautifulSoup, Comment
from faster_than_requests import get2str

class Engine:
    def __init__(self):
        pass

    def returnlink_fromhtml(self, s):
        l =  [t['href'] for t in s.find_all(href = True) if t]
        return l

    def returnsrc_fromimg(self, s):
        l = []
        for i in s.find_all('img'):
            if i.has_attr('src'): l.append(i['src'])
        return set(l)

    def returncomment_fromcomment(self, s):
        return set(s.find_all(string=lambda text: isinstance(text, Comment)))

    def returnhiddden_frominput(self, s):
        p = []
        l = s.find_all('input')
        for i in l:
            if i.has_attr('type') and i['type'] == "hidden" and i.has_attr('name'):
                p.append(i['name'])
        return p

    def returnexline_fromscript(self, s):
        e = [st for st in s.find_all('script') if st.has_attr('src')]
        return e

    def returnjs_fromjs(self, u):
        try:
            return beautify(get2str(u)).split('\n')
        except Exception as E:
            print(E,E.__class__)
        return []

    def returnjs_fromhtml(self, u):
        m = []
        try:
            r = get2str(u)
        except Exception as E:
            print(E,E.__class__)
            return [], []
        s = BeautifulSoup(r, 'html.parser')
        stext = filter(None, map(lambda st: beautify(st.string).split('\n'), filter(None, s.find_all("script"))))
        for st in stext:
            m.extend(st)
        return m, [self.returncomment_fromcomment(s), self.returnexline_fromscript(s), self.returnhiddden_frominput(s), self.returnlink_fromhtml(s), self.returnsrc_fromimg(s)]
