import sqlite3
from tkinter import *
from tkinter import ttk,messagebox
import time

win = Tk()
win.title('登录')
screenwidth = win.winfo_screenwidth()  
screenheight = win.winfo_screenheight()  
size = '%dx%d+%d+%d' % (400, 400, (screenwidth - 400)/2, (screenheight - 400)/2)    
win.geometry(size)
win.resizable(False, False)

#登录**页面布局
lab1 = Label(win,text = '饭卡管理系统登录',font = '微软雅黑 15').place(x = 120,y = 30)
frame1 = Frame(win,height = 200,width = 300,bd = 1,relief = 'sunken')
frame1.place(x = 50,y = 90)
lab_username = Label(frame1,text = '用户名：',font = '微软雅黑 12').place(x = 40,y = 40)
entry_username = Entry(frame1,width = 20)
entry_username.place(x = 110,y = 45)
lab_passwd = Label(frame1,text = '密 码：',font = '微软雅黑 12').place(x = 40,y = 80)
entry_passwd = Entry(frame1,width = 20,show = '*')
entry_passwd.place(x = 110,y = 85)
lab4 = Label(frame1,text = '选择登录类型：',font = '微软雅黑 12').place(x = 40,y = 120)
combo4 = ttk.Combobox(frame1, width=10, height=20,values=('学生', '教职工','管理员'),state = "readonly")
combo4.place(x=150, y=120,)
combo4.current(0)#默认值
btn1 = ttk.Button(win,text = '登录')
btn1.place(x = 80,y = 320)
btn2 = ttk.Button(win,text = '取消',command = lambda: win.quit())
btn2.place(x = 240,y = 320)

#创建表
try:
    conn = sqlite3.connect('fanka.db')
    conn.execute('''CREATE TABLE USER
                  (ID CHAR(13) PRIMARY KEY NOT NULL ,
                  PASSWD TEXT,
                  TYPE TEXT)''')
    conn.execute('''CREATE TABLE USERINFO
                  (ID CHAR(13) PRIMARY KEY NOT NULL ,
                  NAME TEXT,
                  SEX BOOLEAN,
                  PHONENUM  CHAR(11),
                  ADDR CHAR(50))''')
    conn.execute('''CREATE TABLE CDINFO
                  (ID CHAR(13) PRIMARY KEY NOT NULL,
                  MONEY FLOAT ,
                  LOCK BOOLEAN)''')
    conn.execute('''CREATE TABLE HISTORY
                  (ID CHAR(13) ,
                  TIME TEXT,
                  MONEY FLOAT )''')
    messagebox.showinfo('欢迎使用','初始化成功！')
    conn.close()
except:
    pass

conn = sqlite3.connect('fanka.db')

varmoney = StringVar()
infoID = StringVar()
sexSelect = StringVar()
peopleSelect = StringVar()

time1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def check_lock(ID):
    cursor = conn.execute('SELECT lock from CDINFO where ID= "'+ ID +'"')
    temp = cursor.fetchall()
    if temp[0][0] == 1:
        messagebox.showinfo('提示','此饭卡已锁定')
        return False
    else:
        return True
    
def doSql(sql):
    '''用来执行SQL语句，尤其是INSERT和DELETE语句'''    
    conn = sqlite3.connect('fanka.db')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    
