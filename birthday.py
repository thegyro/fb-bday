import urllib2
import urllib
import json
import time
import utils

class Facebook_Actions:
    def __init__(self,username,basic_url,access_token):
        self.username = username
        self.access_token = access_token
        self.basic_url = basic_url
        
    def get_user_id(self):
        request_url = self.basic_url + self.username
        try:
            response = urllib2.urlopen(request_url)
            user_data = json.loads(response.read())
            return str(user_data['id'])

        except IOError as err:
            print str(err)


    def get_posts_date(self,dates,limit):
        user_id = self.get_user_id()
        request_url = self.basic_url + user_id + '/feed/?limit=%s&access_token=%s' % (str(limit),self.access_token)

        try:
            response = urllib2.urlopen(request_url)
            response_json = json.loads(response.read())
            posts = response_json['data']
            posts_date = []
            for post in posts:
                message = post.get('message')
                if utils.check_message_birthday(message) and (dates[0] in post['created_time'] or dates[1] in post['created_time']):
                    posts_date.append(post)

        except IOError as err:
            print str(err)
        
        finally:
            return posts_date

    def comment_on_posts(self,dates):
        user_id = self.get_user_id()
        posts = self.get_posts_date(dates,100)
        for post in posts:
            post_id = post.get('id')
            message = post.get('message')
            from_user = post.get('from').get('name')


            c_flag,l_flag = utils.check_comment_like(post)
            if not c_flag:
                request_url = self.basic_url + post_id + '/comments?access_token=%s' % self.access_token
                comment_data = urllib.urlencode({'message':'Thanks %s!' % from_user.split()[0]})
                print 'Commenting on Post from %s' % from_user
                try:
                    urllib2.urlopen(request_url,comment_data)
                    print 'Comment Successful! \n'

                except IOError as err:
                    print str(err)
                    print 'Comment Failed \n'

            if not l_flag:
                request_url = self.basic_url + post_id + '/likes?access_token=%s' % self.access_token
                print 'Liking Post from %s' % from_user
                try:
                    urllib2.urlopen(request_url,data='')
                    print 'Like Successful! \n'
                except IOError as err:
                    print str(err)
                    print 'Like Failed! \n'\
