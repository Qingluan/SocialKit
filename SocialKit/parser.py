import re
from pyquery import PyQuery as _pq
from bs4 import BeautifulSoup as _BS
from lxml.etree import  XMLSyntaxError

class XmlParser:
    tager = re.compile(r'\<[\w\W].+?\>')

    def __init__(self, *args, **kargs):
        self.encoding = 'utf8'
        self._text = None
        if 'encoding' in kargs:
            self.encoding = kargs['encoding']

        try:
            self._raw = _pq(*args, **kargs)
            self.handler = 'pq'
        except XMLSyntaxError as e:
            self._raw = _BS(*args, features='lxml',**kargs)
            self.handler = 'bs'
    
    def __repr__(self):
        if self.handler == "bs":
            return self._raw.select("title")[0].string
        return self._raw("title").text()
        

    def __call__(self, st):
        if self.handler =='pq':
            return self._raw(st)
        elif self.handler == 'bs':
            return self._raw.select(st)

    def html(self, encoding='utf8'):
        if self.handler =='pq':
            return self._raw.html()
        elif self.handler == 'bs':
            return self._raw.decode(eventual_encoding=encoding)

    def remove(self, tag):
        if self.handler == "bs":
            [i.replaceWith("") for i in self._raw.select(tag)]
        else:
            self._raw(tag).remove()

    @property
    def text(self):
        self.remove("script")
        self.remove("style")
        if self.handler == "bs":
            return XmlParser.tager.sub('', self._raw.getText())
        else:
            return XmlParser.tager.sub('', self._raw.text())
