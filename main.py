from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import pandas as pd
from pandas import DataFrame
import os
import json

app = Flask(__name__)

#This function is used to load the csv file into the database
@app.route('/ctb', methods=['GET','POST'])
def ctb():
    if request.method == 'POST':
        f = request.files['myf']
        d = pd.read_csv(f)
        cnx = sql.connect('minnowdatabase.db')
        d.to_sql(name="minnow", con=cnx, if_exists="replace", index=False)
        return render_template('home.html')

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/barchart', methods=['GET','POST'])
def list():
    cnx = sql.connect("minnowdatabase.db")
    cnx.row_factory = sql.Row
    cr = cnx.cursor()
    cr.execute("select * from minnow where Fare=100")
    rows = cr.fetchall();
    fare100=len(rows)
    cr.execute("select * from minnow where Fare=200")
    rows = cr.fetchall();
    fare200=len(rows)
    cr.execute("select * from minnow where Fare=500")
    rows = cr.fetchall();
    fare500=len(rows)
    cr.execute("select * from minnow where Fare=800")
    rows = cr.fetchall();
    fare800=len(rows)
    total = 0.0
    total = fare100 + fare200 + fare500 + fare800
    p1 = (fare100*100.0)/total
    p2 = (fare200*100.0)/total
    p3 = (fare500*100.0)/total
    p4 = (fare800*100.0)/total
    print("fetch success")
    return render_template('barchart.html',p1=p1,p2=p2,p3=p3,p4=p4)

@app.route('/piegraph', methods=['GET','POST'])
def fare():
    cnx = sql.connect("minnowdatabase.db")
    cnx.row_factory = sql.Row
    cr = cnx.cursor()
    cr.execute("select * from minnow where Age between 10 and 19")
    rows = cr.fetchall();
    a=len(rows)
    cr.execute("select * from minnow where Age between 20 and 29")
    rows = cr.fetchall();
    b=len(rows)
    cr.execute("select * from minnow where Age between 30 and 39")
    rows = cr.fetchall();
    c=len(rows)
    cr.execute("select * from minnow where Age between 40 and 49")
    rows = cr.fetchall();
    d=len(rows)
    counts=[a,b,c,d]
    cr.execute("select * from minnow where Fare=100")
    rows = cr.fetchall();
    fare100=len(rows)
    cr.execute("select * from minnow where Fare=200")
    rows = cr.fetchall();
    fare200=len(rows)
    cr.execute("select * from minnow where Fare=500")
    rows = cr.fetchall();
    fare500=len(rows)
    cr.execute("select * from minnow where Fare=800")
    rows = cr.fetchall();
    fare800=len(rows)
    total = 0.0
    total = fare100 + fare200 + fare500 + fare800
    p1 = (fare100*100.0)/total
    p2 = (fare200*100.0)/total
    p3 = (fare500*100.0)/total
    p4 = (fare800*100.0)/total
    print("fetch success")
    return render_template('piechart.html',var=counts,p1=p1,p2=p2,p3=p3,p4=p4)
    
@app.route('/scattergraph', methods=['GET','POST'])
def scattergraph():
    cnx = sql.connect("minnowdatabase.db")
    cnx.row_factory = sql.Row
    cr = cnx.cursor()
    cr.execute("select Survived from minnow")
    rows1 = cr.fetchall();
    a=len(rows1)
    cr.execute("select Age from minnow")
    rows2 = cr.fetchall();
    b=len(rows2)
    mylist = []  
    the_list = [] 
    for i in range(a):
        mylist.append(rows1[i])
        mylist.append(rows2[i])
        the_list.append(mylist)
        mylist = []
    return render_template('scattergraph.html',the_list=the_list)

@app.route('/imagedisplay', methods=['GET','POST'])
def imagedisplay():
	return render_template('imagedisplay.html')

if __name__ == '__main__':
    app.run(debug=True)