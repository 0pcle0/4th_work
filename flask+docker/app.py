from flask import Flask, request, redirect, render_template, session, flash, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = "My_Key"
app.config["SECRET_KEY"]="ABCD"



userID=1
newID = 1
writ = []

user = []


db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     passwd='noneage0522!',
                     db='notice',
                     charset='utf8')

with db.cursor() as cur:
    sql = ''' CREATE TABLE NOTICE1(
              ID INT NOT NULL,
              TITLE CHAR(40) NOT NULL,
              BODY CHAR(255) NOT NULL,
              USER CHAR(15) NOT NULL,
              DATE CHAR(40) NOT NULL,
              PW INT,
              FILE CHAR(100),
              PRIMARY KEY(ID)
              )ENGINE=INNODB;'''
    
    cur.execute(sql)
    db.commit()


sql = '''INSERT INTO notice1 (id, title, body, user, date) VALUES (%s, %s, %s, %s, %s)'''


with db.cursor() as cur:
    for arti in writ:
        sql = '''INSERT INTO notice1 (id, title, body, user, date) VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(sql,(arti['id'], arti['title'], arti['body'],arti['user'], arti['date']))
        db.commit()


with db.cursor() as cur:
    sql = ''' CREATE TABLE USER(
              id INT NOT NULL,
              NAME CHAR(10) NOT NULL,
              USER CHAR(40) NOT NULL,
              PW CHAR(255) NOT NULL,
              TEL CHAR(20) NOT NULL,
              GEN CHAR(10) NOT NULL,
              AGE INT NOT NULL,
              PRIMARY KEY(id)
              )ENGINE=INNODB;'''
    
    cur.execute(sql)
    db.commit()


@app.route('/logout')
def logout():
    session.pop('id', None)
    url = '/login/'
    return redirect(url)


@app.route('/')
def webf():
    return render_template('main.html', writ=writ)



@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        ID1 = str(request.form['ID1'])
        PW1 = str(request.form['PW1'])
        if ID1 == '' or PW1 =='':
            url = '/login/'
            return redirect(url)
        else:
            for i in user:
                if ID1 == i['USER']:
                    if PW1 == i['PW']:
                        session['id']=ID1
                        url = '/'
                        return redirect(url)
                    else:
                        flash("아이디와 비밀번호를 확인해주세요.")
                        url = '/login/'
                        return redirect(url)
                else:
                    flash("등록되지 않은 아이디입니다.")
                    url = '/login/'
                    return redirect(url)
            else:
                url = '/login/'
                return redirect(url)



@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        global userID
        name = str(request.form['name'])
        username = str(request.form['username'])
        pw = str(request.form['password'])
        tel = str(request.form['tel'])
        gender = str(request.form['gender'])
        age = str(request.form['age'])
        newuser = {'id':userID, 'NAME':name, 'USER':username, 'PW':pw, 'TEL':tel, 'GEN':gender, 'AGE':age}
        if newuser['USER']=='' or newuser['PW']=='' or newuser['GEN']=='' or newuser['AGE']=='' or newuser['TEL']=='' or newuser['NAME']=='':
            url='/register/'
            return redirect(url)
        with db.cursor() as cur:
            sql = '''INSERT INTO user (id, name, user, pw, tel, gen, age) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(sql,(newuser['id'], newuser['NAME'], newuser['USER'], newuser['PW'], newuser['TEL'], newuser['GEN'], newuser['AGE']))
            db.commit()
        userID += 1
        user.append(newuser)
        url = '/login/'
        return redirect(url)


@app.route('/findid/', methods=['GET','POST'])
def findid():
    if request.method=='GET':
        return render_template('findid.html')
    elif request.method=='POST':
        name = request.form['name']
        tel = request.form['tel']
        if name == '' or tel =='':
            url = '/login/'
            return redirect(url)
        else:
            for i in user:
                if name == i['NAME']:
                    if tel == i['TEL']:
                        username=i['USER']
                        return render_template('foundid.html', username=username)
                    else:
                        url = '/login/'
                        return redirect(url)
                else:
                    url = '/login/'
                    return redirect(url)
            else:
                url = '/login/'
                return redirect(url)



@app.route('/findpw/', methods=['GET','POST'])
def findpw():
    if request.method=='GET':
        return render_template('findpw.html')
    elif request.method=='POST':
        username = request.form['username']
        tel = request.form['tel']
        if username == '' or tel =='':
            url = '/login/'
            return redirect(url)
        else:
            for i in user:
                if username == i['NAME']:
                    if tel == i['TEL']:
                        id = i['id']
                        url =  '/newpw/'+ str(id)
                        return redirect(url)
                
                    else:
                        url = '/login/'
                        return redirect(url)
                else:
                    url = '/login/'
                    return redirect(url)
            else:
                url = '/login/'
                return redirect(url)



@app.route('/newpw/<int:id>', methods=['GET','POST'])
def newpw(id):
    if request.method=='GET':
        return render_template('newpw.html', id=id)
    elif request.method=='POST':
        newpw1 = request.form['newpw1']
        newpw2 = request.form['newpw2']
        if newpw1 == '' or newpw2 =='':
            url = '/login/'
            return redirect(url)
        else:
            if newpw1 == newpw2:
                for i in user:
                    if id == i['id']:
                        i['pw'] = newpw1
                        break;
                with db.cursor() as cur:
                    sql = '''UPDATE user SET pw=%s WHERE ID=%s'''
                    cur.execute(sql,(newpw1, i['id']))
                    db.commit()
                url = '/login/'
                return redirect(url)
            else:
                url = '/findpw/'
                return redirect(url)
                    
                
        



