from multiprocessing import connection

import database_ops as dbo
import db_conn as dbc
import urllib.request
import os


def download_image(url, img_name):
    try:
        if os.path.exists(img_name):
            return img_name

        urllib.request.urlretrieve(url, img_name)

        return img_name
    except:
        return 'error_img.jpg'


def on_login_admin(admn_id, pswd):
    connection_1 = dbc.connect_to_db()
    cursor = connection_1.cursor()
    details = []
    db_details = dbo.verify_admin(admn_id, pswd, cursor)
    if db_details[0] != 0:
        details.append("1")
    else:
        if db_details[0] == 1:
            details.append("Database error occured,Please try again later")
        elif db_details[0] == 2:
            details.append("UserID is incorrect ")
        elif db_details[0] == 3:
            details.append("Password is incorrect ")
        elif db_details[0] == 0:
            details.append("Login Successful")
            details.append(db_details[1])
    connection_1.close()
    return details


def on_login_client(client_id, pswd):
    connection_1 = dbc.connect_to_db()
    cursor = connection_1.cursor()
    details = []
    db_details = dbo.verify_client(client_id, pswd, cursor)
    if db_details[0] != 0:
        details.append("1")
    else:
        if db_details[0] == 1:
            details.append("Database error occured,Please try again later")
        elif db_details[0] == 2:
            details.append("UserID is incorrect ")
        elif db_details[0] == 3:
            details.append("Password is incorrect ")
        elif db_details[0] == 0:
            details.append("Login Successful")
            details.append(db_details[1])
    connection_1.close()
    return details


def generate_student_list():
    connection_1 = dbc.connect_to_db()
    cursor = connection_1.cursor()
    db_details = dbo.get_student_list(cursor)
    return db_details
    connection_1.close()


def generate_student_list_by_id(search_str=''):
    connection = dbc.connect_to_db()
    cursor = connection.cursor()
    db_details = dbo.get_student_list(cursor, 1, search_str, 1, 0)
    return db_details
    connection.close()


def generate_student_list_by_name(search_str=''):
    connection = dbc.connect_to_db()
    cursor = connection.cursor()
    db_details = dbo.get_student_list(cursor, 1, search_str, 0, 1)
    return db_details
    connection.close()


def send_student_list(sb='', search_str=''):
    if sb == '' or search_str == '':
        x = generate_student_list()
    else:
        if sb == 'n':
            x = generate_student_list_by_name(search_str)
        else:
            x = generate_student_list_by_id(search_str)
    return x

