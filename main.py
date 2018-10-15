import pymysql
from flask import Flask,render_template,request   
import traceback  
import time
from userManage import getCurrUser,setCurrUser,changeUserImg


#传递根目录
app = Flask(__name__)

#主界面
@app.route('/')
def home():
	return render_template('index.html')

#管理员登陆页面
@app.route('/admin')
def admin():
	return render_template('admin.html')

#普通用户登陆界面
@app.route('/login')
def login():
	return render_template('login.html')

#注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')

#设置响应头
def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp 

#获取注册请求及处理,把用户名和密码注册到数据库中
@app.route('/registuser')
def getRigistRequest():
    db = pymysql.connect("localhost","root","123456","test" )
    cursor = db.cursor()

    checkSql = "select * from userinfo where username='%s'" % request.args.get('user')
    cursor.execute(checkSql)
    result = cursor.fetchall() 
    db.commit()
    if len(result) == 1:
    	return render_template('alert.html')

    sql = "insert into userinfo value('%s','%s',%d,'%s')" % (request.args.get('user'),request.args.get('password'),1000,"../static/default.jpg")
    cursor.execute(sql)
    db.commit()
    db.close()
    return render_template('login.html') 
    

#获取登录参数及处理，查询用户名及密码是否匹配及存在
@app.route('/logincheck')
def getLoginRequest():
    db = pymysql.connect("localhost","root","123456","test" )
    cursor = db.cursor()
    sql = "select path from userinfo where username='%s' and password ='%s'" % (request.args.get('user'),request.args.get('password'))
    cursor.execute(sql)
    result = cursor.fetchall()
    db.commit()
    db.close()
    if len(result)==1:
        setCurrUser(request.args.get('user'))
        return render_template('loginSucceed.html',username = request.args.get('user'),path = result[0][-1])
    else:
        return '用户名或密码不正确'

@app.route('/search')
def search():
	return render_template('search.html')

#用户更改头像
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    userName = getCurrUser()
    f.save(r'static/'+ userName + "." + f.filename.split(".")[-1])
    newPath = "../static/" + userName + "." + f.filename.split(".")[-1]
    changeUserImg(userName,newPath)
    return render_template("loginSucceed.html",username = userName,path = newPath)
#使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
#启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
    app.run(debug=True)