@app.route('/check/<int:id>/')
def check(id):
    for arti in writ:
        if id == arti['id']:
            if arti['pw'] == '':
                url = '/read/'+str(id)
                return redirect(url)
            elif arti['pw'] != '':
                return render_template('check.html', id=id)
                userpw = request.form['pw']
                if userpw == arti['pw']:
                    url = '/read/'+str(id)
                    return redirect(url)
            else:
                url = '/'
                return redirect(url)


@app.route('/download/<int:id>/')
def download(id):
    for arti in writ:
        if id == arti['id']:
            path = './up_down/'+arti['file']
            return send_file(path, as_attachment=True)

            


@app.route('/read/<int:id>/', methods=['POST'])
def read(id):
    if request.method=='POST':
        title = ''
        body = ''
        date =''
        for arti in writ:
            if id == arti['id']:
                title = str(arti['title'])
                body = str(arti['body'])
                date = arti['date']
                break;
        return render_template('read.html', id=id, title=title, body=body, date=date)



    
		


@app.route('/create/', methods=['GET','POST'])
def create():
    if 'id' in session:
        if request.method == 'GET':
            return render_template('create.html')
    
        elif request.method == 'POST':
            global newID
            title = str(request.form['title'])
            body = str(request.form['body'])
            user = str(session['id'])
            pw = str(request.form['pw'])
            f1 = str(request.files['file'])
            f2 = f1.split("'")
            file = f2[1]
            date = datetime.now()
            date = date.strftime("%Y/%m/%d, %H:%M:%S")
            f = request.files['file']
            f.save('./up_down/' + secure_filename(f.filename))
            newwri = {'id':newID, 'title':title, 'body':body, 'user':user, 'date':date, 'pw':pw, 'file':file}
            url = '/'
            with db.cursor() as cur:
                sql = '''INSERT INTO notice1 (id, title, body, user, date, pw, file) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(sql,(newwri['id'],newwri['title'], newwri['body'], newwri['user'], newwri['date'], newwri['pw'], newwri['file']))
                db.commit()
            newID += 1
            writ.append(newwri)
            return redirect(url)
    else:
        url = '/login/'
        return redirect(url)
    
        


@app.route('/update/<int:id>/', methods=['GET','POST'])
def update(id):
    if 'id' in session:
        if request.method =='GET':
            title = ''
            body = ''
            for arti in writ:
                if id == arti['id']:
                    title = arti['title']
                    body = arti['body']
                    date = arti['date']
                    pw = arti['pw']
                    break
            return render_template('update.html', id=id, title=title, body=body, date=date, pw=pw)
    
        elif request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            for arti in writ:
                if id == arti['id']:
                    arti['title']=title
                    arti['body']=body
                    newpw=request.form['pw']
                    arti['pw']=newpw
                    date = datetime.now()
                    date = date.strftime("%Y/%m/%d, %H:%M:%S")
                    arti['date']=date
                    break;
            with db.cursor() as cur:
                sql = '''UPDATE notice1 SET title=%s, body=%s, date=%s, pw=%s WHERE ID=%s'''
                cur.execute(sql,(title, body, date, newpw, arti['id']))
                db.commit()
            url = '/'
            return redirect(url)
    else:
        url = '/login/'
        return redirect(url)




@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        searchtype = request.form['searchtype']
        search = request.form['search']
        word1 = '%'+request.form['search']+'%'
        if searchtype == 'title':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE title LIKE %s'''
            cur.execute(sql,(word1))
            records = cur.fetchall()    
            relist = []
            for arti in records:
                reDict = {
                    'id':arti[0],
                    'title':arti[1],
                    'body':arti[2],
                    'user':arti[3],
                    'date':arti[4]
                    }
                relist.append(reDict)
            db.commit
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)

        elif searchtype == 'body':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE body LIKE %s'''
            cur.execute(sql,(word1))
            records = cur.fetchall()    
            relist = []
            for arti in records:
                reDict = {
                    'id':arti[0],
                    'title':arti[1],
                    'body':arti[2],
                    'user':arti[3],
                    'date':arti[4]
                    }
                relist.append(reDict)
            db.commit
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)
        
        elif searchtype == 'titlebody':
            cur = db.cursor()
            sql = '''SELECT * FROM notice1 WHERE title LIKE %s or body LIKE %s'''
            cur.execute(sql,(word1,word1))
            records = cur.fetchall()    
            relist = []
            for arti in records:
                reDict = {
                    'id':arti[0],
                    'title':arti[1],
                    'body':arti[2],
                    'user':arti[3],
                    'date':arti[4]
                    }
                relist.append(reDict)
            db.commit
            return render_template('search.html', searchtype=searchtype, search=search, relist=relist)



@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for arti in writ:
        if id == arti['id']:
            writ.remove(arti)
            break
    with db.cursor() as cur:
            sql = '''DELETE FROM notice1 WHERE ID=%s'''
            cur.execute(sql,(arti['id']))
            db.commit()
    return redirect('/')


if __name__=="__main__":
    app.run(port=5003)
