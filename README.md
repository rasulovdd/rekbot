<h1 align="center">rekbot</h1>

## Описание

Бот для работы рекламы

## Стек
Core: python 3, pyTelegramBotAPI <br/>
Database: mysql<br/>

## Установка

1. Скачайте репозиторий<br/>

    ```bash
    git clone https://github.com/rasulovdd/rekbot.git && cd rekbot
    ```

2. Устанавливаем виртуальное окружение<br/>

    ```bash
    apt install -y python3-venv
    ```
    ```bash
    python3 -m venv env
    ```

3. Активируем её <br/>

    ```bash
    source env/bin/activate
    ```

4. Скачиваем и устанавливаем нужные библиотеки<br/>

    ```bash
    pip install -r requirements.txt
    ```

5. Изменить в скрипте mysql-setup.sh следующие параметры: <br/>
    
    Пользователь: bot_user
    Пароль: bot_password1!
    База данных: rekbot

6. Запустить скрипт mysql-setup.sh<br/>
    даем права 
    ```bash
    chmod +x mysql-setup.sh
    ```
    запускаем скрипт
    ```bash
    mysql-setup.sh
    ```

7. Создаем .env файл с вашими данными, можно создать из шаблона и просто поправить поля <br/>

    ```bash
    cp .env.sample .env
    nano .env
    ```

8. Создаем .service файл для вашего бота 
    sudo nano /etc/systemd/system/rekbot.service<br/>

    ```ini
    [Unit]
    Description='Service for rekbot'
    After=network.target

    [Service]
    Type=idle
    Restart=on-failure
    StartLimitBurst=2
    StartLimitInterval=120
    User=root
    ExecStart=/bin/bash -c 'cd ~/rekbot/ && source env/bin/activate && python3 app.py'

    [Install]
    WantedBy=multi-user.target

    ```

9. Включаем сервис и запускаем<br/>

    ```bash
    systemctl enable rekbot.service
    systemctl start rekbot.service
    ```

10. Бот готов к использованию 

## Дополнительно

Чтобы бот мог присылать уведомления, необходимо в .env фале указать ID пользователя (пользователей) в users_id через запятую

пример заполнения .env файла:

    bot_tokken="Токен бота"
    api_tokken="токен доступа к BotAPI"
    #Адрес базы данных
    db_host="127.0.0.1"
    #имя пользователя БД
    db_user="bot_user" 
    #пароль пользователя БД
    db_password="bot_password1!"
    #название БД
    database="rekbot"
    #адрес сервера где будет работать BotAPI
    my_host="10.10.1.111"
    #порт сервера где будет работать BotAPI
    my_port="5010" 
    #список пользователей для уведомления
    users_id="2964812"
    #список пользователей c правами администратора
    admins_id="2964812"
    #статус debug режима
    debug_on=1 


