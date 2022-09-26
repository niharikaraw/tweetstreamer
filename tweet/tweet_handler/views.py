import json
import traceback
from django.views.decorators.csrf import csrf_exempt
import telegram
from django.http import HttpResponse
from emoji import emojize
from tweet_handler.cred import *
from tweet_handler.models import CustomUser, UserTweetMapping
from tweet_handler.utils import set_rules, show_subscriptions
# Create your views here.

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token= TOKEN)

@csrf_exempt
def home(request):
    try:
        body = json.loads(request.body)
        print(body)
        chat_id = body.get('message').get('chat').get('id')
        print(chat_id)
        message = body.get('message').get('text')
        reply_to_message_id = body.get('message').get('message_id')
        return_reply = 'Welcome to Tweet Bot! {} {}{}\n '.format(body.get('message').get('from').get('first_name'),body.get('message').get('from').get('last_name'),emojize(':grinning_face:'))
        if (chat_id != 5164975159):
            bot.send_message(chat_id=5164975159, text=('From: {} {}\nMessage: {}'.format(body.get('message').get('from').get('first_name'),body.get('message').get('from').get('last_name'),message)))
        
        if '/start' in message.lower():
            userobj = CustomUser(
                first_name = body.get('message').get('from').get('first_name'),
                last_name = body.get('message').get('from').get('last_name'),
                chat_id = chat_id
            )
            userobj.save()

        if 'show subscription' in message.lower():
            chat_id = chat_id
            return_reply = show_subscriptions(chat_id)

        if message.lower().startswith('subscribe'):
            topic = message.replace('subscribe','').replace('Subscribe','').strip()
            rules = set_rules(topic)
            print('&&&',rules,'----',type(rules))
            if 'errors' in rules:
                rule_id = rules.get('errors')[0].get('id')
                print(rule_id)
            else:
                rule_id = rules.get('data')[0].get('id')
                print(rule_id)
            
            
            subscription = UserTweetMapping.objects.filter(user=chat_id, rule_id=rule_id).exists()
            print(subscription)
            if subscription:
                try:
                    bot.send_message(chat_id=chat_id,text="You have already subscribed to @{}'s tweets.".format(topic),reply_to_message_id=reply_to_message_id)
                except Exception as e :
                    print (traceback.format_exc())
                    return_reply = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
                    return HttpResponse('okay')
            else:
                tweetmap = UserTweetMapping(
                    user_id = chat_id,
                    rule_id = rule_id,
                    rule_name = topic
                )
                tweetmap.save()
                try:
                    bot.send_message(chat_id=chat_id,text="You have successfully subscribed to @{}'s tweets.\nYou will get an update everytime they post a tweet!".format(topic),reply_to_message_id=reply_to_message_id)
                except Exception as e :
                    print (traceback.format_exc())
                    return_reply = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
                    return HttpResponse('okay')

        elif message.lower().startswith('unsubscribe'):
            topic = message.replace('unsubscribe','').replace('Unsubscribe','').strip()
            subscription = UserTweetMapping.objects.filter(user=chat_id, rule_name=topic)
            if not subscription:
                try:
                    bot.send_message(chat_id=chat_id,text="You have already unsubscribed from @{}'s tweets.".format(topic, topic),reply_to_message_id=reply_to_message_id)
                except Exception as e :
                    print (traceback.format_exc())
                    return_reply = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
                    return HttpResponse('okay')
            else:
                subscription.delete()
                try:
                    bot.send_message(chat_id=chat_id,text="You have successfully unsubscribed from @{}'s tweets.\nYou will not get any updates from @{}".format(topic, topic),reply_to_message_id=reply_to_message_id)
                except Exception as e :
                    print (traceback.format_exc())
                    return_reply = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
                    return HttpResponse('okay')

        else:
            try:
                bot.send_message(chat_id=chat_id,text=return_reply,reply_to_message_id=reply_to_message_id)
            except Exception as e :
                print (traceback.format_exc())
                return_reply = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
                return HttpResponse('okay')


    except Exception as e:
        print(traceback.format_exc())
        return_reply = 'Oops! Something went wrong{} Please provide a valid youtube link'.format(emojize(':slightly_frowning_face:'))
        return HttpResponse('okay')
    
    
        
    return HttpResponse("Hi")


''' {"data": {
        "id": "1571786669518618624",
        "text": "test tweet"
    },
    "matching_rules": [
        {
            "id": "1571785499026784257",
            "tag": ""
        }
    ]}'''
@csrf_exempt
def tweet_stream(request):
    payload = json.loads(request.body)
    rule_id = payload.get('matching_rules')[0].get('id')
    print(rule_id)
    users = UserTweetMapping.objects.filter(rule_id=rule_id)
    tweet = payload.get('data').get('text')
    if not users:
        return HttpResponse('no subscriptions')
    reply_text = "You have a new update from {}.\nTake a look!\n\n\n{}".format(users[0].rule_name, tweet)
    for user in users:
        try:
            bot.send_message(chat_id=user.user_id, text=reply_text)
        except Exception as e :
            print (traceback.format_exc())
            reply_text = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))

    return HttpResponse('Okay')
    



def set_webhook(request):
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   print(s)
   if s:
       return HttpResponse("webhook setup ok")
   else:
       return HttpResponse("webhook setup failed")


'''{"meta": {"sent": "2022-09-20T20:59:30.742Z", "summary": {"created": 0, "not_created": 1, "valid": 0, "invalid": 1}}, "errors": [{"value": "from:AWSCloudIndia", 
"id": "1572329540919398400", "title": "DuplicateRule", "type": "https://api.twitter.com/2/problems/duplicate-rules"}]}'''


