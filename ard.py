import serial
import sqlite3
import datetime
import time


def add_db(time,t,h,dt):
    conn=sqlite3.connect('Temperature.db')
    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS data 
    (Time TEXT,Temperature TEXT,Humidity TEXT,Date TEXT)""")

    c.execute(""" INSERT INTO data
    (Time, Temperature, Humidity, Date)
    VALUES (?, ?, ?, ?)""", (time, t, h, dt))

    conn.commit()
    c.close()
    conn.close()


def read_data():
    arduinodata=serial.Serial('COM8',9600,timeout=0.1)
    while arduinodata.inWaiting:
        val=arduinodata.readline().decode('ascii')
        if len(val) == 13 :
            #print(val)
            return val


while 1:
    h,t=read_data().split(',')
    mytime=datetime.datetime.now()
    tm='{}:{}:{}'.format(mytime.hour,mytime.minute,mytime.second)
    dt='{}/{}/{}'.format(mytime.month,mytime.day,mytime.year)

    print(tm,str(t),str(h),str(dt))
    add_db(tm,str(t),str(h),str(dt))

    time.sleep(10)


