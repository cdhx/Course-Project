import pymysql

def getCurrUser():
	filename = "user.txt"
	with open(filename,'r+') as f:
		user = f.read()
	return user

def setCurrUser(name):
	filename = "user.txt"
	with open(filename,'w') as f:
		f.write(name)

def changeUserImg(name,path):
	db = pymysql.connect("localhost","root","123456","test")
	cursor = db.cursor()
	sql = "update userinfo set path = '%s' where username = '%s'" % (path,name)
	cursor.execute(sql)
	db.commit()
	db.close()
