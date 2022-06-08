

def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import iz_func
    import iz_game
    import iz_main
    import time
    import iz_telegram
    db,cursor = iz_func.connect ()

    send_message = 'Yes'

    if message_in.find ("/start") != -1:
        send_message = 'No'


    if message_in == "Отмена":
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'ОтменаДействия','S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''


    if message_in == "Купить":
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'КупитьПодписку','S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ''





    if message_in.find ("Регистрация") != -1:
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Укажите Ваше имя','S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'Имя')


    if status == 'Имя':
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Укажите Ваше телефон','S',0) 
        iz_telegram.save_variable (user_id,namebot,"Имя",message_in)
        iz_telegram.save_variable (user_id,namebot,"status",'Телефон')


    if status == 'Телефон':
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Укажите Ваше email','S',0) 
        iz_telegram.save_variable (user_id,namebot,"Телефон",message_in)
        iz_telegram.save_variable (user_id,namebot,"status",'email')

    if status == 'email':
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Спасибо за регистрацию','S',0) 
        iz_telegram.save_variable (user_id,namebot,"email",message_in)
        iz_telegram.save_variable (user_id,namebot,"status",'')




    if message_in.find (namebot) != -1:
        send_message = 'No'
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Поиск ключа в базе данных','S',0) 
        sql = "select id,name from bot_access_code where 1=1 limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,name = rec.values() 
        if id == 0: 
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Ключ в базе не найден','S',0) 
        else:
            message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Ключ в базе обнаружен','S',0) 
            id = 0
            sql = "select id from bot_active_user where 1=1 limit 1;".format()
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id = rec.values() 
            if id == 0:                             	
                message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Создаем клиента для рассылки','S',0) 
                sql = "INSERT INTO bot_active_user (adress,komment,language,login,namebot,project,summ,`system`,telefon,user_id,wallet) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format ("","","","",namebot,"","","","","",user_id)
                cursor.execute(sql)
                db.commit()
            else:
            	message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Обновляем данные рассылки','S',0) 

    if message_in.find ("add1_") != -1:
        send_message = 'No'
        db,cursor = iz_func.connect ()
        word  = message_in.replace('add1_','')
        sql = "select id,message,namebot,user_id from bot_message_send where id = {} limit 1;".format(word)
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,message,namebot_l,user_id_l = rec.values()

            message_out = '<b>Отправлен</b>\n'+message
            markup = ''
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)


            sql = "select id,user_id from bot_user where namebot = '{}'".format(namebot)
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            list = []
            for rec in data: 
                id,user_id_s = rec.values()
                list.append([id,user_id_s])
            
            number_of_elements = len(list)
            message_out,menu = iz_telegram.get_message (user_id,'Начало рассылки',namebot)
            message_out = message_out.replace('%%number_of_elements%%',str(number_of_elements)) 
            message_out = message_out.replace('%%Отправлено сообщений%%',str(0)) 
            markup = ''
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
            nm_answer = answer

            number_of_send = 0
            for line in list:
                number_of_send = number_of_send + 1
                message_out,menu = iz_telegram.get_message (user_id,'Начало рассылки',namebot)
                message_out = message_out.replace('%%number_of_elements%%',str(number_of_elements)) 
                message_out = message_out.replace('%%Отправлено сообщений%%',str(number_of_send)) 
                markup = ''
                answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,nm_answer) 

                message_out =  message
                markup = ''
                answer = iz_telegram.bot_send (line[1],namebot,message_out,markup,0)   




    if send_message == 'Yes':

        message_out = "<b>Ждет отправки ...</b>\n"+message_in        



        db,cursor = iz_func.connect ()
        sql = "INSERT INTO bot_message_send (message,namebot,user_id) VALUES ('{}','{}','{}')".format (message_in,namebot,user_id)
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        from telebot import types 
        markup = types.InlineKeyboardMarkup(row_width=4)
        mn011 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Всем"),callback_data = "add1_"+str(lastid))
        mn012 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Подписчикам"),callback_data = "add2_"+str(lastid))
        mn013 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"В каталог"),callback_data = "add3_"+str(lastid))
        markup.add(mn011)
        markup.add(mn012)
        markup.add(mn013)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)         












