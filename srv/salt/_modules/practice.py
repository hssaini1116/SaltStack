from  slacker import Slacker


def slackNotification():

    slack = Slacker('xoxp-226792929462-225250171360-260800059796-84e42e6ad4ccd7376fda3aa95b3c3fb3')

    return slack



def call():
    s = slackNotification()
    s.chat.post_message('#devops', "message is working")
