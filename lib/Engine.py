from jsbeautifier import beautify
from bs4 import BeautifulSoup, Comment
from faster_than_requests import get2str

class Engine:
    def __init__(self):
        pass

    def returncomment_fromhtml(self, jsresponse):
        js_soup = BeautifulSoup(jsresponse, 'html.parser')
        comments_list = js_soup.find_all(string=lambda text: isinstance(text, Comment))
        return set(comments_list)

    def returnhidden_parameter(self, jsresponse):
        input_parameters = []
        js_soup = BeautifulSoup(jsresponse, 'html.parser')
        input_list = js_soup.find_all('input')
        for input_tag in input_list:
            if input_tag.has_attr('type') and input_tag['type'] == "hidden":
                if input_tag.has_attr('name'):
                    input_parameters.append(input_tag['name'])
        return input_parameters

    def return_exlinetag_fromhtml(self, jsresponse):
        exline_tags = []
        js_soup = BeautifulSoup(jsresponse, 'html.parser')
        scripts_list = js_soup.find_all('script')
        for script_tag in scripts_list:
            if script_tag.has_attr('src'):
                exline_tags.append(script_tag)
        return exline_tags

    def returnjs_fromjs(self, jsurl):
        try:
            jsresponse = get2str(jsurl)
        except Exception as E:
            print(E,E.__class__)
            return []
        jstext = beautify(jsresponse).split('\n')
        return jstext

    def returnjs_fromhtml(self, jsurl):
        mega_text = []
        try:
            jsresponse = get2str(jsurl)
        except Exception as E:
            print(E,E.__class__)
            return [], []
        js_soup = BeautifulSoup(jsresponse, 'html.parser')
        script_tags = js_soup.find_all("script")
        for script_tag in script_tags:
            if script_tag != None:
                jstext = beautify(script_tag.string).split('\n')
                if jstext:
                    mega_text.extend(jstext)
        return mega_text, [self.returncomment_fromhtml(jsresponse), self.return_exlinetag_fromhtml(jsresponse), self.returnhidden_parameter(jsresponse)]
