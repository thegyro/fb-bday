def check_message_birthday(message):
    #Should write a better condition for checking whether a Facebook friend is wishing me for my birthday.The one below is rough and ugly.
    birthday = ['bday','birthday',"b'day",'Birthday',"B'day",'day']
    happy = ['happy','Happy','happie','HAPPY']
    
    if message:
        for h in happy:
            for b in birthday:
                if h in message and b in message:
                    return True
    return False


def check_comment_like(post):
    c_flag = False
    l_flag = False
    
    comment_data = post.get('comments')
    if comment_data:
        comments = comment_data.get('data')
        if comments:
            for comment in comments:
                if comment.get('from').get('name') == 'Srinath Rajagopalan':
                    c_flag = True
                    break
                    
    like_data = post.get('likes')
    if like_data:
        likes = like_data.get('data')
        if likes:
            for like in likes:
                if like.get('name') == 'Srinath Rajagopalan':
                    l_flag = True
                    break

    return (c_flag,l_flag)
