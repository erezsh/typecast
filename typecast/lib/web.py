from ..typecast import typecast_decor, CastError, Typecast, autocast

class HTML(metaclass=Typecast):

    def __init__(self, html):
        self.html = html

    def __repr__(self):
        return "HTML(%r)" % self.html

    def from__str(cls, s):
        assert isinstance(s, str), s
        return cls(s.replace('<', '&lt;').replace('>', '&gt;'))

    def to__str(self, str):
        return str(self.html.replace('&gt;', '>').replace('&lt;', '<'))

    def from__list(cls, l):
        return '<ol>\n%s\n</ol>' % '\n'.join('<li>%s</li>' % (n >> cls).html for n in l)

    def from__set(cls, s):
        return '<ul>\n%s\n</ul>' % '\n'.join('<li>%s</li>' % (n >> cls).html for n in s)

    def from__dict(cls, d):
        return '<dl>\n%s\n</dl>' % '\n'.join('<dt>%s</dt><dd>%s</dd>' % ((k>>cls).html, (v>>cls).html) for k,v in d.items())

