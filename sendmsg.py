import re
import base64
import urllib.request
import random
import numpy as np

Msg_list=['0','1','10']
repMsg={}
try:
    remembered_word=np.load('QA.npy',allow_pickle=True).item()
except FileNotFoundError:
    remembered_word={}
cur_word=''
cur_answer=''
cur_word_guessed=''
cur_char_guessed=[]
cur_state=0
error_times=0
game_finish_state=0
p_count=0
EnWords=open('EnWords.csv','r', encoding = 'utf8')
EnWords_lines=EnWords.readlines()


def update_dict(message):
    check_haha(message)
    #print('Haha checked.')
    check_greet(message)
    #print('Greet checked.')
    check_meme(message)
    #print('Meme checked.')
    check_setu(message)
    #print('Setu checked.')
    #check_repeatmachine(message)
    #print('Repeat machine checked.')
    check_answers(message)
    #print('Answers checked.')
    check_sheshe(message)
    #print('Sheshe checked.')
    hanged_man(message)
    remember(message)
    
def getData (data_in):
    try:
        message=data_in['message'][0]['data'].get('text')
        #print(message)
        record_msg(message)
        #print(Msg_list)
    except TypeError:
        message=data_in['message'][0]['data'].get('id')
        record_msg(message)
    message_type=data_in['message_type']
    if message_type=='group':
        data_out={
            'group_id': getID_group(data_in),
            'message': getMessage(data_in),
            'auto_escape': False
        } 
    elif message_type=='private':
        data_out={
            'user_id': getID_private(data_in),
            'message': getMessage(data_in),
            'auto_escape': False
        } 
    return data_out

def getID_private(data_in):
    if 'user_id' in data_in:
        return int(data_in['user_id'])
    else:
        return 0

def getID_group(data_in):
    if 'group_id' in data_in:
        return int(data_in['group_id'])
    else:
        return 0

def getMessage(data_in):
    try:
        message=data_in['message'][0]['data'].get('text')
        repMsg.clear()
        update_dict(message)
        try:
            return repMsg[message]
        except KeyError:
            return None
    except TypeError:
        message=data_in['message'][0]['data']['id']
        #if message=='13': return '[CQ:face,id=107]'
        #elif message=='107': return '[CQ:face,id=13]'
        return None

def getImage(key):
    with open('test.jpg','rb') as imageFile:
        codedImage=base64.b64encode(imageFile.read())
        return codedImage

def get_konachan_url():
    random_url='https://konachan.net/post?tags=order%3Arandom'
    html_r=urllib.request.urlopen(random_url).read()
    html_r=html_r.decode("utf-8")
    pat='<li style="width:.*?;" id="p(.*?)"'
    inputnum=re.search(pat,html_r).groups(1)[0]
    if inputnum==None: 
        return '运气不好呢亲爱的'
    else:
        return 'konachan.net/post/browse#{}'.format(inputnum)

def record_msg(message):
    Msg_list.append(message)
    if (len(Msg_list)>=30): Msg_list.pop(0)

def check_meme(message):
    repMsg['zaima？']='buzai'
    repMsg['kkp？']='guna'
    repMsg['nmd']='你再骂？'
    repMsg['啊']='吵死了！'
    repMsg['哦']='口我'
    repMsg['奥']='安静'
    repMsg['?']='？'
    repMsg['？']='？'
    repMsg['???']='？'
    repMsg['？？？']='？'
    '''
    '''

def check_haha(message):
    hahacount=0
    for character in message:
        if character=='哈':
            hahacount+=1
    if hahacount in range(1,3):
        repMsg[message]='你笑你🐎呢臭dd？'
    elif hahacount in range(3,8):
        repMsg[message]='哈哈哈哈哈哈哈哈哈'
    elif hahacount>=8:
        repMsg[message]='谢谢，有被笑到'
    
def check_greet(message):
    greeting_msg_list=[
        '该起了',
        '早上好',
        '早！',
        '？',
        '晚上好',
        '给娘娘请安',
        'aloha!',
        '来点色图？'
    ]
    goodbye_msg_list=[
        '晚安',
        '再见',
        '好梦',
        'S S D',
        'zzZzzZZ',
        '这才几点？',
        '好的亲爱的，我去陪别的男人',
        '柜子动了我不玩了'
    ]
    morning_greeting=random.choice(greeting_msg_list)
    night_greeting=random.choice(goodbye_msg_list)
    repMsg['早']=morning_greeting
    repMsg['早！']=morning_greeting
    repMsg['早上好']=morning_greeting
    repMsg['早上好！']=morning_greeting
    repMsg['你好']=morning_greeting
    repMsg['88']=night_greeting
    repMsg['再见']=night_greeting
    repMsg['我下了']=night_greeting
    repMsg['下了']=night_greeting
    repMsg['拜拜']=night_greeting
    repMsg['晚安']=night_greeting
    repMsg['晚安好梦']=night_greeting
    repMsg['晚安！']=night_greeting
    repMsg['晚好']=night_greeting
    repMsg['晚安好梦!']=night_greeting
    repMsg['我溜了']=night_greeting
    repMsg['溜了']=night_greeting
    '''
    '''

def check_setu(message):
    if ('色图' in message) or ('再来点' in message):
        repMsg[message]=get_konachan_url()

