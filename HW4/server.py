from flask import Flask,request,render_template
import sqlite3

talkMsg={}#聊天内容保存到这个字典中
#取走对应聊天记录后，请对应的内容，dict.pop()函数完成

webName=[]
talkRoom=Flask(__name__)
dbConn=sqlite3.connect('userData.db')
sql="""select * from user"""
dbRec=dbConn.execute(sql)

ls=list(dbRec)
dic={} #{userName:[ID,password,friends_ID]}
for everyRec in ls:
    webName.append(everyRec[1]) #everyRec是元组(ID,userName,password,friends_ID)
    dic[everyRec[1]]=[everyRec[0],everyRec[2],everyRec[3]]

dbConn.close()


@talkRoom.route('/')
def root():
    return render_template('root.html',Msg='欢迎来到在线聊天室！')

@talkRoom.route('/talk',methods=('post',))
def talk():
    print(request.form)
    name=request.form["netName"].strip()
    pwd=request.form['pwd1']
    return talkRoom.send_static_file('Talk.html')

@talkRoom.route('/check_login',methods=('post',))
def check_login():
    print('check_login',request.form)
    name=request.form["netName"].strip()
    pwd=request.form['pwd1']
    if name in webName and dic[name][1]==pwd:
        return "1"
    else:
        return "0"
    

@talkRoom.route('/register')
def register():
    return talkRoom.send_static_file('Register.html')

@talkRoom.route('/Register_check',methods=("post",))
def Register_check():
    netName=request.form["netName"].strip()
    pwd1=request.form["pwd1"]
    pwd2=request.form["pwd2"]
    if netName not in webName:
        webName.append(netName)
        statusMsg="恭喜您！注册成功！"
    return talkRoom.send_static_file('Register.html')

@talkRoom.route('/sendMsg',methods=('get',)) #从服务端发送信息到网页端
def sendMsg():
    thisSide=request.args['thisSide'] #用户自身
    thatSide=request.args['thatSide'] #交谈的另一方
    FromToSide=f'{thatSide}_To_{thisSide}' #上述字典talkMsg的键（key）
    rtnMsg='' #要返回到网页端的字符串（也就是要处理的信息）
    if FromToSide in talkMsg:
        for everyMsg in talkMsg[FromToSide]: #可能有多条信息尚待处理
            rtnMsg+="<div class='thatSide'>TA说："+everyMsg+"</div>"
        talkMsg.pop(FromToSide) #取走后，删除数据
    return rtnMsg

@talkRoom.route('/saveMsg',methods=('get',))
def saveMsg():
    fromSide=request.args['fromSide'] #信息发送用户，记为A
    toSide=request.args['toSide'] #信息接收用户，记为B
    Msg=request.args['Msg'] #信息
    FromToSide=f'{fromSide}_To_{toSide}'
    if FromToSide in talkMsg: #talkMsg中有A发给B的信息还未处理
        talkMsg[FromToSide].append(Msg)
    else: 
        talkMsg[FromToSide]=[Msg]
    return 'Message saved successfully!'

@talkRoom.route('/checkName',methods=('post',))
def checkName():
    name=request.form['netName']
    if name in webName: return '0'
    else: return '1'

if __name__=="__main__":
    talkRoom.run(port=80,debug=True)

