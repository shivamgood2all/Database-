#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import base64
import imageio
import cv2 


# In[ ]:


password = '123456'

connect = input('Please enter the password: ')

while connect != password:
    connect = input('Please enter the password: ')
    if connect == 'q':
        break 
        
if connect == password:
    conn = sqlite3.connect('mysafe.db')
    
    try:
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''') 
        print('Your safe has been created!\n what would you like to store in it today?')
    except:
        print('You have a safe. What would you like to do today?')
        
    while True:
        print('\n'+'*'*15)
        print('Commands')
        print('s: store a file.')
        print('o: see a file.')
        print('q: quit.')
        print('*'*15)
        input_=input(':')
            
        if input_ == 'q':
            break 
        if input_ == 'o':
            #open a file
            file_type = input('what is the file type of the file you want to open\n')
            file_name = input('what is the file name you want to open\n')
            fill_ = file_name+'.'+file_type
                
            cursor = conn.execute('SELECT * FROM SAFE WHERE FULL_NAME='+'"'+fill_+'"')
                
            file_string =''
            for row in cursor:
                file_string = row[3]
            with open(fill_ , 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))
                
        if input_ == 's':
            #store a file
                
            PATH = input('Type in the full path to the file you want to store.\nExample: /Users/kalle/Desktop/myfile.py\n')
                
            FILE_TYPES ={
                'txt':'TEXT',
                'java':'TEXT',
                'dart':'TEXT',
                'py':'TEXT',
                'jpg':'IMAGE',
                'png':'IMAGE',
                'jpeg':'IMAGE'
            }
                
            file_name = PATH.split('\\')
            file_name = file_name[len(file_name)-1]
            file_string = ''
                
            NAME = file_name.split('.')[0]
            EXTENSION = file_name.split('.')[1]
                                       
            try:
                EXTENSION = FILE_TYPES[EXTENSION]
                
            except:
                Exception()
                
                                       
            if EXTENSION == 'IMAGE':
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode('.jpg',IMAGE)[1]).decode()
                
            if EXTENSION == 'TEXT':
                file_string = open(PATH,'r').read()
                file_string = base64.b64encode(file_string)
                    
            EXTENSION = file_name.split('.')[1]
                
            command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')
            
            conn.execute(command)
            conn.commit()
                    
                
                        
    


# In[ ]:




