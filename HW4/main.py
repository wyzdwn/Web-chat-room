from flask import Flask,request,render_template
import random
import numpy as np

Sudoku=Flask(__name__)

try:
    sudoku_file=open('./data/sudoku.data','r',encoding='utf-8')
    sudoku_data=sudoku_file.read()
    sudoku_file.close()
    sudoku_data=sudoku_data.splitlines()
except FileNotFoundError:
    sudoku_data=[]
last_index=-1   #上次使用的数独数据的下标

@Sudoku.route('/')
def root():
    links = "<a href='/addSudoku'><img width='200' src='./static/img/adddata.png' alt='添加数据' id='adddata' ></a>"
    links += "<a href='/play'><img width='200' src='./static/img/play.png' alt='开始游戏' id='play' ></a>"

    return render_template('root.html',url=links)

@Sudoku.route('/addSudoku')
def addSudoku():
    return Sudoku.send_static_file('addSudoku.html')

@Sudoku.route('/play')
def play():
    global last_index
    index=random.randint(0,len(sudoku_data)-1) #随机选一个数据
    while(last_index==index):
        index = random.randint(0, len(sudoku_data) - 1)
    last_index=index
    return render_template('play.html',data=sudoku_data[index])

@Sudoku.route(('/save'),methods=['post',])
def save():
    sudoku_file=open('./data/sudoku.data','a',encoding='utf-8')
    save_data=request.form['save_data']
    if(sudoku_data.count(save_data)):
        return save_data+'已经保存过了'
    sudoku_data.append(save_data)
    print(save_data,file=sudoku_file) #直接将数据添加到文件中，而不是将列表添加进去
    sudoku_file.close()
    return save_data+'保存成功'

@Sudoku.route('/next',methods=['post',])
def next():
    global last_index
    index = random.randint(0, len(sudoku_data) - 1)  # 随机选一个数据
    while (last_index == index):
        index = random.randint(0, len(sudoku_data) - 1)
    last_index = index
    return sudoku_data[index]

@Sudoku.route('/time_record',methods=['post',]) #记录数独的平均用时，通关次数
def time_record():
    used_time=request.form['used_time'] #本次用时
    data=request.form['data']   #本次通关的数独
    f=open('./data/time_record.txt','r')
    my_record=f.read()
    f.close()
    my_record=my_record.splitlines()
    flag=0  #判断记录中是否有该条数独数据（也就是该数独是否非第一次通关）
    write_back=[]   #处理好后写回文档的数据
    for line in my_record:  #每一行有3条被'\t'隔开的数据：数独数据，平均用时，通关次数
        line=line.split(',')
        if(data==line[0]):
            flag=1
            line[1]=str((float(line[1])*float(line[2])+float(used_time)) / (float(line[2])+1))
            line[2]=str(int(line[2])+1)
        write_back.append(','.join(line))
    if(flag==0):
        line=[]
        line.append(str(data))
        line.append(str(used_time))
        line.append('1')
        write_back.append(','.join(line))
    f = open('./data/time_record.txt', 'w+')
    print('\n'.join(write_back),file=f)
    f.close()
    return ''

if __name__ == '__main__':
    Sudoku.run(port=80,debug=True)