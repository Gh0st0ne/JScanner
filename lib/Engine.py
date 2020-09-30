from bs4 import BeautifulSoup
from jsbeautifier import beautify
from faster_than_requests import get2str

class Engine:
    def __init__(self):
        pass

    def returnjs_fromjs(self, jsurl):
        try:
            jsresponse = get2str(jsurl)
        except Exception as E:
            print(E,E.__class__)
        jstext = beautify(jsresponse).split('\n')
        return jstext

    def returnjs_fromhtml(self, jsurl):
        mega_text = []
        try:
            jsresponse = get2str(jsurl)
        except Exception as E:
            print(E,E.__class__)
        js_soup = BeautifulSoup(jsresponse, 'html.parser')
        script_tags = js_soup.find_all("script")
        for script_tag in script_tags:
            if script_tag != None:
                jstext = beautify(script_tag.string).split('\n')
                if jstext:
                    mega_text.extend(jstext)
        return mega_text
