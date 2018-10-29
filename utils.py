import apiai
import json
from gnewsclient import gnewsclient


# api.ai client
APIAI_ACCESS_TOKEN = 'a795dcf8e6a24895b5e2ef8e65bc5d28'
ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)


def apiai_response(query, session_id):
    '''
    function to fetch api.ai response
    '''
    request = ai.text_request()
    request.lang = 'en'
    request.session_id = session_id
    request.query = query
    response = request.getresponse()
    return json.loads(response.read().decode('utf8'))


def parse_response(response):
    '''
    function to parse response and
    return intent and its parameters
    '''
    result = response['result']
    params = result.get('parameters')
    intent = result['metadata'].get('intentName')
    return intent, params


def fetch_reply(query, session_id):
    '''
    main function to fetch reply for chatbot and
    return a reply
    '''
    response = apiai_response(query, session_id)
    print('--------------')
    print(response)
    intent, params = parse_response(response)
    reply = response['result']['fulfillment']['messages'][0]['speech']        
                    
                    
    '''if response['result']['action'].startswith('smalltalk'):
        reply = response['result']['fulfillment']['speech']
    elif intent == 'show_news':
        reply = 'Ok, I will show you {} news!'.format(params.get('news'))
    else:
        reply = 'Sorry, I didn't understand!'''
                                            
    return reply


def get_welcome_elements():
    
    element=[{
             'title':'你好!我是vesta,你的私人点餐助手',
             'image_url':'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1200px-Good_Food_Display_-_NCI_Visuals_Online.jpg',
             'subtitle':'我是参加比赛的vesta，希望你喜欢我.',
             'default_action': {
             'type': 'web_url',
             'url': 'https://petersfancybrownhats.com/view?item=103',
             'webview_height_ratio': 'tall',
             },
             'buttons':[{
                        'type':'postback',
                        'title':'我要寻找餐厅',
                        'payload':'find'
                        },{
                        'type':'postback',
                        'title':'我已经想好吃什么了',
                        'payload':'eat'
                        }]}]
    
    return element

def get_welcome_elements1():
    titles=['我在香港岛','我在九龍西','我在九龍東','我在新界東','我在新界西']
    image_urls=['https://cdn09.dcfever.com/media/travel/destination/2017/04/2546_destination_banner.jpg','http://hm.people.com.cn/mediafile/201008/18/F201008180927283188427250.jpg','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5vd-QxzMh24fhnw4lbiBIm02c2uxab-gFa1UsGQv_yd0kfo2NXw','https://img-cdn.hopetrip.com.hk/2017/0420/20170420025907117.jpg','https://imgs.qunarzz.com/p/p61/201312/26/3475518e024049cf93835fbb.jpg_750x500_9d090012.jpg']
    element=[]
    for i in range(len(titles)):
    
        event={
                 'title':titles[i],
                 'image_url':image_urls[i],
                 
                 'default_action': {
                 'type': 'web_url',
                 'url': 'https://petersfancybrownhats.com/view?item=103',
                 'webview_height_ratio': 'tall',
                 },
                 'buttons':[{
                            'type':'postback',
                            'title': titles[i],
                            'payload':'find'
                            }]}
        element.append(event)
                            
    return element


def pay_load_adapter(payload):
    if payload=="find":
        elements=get_welcome_elements1()
        return elements
        
        