#登录**函数定义
def login(event):
    
    def infoWin():
        '''详细信息——窗口'''
        global infoID,sexSelect
        winInfo = Toplevel() 
        sizeWinInfo = '%dx%d+%d+%d' % (500, 500, (screenwidth - 500)/2, (screenheight - 500)/2)    
        winInfo.geometry(sizeWinInfo)
        winInfo.title('详细信息')
        winInfo.attributes("-toolwindow", 1)#新窗口在最上面
            
        lab11InfoID = Label(winInfo,text = '卡号',font = '微软雅黑 12',fg = 'blue').place(x = 140,y = 10)
        lab12InfoID = Label(winInfo,textvariable = infoID,font = '微软雅黑 12',fg = 'blue').place(x = 220,y = 10)
            
        lab2InfoName = Label(winInfo,text = '姓名',font = '微软雅黑 12').place(x = 140,y = 60)
        entryInfoName = Entry(winInfo,width = 20)
        entryInfoName.place(x = 220,y = 62)
                        
        lab3InfoName = Label(winInfo,text = '性别',font = '微软雅黑 12').place(x = 140,y = 140)
        comboInfoSex = ttk.Combobox(winInfo, width=5, height=20,textvariable = sexSelect,values=('男', '女'),state = "readonly")
        comboInfoSex.place(x = 220,y = 142)
        sexSelect.set('男')
                        
        lab41InfoNum = Label(winInfo,text = '电话',font = '微软雅黑 12').place(x = 140,y = 220)
        entryInfoNum = Entry(winInfo,width = 20)
        entryInfoNum.place(x = 220,y = 222)
                        
        lab5InfoAddr = Label(winInfo,text = '住址',font = '微软雅黑 12').place(x = 140,y = 300)
        entryInfoAddr = Entry(winInfo,width = 20)
        entryInfoAddr.place(x = 220,y = 302)
                        
        btn1Info = ttk.Button(winInfo,text = '确定',width = 15)
        btn1Info.place(x = 100,y = 400)
                        
        btn2Info = ttk.Button(winInfo,text = '清除',width = 15)
        btn2Info.place(x = 300,y = 400)
        
        cursor = conn.execute('select * from USERINFO where ID = "'+ infoID.get() +'"')
        temp = cursor.fetchall()[0]
        entryInfoName.insert(0,temp[1])
        sexSelect.set(temp[2])
        entryInfoNum.insert(0,temp[3])
        entryInfoAddr.insert(0,temp[4])

        def check(event):
            ID = infoID.get()
            name = entryInfoName.get()
            sex = comboInfoSex.get()
            phonenum = entryInfoNum.get()
            addr = entryInfoAddr.get()

            if name == '':
                messagebox.showerror('错误','姓名不能为空')
                return 
            if phonenum != '':
                if len(phonenum) != 11:
                    messagebox.showerror('错误','手机号码必须为11位')
                    return 
            ask = messagebox.askyesnocancel('注意','是否保存修改？')
            if ask == True:
                sql = 'update USERINFO set name = "'+ name + '", sex = "' 
                sql += sex + '", phonenum = "' + phonenum + '",addr ="' + addr + '"'
                doSql(sql)
                winInfo.destroy()
                messagebox.showinfo('恭喜','修改成功！')
            elif ask == False:
                winInfo.destroy()
            else:
                pass
             
        def clear(event):
            entryInfoName.delete(0, END)
            entryInfoNum.delete(0, END)
            entryInfoAddr.delete(0, END)
            comboInfoSex.current(0)
            
        btn1Info.bind('<Button-1>',check)
        btn2Info.bind('<Button-1>',clear)

    def addMoneyWin():
        '''充值——窗口'''
        global entry1AddMoney,ID
        winAddMoney = Toplevel() 
        sizeWinAddMoney = '%dx%d+%d+%d' % (400, 250, (screenwidth - 400)/2, (screenheight - 250)/2)    
        winAddMoney.geometry(sizeWinAddMoney)
        winAddMoney.title('充值')
        winAddMoney.attributes("-toolwindow", 1)#新窗口在最上面

        frameAddMoney = Frame(winAddMoney,height = 200,width = 340,bd = 1,relief = 'sunken')
        frameAddMoney.place(x = 30,y = 30)
        lab1AddMoney = Label(frameAddMoney,text = '充值金额：',font = '微软雅黑 12').place(x = 50,y = 30)
        entry1AddMoney = Entry(frameAddMoney,width = 20)
        entry1AddMoney.place(x = 130,y = 32)
        btn1AddMoney = ttk.Button(frameAddMoney,text = '确认')
        btn1AddMoney.place(x = 40,y = 150)
        btn2AddMoney = ttk.Button(frameAddMoney,text = '清除')
        btn2AddMoney.place(x = 200,y = 150)
        
        def clear(event):
                entry1AddMoney.delete(0, END)
        
        def add(event):
            cursor = conn.execute('select money from CDINFO where ID = "'+ ID +'"')
            temp = cursor.fetchall()
            money1 = temp[0][0]
            sql1 = 'update CDINFO set money = "'+ str(money1 + float(entry1AddMoney.get())) +'" where ID = "'+ ID +'"'
            sql2 = 'insert into HISTORY values("'+ ID +'","'+ time1 + '","'+ entry1AddMoney.get() +'")'
            doSql(sql1)
            doSql(sql2)
            cursor = conn.execute('select money from CDINFO where ID = "'+ ID +'"')
            temp = cursor.fetchall()
            money2 = temp[0][0]
            messagebox.showinfo('恭喜','充值成功！当前余额为%0.2f' %money2 + ' 元')
            varmoney.set(money2)
            winAddMoney.destroy() 
        
        btn1AddMoney.bind('<Button-1>',add)
        btn2AddMoney.bind('<Button-1>',clear)
            
    def lookWin():
        '''查看历史——窗口'''
        global treeList
        winLookWin = Toplevel() 
        sizeLookWin = '%dx%d+%d+%d' % (550, 300, (screenwidth - 550)/2, (screenheight - 300)/2)    
        winLookWin.geometry(sizeLookWin)
        winLookWin.title('流水查询')
        winLookWin.attributes("-toolwindow", 1)#新窗口在最上面
            
        #在窗口上放置用来显示通信录信息的表格，使用Treeview组件实现
        frame = Frame(winLookWin,height = 300,width = 500,bd = 1,relief = 'sunken')
        frame.place(x=3, y=3)
        #滚动条
        scrollBar = Scrollbar(frame)
        scrollBar.pack(side=RIGHT, fill=Y)
        #Treeview组件
        treeList = ttk.Treeview(frame,height = 13, columns=('c1', 'c2', 'c3'),show="headings", yscrollcommand = scrollBar.set)
        treeList.column('c1', width=170, anchor='center')
        treeList.column('c2', width=170, anchor='center')
        treeList.column('c3', width=170, anchor='center')
        treeList.heading('c1', text='卡号')
        treeList.heading('c2', text='操作时间')
        treeList.heading('c3', text='明细（元）')
        treeList.pack(side=LEFT, fill=BOTH)
        #Treeview组件与垂直滚动条结合
        scrollBar.config(command=treeList.yview)

    def newWin():
        winNewWin = Toplevel(win) 
        sizeWinNewWin = '%dx%d+%d+%d' % (500, 500, (screenwidth - 500)/2, (screenheight - 500)/2)    
        winNewWin.geometry(sizeWinNewWin)
        winNewWin.title('用户操作')
        winNewWin.attributes("-toolwindow", 1)#新窗口在最上面
        
        lab1NewWin = Label(winNewWin,text = '欢迎使用饭卡管理系统',font = '微软雅黑 15').place(x = 150,y = 30)
        frameNewWin = Frame(winNewWin,height = 350,width = 430,bd = 1,relief = 'sunken')
        frameNewWin.place(x = 30,y = 110)
        lab2NewWin = Label(frameNewWin,text = '卡号：',font = '微软雅黑 12').place(x = 120,y = 50)
        entryNewWinID = Entry(frameNewWin,width = 20)
        entryNewWinID.place(x = 180,y = 54)
            
        btn1NewWin = ttk.Button(frameNewWin,text = '修改密码',width = 18)
        btn1NewWin.place(x = 160,y = 120)
            
        btn2NewWin = ttk.Button(frameNewWin,text = '充     值',width = 18)
        btn2NewWin.place(x = 160,y = 150)
            
        btn3NewWin = ttk.Button(frameNewWin,text = '详细信息',width = 18)
        btn3NewWin.place(x = 160,y = 180)
            
        btn4NewWin = ttk.Button(frameNewWin,text = '挂     失',width = 18)
        btn4NewWin.place(x = 160,y = 210)
            
        btn5NewWin = ttk.Button(frameNewWin,text = '流水查询',width = 18)
        btn5NewWin.place(x = 160,y = 240)

        lab3NewWin = Label(frameNewWin,text = '余额：',font = '微软雅黑 12').place(x = 120,y = 290)
        lab4NewWin = Label(frameNewWin,width = 5,textvariable = varmoney,font = '微软雅黑 12').place(x = 190,y = 290)

        lab5NewWin = Label(frameNewWin,text = '(元)',font = '微软雅黑 12').place(x = 260,y = 290)
        
        cursor = conn.execute('select money from CDINFO where ID = "'+ entry_username.get() +'"')
        temp = cursor.fetchall()
        money2 = temp[0][0]
            
        entryNewWinID.insert(0,entry_username.get())
        varmoney.set(money2)

        def alterPasswd(event):
            '''修改密码'''
            winAlterPasswd = Toplevel(winNewWin) 
            sizeWinAlterPasswd = '%dx%d+%d+%d' % (400, 250, (screenwidth - 400)/2, (screenheight - 250)/2)    
            winAlterPasswd.geometry(sizeWinAlterPasswd)
            winAlterPasswd.title('修改密码')
            winAlterPasswd.attributes("-toolwindow", 1)#新窗口在最上面

            frameAlterPasswd = Frame(winAlterPasswd,height = 200,width = 340,bd = 1,relief = 'sunken')
            frameAlterPasswd.place(x = 30,y = 30)
            lab1AlterPasswd = Label(frameAlterPasswd,text = '原密码：',font = '微软雅黑 12').place(x = 50,y = 30)
            entry1AlterPasswd = Entry(frameAlterPasswd,show = '*',width = 20)
            entry1AlterPasswd.place(x = 130,y = 32)
            lab1AlterPasswd = Label(frameAlterPasswd,text = '新密码：',font = '微软雅黑 12').place(x = 50,y = 60)
            entry2AlterPasswd = Entry(frameAlterPasswd,show = '*',width = 20)
            entry2AlterPasswd.place(x = 130,y = 62)
            lab1AlterPasswd = Label(frameAlterPasswd,text = '确认密码：',font = '微软雅黑 12').place(x = 50,y = 90)
            entry3AlterPasswd = Entry(frameAlterPasswd,show = '*',width = 20)
            entry3AlterPasswd.place(x = 130,y = 92)
            btn1AlterPasswd = ttk.Button(frameAlterPasswd,text = '确认')
            btn1AlterPasswd.place(x = 40,y = 150)
            btn2AlterPasswd = ttk.Button(frameAlterPasswd,text = '清除')
            btn2AlterPasswd.place(x = 200,y = 150)

            def clear(event):
                entry1AlterPasswd.delete(0, END)
                entry2AlterPasswd.delete(0, END)
                entry3AlterPasswd.delete(0, END)

            def check(event):
                if entry1AlterPasswd.get() != entry_passwd.get():
                    messagebox.showerror('错误','原密码输入错误')
                    return
                elif entry2AlterPasswd.get() != entry3AlterPasswd.get():
                    messagebox.showerror('错误','两次输入不一致')
                    return
                else:
                    sql = 'update USER set passwd = "'+ entry3AlterPasswd.get() +'"'
                    doSql(sql)
                    messagebox.showinfo('恭喜','修改成功！')
                    winAlterPasswd.destroy()
                    winNewWin.destroy()
                    entry_passwd.delete(0,END)
                    messagebox.showwarning('提示','请重新登录')
                    return
                    
            btn1AlterPasswd.bind('<Button-1>',check)
            btn2AlterPasswd.bind('<Button-1>',clear)
        
        def addmoney(event):
            '''充值'''
            global ID
            ID = entryNewWinID.get()
            addMoneyWin()            

        def information(event):
            '''详细信息'''
            infoID.set(entryNewWinID.get())
            infoWin()

        def lost(event):
            '''挂失'''
            ask = messagebox.askyesno('提示','将要进行挂失，挂失后将不能自助解锁\n\t是否继续？')
            if ask == True:
                if check_lock(entryNewWinID.get()) :
                    sql = 'update CDINFO set lock = "1" where ID = "'+ entryNewWinID.get() +'"'
                    doSql(sql)
                    winNewWin.destroy()
                    
            else:
                return

        def look(event):
            '''查看历史'''
            lookWin()
            showall(entryNewWinID.get())
            
        btn1NewWin.bind('<Button-1>',alterPasswd)
        btn2NewWin.bind('<Button-1>',addmoney)
        btn3NewWin.bind('<Button-1>',information)
        btn4NewWin.bind('<Button-1>',lost)
        btn5NewWin.bind('<Button-1>',look)
    #学生/教职工登录
    if combo4.get() == '学生'or combo4.get() =='教职工':
        cursor = conn.execute('SELECT * from USER where ID= "'+ entry_username.get() +'"')
        temp = cursor.fetchall()
        if len(temp) == 0:
            messagebox.showerror('错误','用户不存在')
            return
        elif temp[0][2] != combo4.get():
            messagebox.showerror('错误','用户类别不正确')
            return
        elif check_lock(entry_username.get()):
            passwd = temp[0][1]
            if entry_passwd.get() != passwd:
                messagebox.showerror('错误','用户名或密码不正确')
                return
            else:
                newWin()        
    
    #管理员登录
    elif combo4.get() == '管理员':
        if entry_username.get() == 'root' and entry_passwd.get() == 'root123':
            win_root = Toplevel(win) 
            size_root = '%dx%d+%d+%d' % (700, 400, (screenwidth - 700)/2, (screenheight - 400)/2)    
            win_root.geometry(size_root)
            win_root.title('管理员操作')
            win_root.attributes("-toolwindow", 1)
            
            #管理员***页面布局
            lab1_root = Label(win_root,text = '欢迎进入管理员界面',font = '微软雅黑 15').place(x = 250,y = 30)
            frame1_root = Frame(win_root,height = 200,width = 650,bd = 1,relief = 'sunken')
            frame1_root.place(x = 28,y = 110)
            lab2_root = Label(frame1_root,text = '卡号：',font = '微软雅黑 12').place(x = 30,y = 80)
            entry_ser_num = Entry(frame1_root,width = 20)
            entry_ser_num.place(x = 80,y = 84)
            
            btn1_root = ttk.Button(frame1_root,text = '新建持卡者',width = 18)
            btn1_root.place(x = 300,y = 30)
            
            btn2_root = ttk.Button(frame1_root,text = '充值',width = 18)
            btn2_root.place(x = 300,y = 85)
            
            btn3_root = ttk.Button(frame1_root,text = '注销饭卡',width = 18)
            btn3_root.place(x = 300,y = 140)
            
            btn4_root = ttk.Button(frame1_root,text = '更改持卡者详细信息',width = 18)
            btn4_root.place(x = 480,y = 30)
            
            btn5_root = ttk.Button(frame1_root,text = '挂失/解锁',width = 18)
            btn5_root.place(x = 480,y = 85)
            
            btn6_root = ttk.Button(frame1_root,text = '查询消费历史',width = 18)
            btn6_root.place(x = 480,y = 140)

            #管理员***函数定义
            def addUser(event):
                '''新建用户'''
                global peopleSelect
                win_root_new = Toplevel(win_root) 
                size_root_new = '%dx%d+%d+%d' % (500, 500, (screenwidth - 500)/2, (screenheight - 500)/2)    
                win_root_new.geometry(size_root_new)
                win_root_new.title('新建用户')
                
                lab11_root_new = Label(win_root_new,text = '卡号',font = '微软雅黑 12').place(x = 140,y = 60)
                lab12_root_new = Label(win_root_new,text = '*',fg = 'red').place(x = 180,y = 60)
                entry_new_ID = Entry(win_root_new,width = 20)
                entry_new_ID.place(x = 220,y = 62)
                
                lab21_root_new = Label(win_root_new,text = '姓名',font = '微软雅黑 12').place(x = 140,y = 100)
                lab22_root_new = Label(win_root_new,text = '*',fg = 'red').place(x = 180,y = 100)
                entry_new_name = Entry(win_root_new,width = 20)
                entry_new_name.place(x = 220,y = 102)
                
                lab3_root_new = Label(win_root_new,text = '性别',font = '微软雅黑 12').place(x = 140,y = 140)
                combo_new_sex = ttk.Combobox(win_root_new, width=5, height=20,values=('男', '女'),state = "readonly")
                combo_new_sex.place(x = 220,y = 142)
                combo_new_sex.current(0)
                
                lab4_root_new = Label(win_root_new,text = '电话',font = '微软雅黑 12').place(x = 140,y = 200)
                entry_new_phone = Entry(win_root_new,width = 20)
                entry_new_phone.place(x = 220,y = 202)
                
                lab5_root_new = Label(win_root_new,text = '住址',font = '微软雅黑 12').place(x = 140,y = 240)
                entry_new_addr = Entry(win_root_new,width = 20)
                entry_new_addr.place(x = 220,y = 242)
                
                lab6_root_new = Label(win_root_new,text = '类别',font = '微软雅黑 12').place(x = 140,y = 280)
                comboInfoPeople = ttk.Combobox(win_root_new, width=5, height=20,textvariable = peopleSelect,values=('学生', '教职工'),state = "readonly")
                comboInfoPeople.place(x = 220,y = 282)
                peopleSelect.set('')
                
                btn1_root_new = ttk.Button(win_root_new,text = '确定',width = 15)
                btn1_root_new.place(x = 100,y = 400)
                
                btn2_root_new = ttk.Button(win_root_new,text = '清除',width = 15)
                btn2_root_new.place(x = 300,y = 400)

                def check(event):
                    ID = entry_new_ID.get()
                    name = entry_new_name.get()
                    sex = combo_new_sex.get()
                    phonenum = entry_new_phone.get()
                    addr = entry_new_addr.get()
                    passwd = '123456'
                    people = comboInfoPeople.get()
                    
                    if ID == '':
                        messagebox.showerror('错误','卡号不能为空')
                        return
                    if len(ID) != 8:
                        messagebox.showerror('错误','卡号必须为8位')
                        return 
                    cursor = conn.execute('SELECT * from USERINFO where ID= "'+ ID +'"')
                    temp = cursor.fetchall()
                    if len(temp) != 0:
                        messagebox.showerror('错误','卡号已存在')
                        return
                    if name == '':
                        messagebox.showerror('错误','姓名不能为空')
                        return 
                    if phonenum != '':
                        if len(phonenum) != 11:
                            messagebox.showerror('错误','手机号码必须为11位')
                            return 
                    if people == '':
                        messagebox.showerror('错误','请选择用户类别')
                        return
                    
                    sql1 = 'insert into USERINFO values("'+ ID +'","'+ name + '","' + sex + '","' + phonenum + '","' + addr + '")'
                    sql2 = 'insert into USER values("'+ ID +'","' + passwd + '","'+ people +'")'
                    sql3 = 'insert into CDINFO values("'+ ID +'","0","0")'
                    sql4 = 'insert into HISTORY values("'+ ID +'","'+ time1 + '","0")'

                    doSql(sql1)
                    doSql(sql2)
                    doSql(sql3)
                    doSql(sql4)
                    win_root_new.destroy()
                    messagebox.showinfo('恭喜','新建成功！')
                
                def clear(event):
                    entry_new_num.delete(0, END)
                    entry_new_name.delete(0, END)
                    entry_new_phone.delete(0, END)
                    entry_new_addr.delete(0, END)
                        
                btn1_root_new.bind('<Button-1>',check)
                btn2_root_new.bind('<Button-1>',clear)

            def addmoneyRoot(event):
                '''充值'''
                global ID
                ID = entry_ser_num.get()
                if ID == '':
                    messagebox.showerror('错误','请输入要充值的卡号')
                    return
                else:
                    cursor = conn.execute('SELECT * from USER where ID= "'+ ID +'"')
                    temp = cursor.fetchall()
                    if len(temp) == 0:
                        messagebox.showerror('错误','用户不存在')
                        return
                    else:
                        addMoneyWin()

            def logout(event):
                '''注销'''
                global ID
                ID = entry_ser_num.get()
                if ID == '':
                    messagebox.showerror('错误','请输入要注销的卡号')
                    return
                else:
                    cursor = conn.execute('SELECT * from USER where ID= "'+ ID +'"')
                    temp = cursor.fetchall()
                    if len(temp) == 0:
                        messagebox.showerror('错误','用户不存在')
                        return
                    else:
                        ask = messagebox.askyesno('提示','          将要进行注销\n             是否继续？')
                        if ask == True:
                            sql1 = 'delete from USER where ID = "'+ ID +'"'
                            sql2 = 'delete from USERINFO where ID = "'+ ID +'"'
                            sql3 = 'delete from CDINFO where ID = "'+ ID +'"'
                            sql4 = 'delete from HISTORY where ID = "'+ ID +'"'
                            doSql(sql1)
                            doSql(sql2)
                            doSql(sql3)
                            doSql(sql4)
                            messagebox.showinfo('恭喜','删除成功！')
                        else:
                            pass
            
            def informationRoot(event):
                '''详细信息'''
                if entry_ser_num.get() == '':
                    messagebox.showerror('错误','请输入要查看的卡号')
                    return
                else:
                    cursor = conn.execute('SELECT * from USER where ID= "'+ entry_ser_num.get() +'"')
                    temp = cursor.fetchall()
                    if len(temp) == 0:
                        messagebox.showerror('错误','用户不存在')
                        return
                    else:
                        infoID.set(entry_ser_num.get())
                        infoWin()
            
            def lostUnlock(event):
                '''挂失解锁'''
                if entry_ser_num.get() == '':
                        messagebox.showerror('错误','请输入要挂失/解锁的卡号')
                        return
                else:
                    cursor = conn.execute('SELECT * from USER where ID= "'+ entry_ser_num.get() +'"')
                    temp = cursor.fetchall()
                    if len(temp) == 0:
                        messagebox.showerror('错误','用户不存在')
                        return
                
                winLostUnlock = Toplevel(win_root) 
                sizeLostUnlock = '%dx%d+%d+%d' % (400, 250, (screenwidth - 400)/2, (screenheight - 250)/2)    
                winLostUnlock.geometry(sizeLostUnlock)
                winLostUnlock.title('挂失/解锁')

                btn1LostUnlock = ttk.Button(winLostUnlock,text = '挂失',width = 15)
                btn1LostUnlock.place(x = 150,y = 80)
                
                btn2LostUnlock = ttk.Button(winLostUnlock,text = '解锁',width = 15)
                btn2LostUnlock.place(x = 150,y = 150)
                
                def lock(event):
                    if check_lock(entry_ser_num.get()):
                        sql = 'update CDINFO set lock = "1" where ID = "'+ entry_ser_num.get() +'"'
                        doSql(sql)
                        winLostUnlock.destroy()
                        messagebox.showinfo('提示','已挂失')
                    
                def unLock(event):
                    cursor = conn.execute('SELECT lock from CDINFO where ID= "'+ entry_ser_num.get() +'"')
                    temp = cursor.fetchall()
                    if temp[0][0] == 0:
                        messagebox.showerror('错误','不可重复解锁')
                        return
                    sql = 'update CDINFO set lock = "0" where ID = "'+ entry_ser_num.get() +'"'
                    doSql(sql)
                    winLostUnlock.destroy()
                    messagebox.showinfo('提示','已解锁') 
                    
                btn1LostUnlock.bind('<Button-1>',lock)
                btn2LostUnlock.bind('<Button-1>',unLock)

            def lookRoot(event):
                '''查看历史'''
                if entry_ser_num.get() == '':
                    messagebox.showerror('错误','请输入要查看的卡号')
                    return
                else:
                    cursor = conn.execute('SELECT * from USER where ID= "'+ entry_ser_num.get() +'"')
                    temp = cursor.fetchall()
                    if len(temp) == 0:
                        messagebox.showerror('错误','用户不存在')
                        return
                    else:
                        lookWin()
                        showall(entry_ser_num.get())
            
            btn1_root.bind('<Button-1>',addUser)
            btn2_root.bind('<Button-1>',addmoneyRoot)
            btn3_root.bind('<Button-1>',logout)
            btn4_root.bind('<Button-1>',informationRoot)
            btn5_root.bind('<Button-1>',lostUnlock)
            btn6_root.bind('<Button-1>',lookRoot)
        else:
            messagebox.showerror('错误','用户名或密码错误！')

#显示所有信息
def showall(ID):
    for row in treeList.get_children():
        treeList.delete(row)
    cursor = conn.execute('select * from HISTORY where ID ="'+ ID +'"')
    temp = cursor.fetchall()

    for i in temp:
        treeList.insert('', 'end', values=i)

btn1.bind('<Button-1>',login)

win.mainloop()