def check_repeatmachine(message):
    #print(Msg_list)
    if Msg_list[-3]==message:
        return
    if Msg_list[-2]==message:
        repMsg[message]=message

def get_random_word():
    target_line=EnWords_lines[random.randint(1,103977)]
    target_word=re.match('\"(.*?)\",',target_line).groups(1)[0]
    answer=re.search(',\"(.*?)\"',target_line).groups(1)[0]
    return (answer,target_word)

def hanged_man(message):
    global cur_state
    global cur_word
    global cur_word_guessed
    global cur_char_guessed
    global cur_answer
    global error_times
    global game_finish_state
    global p_count
    hp=6
    if message=='#吊':
        cur_word=''
        cur_answer=''
        cur_word_guessed=''
        cur_char_guessed=[]
        cur_state=0
        error_times=0
        game_finish_state=0
        p_count=0
        showed_word=''
        (cur_answer,cur_word)=get_random_word()
        cur_word_guessed=cur_word
        for i in range(0,len(cur_word)): showed_word+='*'
        showed_word+='\n开始了！'
        repMsg[message]=showed_word
        cur_state=1
        error_times=0
        print(cur_word)
    elif cur_state==1:
        if message[0]=='+':
            if game_finish_state==1:
                p_count_str=''
                for i in range(1,p_count):
                    p_count_str+='+'
                game_over_msg_list=[
                    '上一轮游戏已经结束了，亲爱的',
                    '+你🐎呢？没看到游戏结束了？',
                    '还+？你🐎出门必买不到口罩',
                ]
                if p_count>=3:
                    repMsg[message]=p_count_str
                else:
                    repMsg[message]=game_over_msg_list[p_count]
                p_count+=1
                return
            cur_guess=message[1:]
            temp_guess=''
            for letter in cur_guess:
                temp_guess+='*'
            sub_result=re.sub(cur_guess,temp_guess,cur_word_guessed)
            cur_char_guessed.append(cur_guess)
            showed_word=''
            for i in range(0,len(cur_word)):
                if sub_result[i]=='*':
                    showed_word+=cur_word[i]
                else:
                    showed_word+='*'
            repMsg[message]=showed_word
            if sub_result==cur_word_guessed:
                repMsg[message]+='\n没匹配到pwp'
                error_times+=1
                #print('Not contained.')
                #未匹配
            else:
                print(showed_word)
                count=0
                for char in sub_result:
                    if char=='*':
                        count+=1
                if count==len(cur_word_guessed):
                    repMsg[message]+='\n{}\n你赢了qwq'.format(cur_answer)
                    game_finish_state=1
                    return
                    #print('Finished')
                    #结束游戏
            repMsg[message]+='\n已猜字符:{}'.format(', '.join(sorted(cur_char_guessed)))
            repMsg[message]+='\n剩余次数:{}'.format(hp-error_times)
            cur_word_guessed=sub_result
            if error_times>=hp or cur_guess=='投了':
                repMsg[message]+='\n你输了qwq\n正确答案是: {} {}'.format(cur_word,cur_answer)
                game_finish_state=1

def check_answers(message):
    search_result=re.search('([我|你|您].*?)[嘛|吗|呢|了|么|？|！]',message)
    if search_result!=None:
        repMsg[message]=search_result.groups(1)[0]
        #print(message[-2])
        end_character_list=['嘛','吗','呢','了','么']
        if message[0]=='你':
            if message[1]=='们':
                repMsg[message]='我'+repMsg[message][2:]
            else:
                repMsg[message]='我'+repMsg[message][1:]
        if search_result[0]=='我' and (search_result[1]!='们' or search_result[1]!='的'):
            repMsg[message]='我也'+repMsg[message][1:]
        if message[-1] in end_character_list:
            #print(message)
            repMsg[message]=repMsg[message][0:len(repMsg[message])]
        if message[-2] in end_character_list:
            #print(message)
            repMsg[message]=repMsg[message][0:len(repMsg[message])-1]
            #print(repMsg[message])
        if message[-1]=='了' or message[-2]=='了':
            repMsg[message]+='了'
        if message[-1]=='！':
            repMsg[message]+='！！'

def check_sheshe(message):
    sheshe_msg_list=[
        '已经 射♥爆♥了',
        '不要啊已经 塞 满 了 ♥',
        '让 我 康 康 你 的 枪 ♂ 法',
        'Y E S, S ♂ I ♂ R',
        'L E T\'s C♥S♥G♥O '
    ]
    sheshe=random.choice(sheshe_msg_list)
    if '射' in message:
        repMsg[message]=sheshe
    elif '🐍' in message:
        repMsg[message]=sheshe
    '''
    if '来' in message:
        repMsg[message]='马上到'
    '''
    if '一把' in message:
        repMsg[message]='阳痿才射一把'
    if 'gay' in message:
        repMsg[message]='I\'m Gay, too.'

def remember(message):
    global repMsg
    repMsg.update(remembered_word)
    try:
        match_msg=re.match('问：(.*?)\s*答：(.*?)$',message)
        remembered_word[match_msg.groups(1)[0]]=match_msg.groups(1)[1]
        np.save('QA.npy',remembered_word)
        repMsg[message]='记住了'
    except AttributeError:
        return