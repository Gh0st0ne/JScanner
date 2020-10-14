from jsbeautifier import beautify
from bs4 import BeautifulSoup, Comment
from faster_than_requests import get2str

class Engine:
    def __init__(self):
        pass

    def returncomment_fromhtml(self, r):
        s = BeautifulSoup(r, 'html.parser')
        c = s.find_all(string=lambda text: isinstance(text, Comment))
        return set(c)

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
        l = s.find_all('script')
        for st in l:
            if st.has_attr('src'):
                e.append(st)
        return e

    def returnjs_fromjs(self, u):
        try:
            r = get2str(u)
        except Exception as E:
            print(E,E.__class__)
            return []
        t = beautify(r).split('\n')
        return t

    def returnjs_fromhtml(self, u):
        m = []
        try:
            r = get2str(u)
        except Exception as E:
            print(E,E.__class__)
            return [], []
        s = BeautifulSoup(r, 'html.parser')
        ss = s.find_all("script")
        for st in ss:
            if st != None:
                t = beautify(st.string).split('\n')
                if t: m.extend(t)
        return m, [self.returncomment_fromhtml(r), self.return_exlinetag_fromhtml(r), self.returnhidden_parameter(r)]
