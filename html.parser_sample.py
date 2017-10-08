from HTMLParser import HTMLParser

class MYParser(HTMLParser):
    def handle_decl(self, decl):
        HTMLParser.handle_decl(self,decl)
        print('decl %s' %decl)

    def handle_starttag(self, tag, attrs):
        HTMLParser.handle_starttag(self,tag,attrs)
        print('<' + tag + '>')

    def handle_endtag(self, tag):
        HTMLParser.handle_starttag(self,tag)
        print('<' + tag + '>')

    def handle_data(self, data):
        HTMLParser.handle_data(self,data)
        print('data %s' %data)

    def handle_startendtag(self, tag, attrs):
        HTMLParser.handle_startendtag(self,tag,attrs)
        print

    def handle_comment(self, data):
        HTMLParser.handle_comment(self,data)
        print('data %s' %data)

    def close(self):
        HTMLParser.close(self)
        print('Close')

demo = MYParser()
demo.feed(open('sample.html').read())
demo.close()