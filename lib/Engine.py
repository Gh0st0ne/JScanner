from jsbeautifier import beautify
from bs4 import BeautifulSoup, Comment
from faster_than_requests import get2str

class Engine:
    def __init__(self):
        pass

    def returncomment_fromhtml(self, r):
        s = BeautifulSoup(r, 'html.parser')
        return set(s.find_all(string=lambda text: isinstance(text, Comment)))

    def returnhidden_parameter(self, r):
        p = []
        s = BeautifulSoup(r, 'html.parser')
        l = s.find_all('input')
        for i in l:
            if i.has_attr('type') and i['type'] == "hidden" and i.has_attr('name'):
                p.append(i['name'])
        return p

    def return_exlinetag_fromhtml(self, r):
        e = []
        s = BeautifulSoup(r, 'html.parser')
        [e.append(st) for st in s.find_all('script') if st.has_attr('src')]
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
        ss = filter(None, map(lambda st: beautify(st.string).split('\n'), filter(None, s.find_all("script"))))
        for st in ss:
            m.extend(st)
        return m, [self.returncomment_fromhtml(r), self.return_exlinetag_fromhtml(r), self.returnhidden_parameter(r)]
