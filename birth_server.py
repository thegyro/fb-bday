import webapp2
import jinja2
import os
import urllib2
import urllib
import json
from birthday import Facebook_Actions

class App_Details:
    APP_ID = '<Your App Id Here>'
    APP_SECRET = '<Your App Secret Here>'
    ACCESS_TOKEN = ''

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render(self,template,**params):
        template = jinja2_env.get_template(template)
        self.write(template.render(params))


class Main(Handler):
    def get(self):
        self.render('front.html',message='hi')

    def post(self):
        if self.request.get('uname') != 'Srinath':
            self.render('front.html',error='Only for Srinath')

        else:
            redirect_uri = 'http://localhost:8080/token'
            scope = 'user_birthday,user_friends,user_location,user_status,publish_stream,read_stream,publish_actions,export_stream,status_update'
            APP_ID = App_Details.APP_ID
            query_param = {'client_id':APP_ID,'redirect_uri':redirect_uri,'scope': scope}
            query = urllib.urlencode(query_param)
            facebook_url = 'https://www.facebook.com/dialog/oauth?%s' % query
            self.redirect(facebook_url)
        

class Token(Handler):
    def get(self):
        code = self.request.get('code')
        base_url = 'https://graph.facebook.com/'
        redirect_uri = 'http://localhost:8080/token'
        APP_ID = App_Details.APP_ID
        APP_SECRET = App_Details.APP_SECRET
        query_param = {'client_id':APP_ID,'redirect_uri':redirect_uri,'client_secret': APP_SECRET,'code':code}
        data = urllib.urlencode(query_param)
        try:
            param_url = 'oauth/access_token?%s' % data
            response  =  urllib2.urlopen(base_url + param_url)
            App_Details.ACCESS_TOKEN = response.read().split('&')[0].lstrip('access_token=')
            self.redirect('/birthday')

        except IOError as err:
            self.response.out.write(str(err))
            
class Birthday(Handler,App_Details):
    def get(self):
        username = 'srinath.rajagopalan.94'
        basic_url = 'https://graph.facebook.com/'
        f = Facebook_Actions(username,basic_url,self.ACCESS_TOKEN)
        f.comment_on_posts(['2014-02-12','2014-02-13'])
        self.render('back.html')
        

def main():
    template_dir = os.path.join(os.path.dirname(__file__),'templates')
    jinja2_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir),autoescape = True)
    app = webapp2.WSGIApplication([('/',Main),('/token',Token),('/birthday',Birthday)])


if __name__ == "__main__" :
    main()
