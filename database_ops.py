"""this py file has all the functions to extract cloud details"""



import db_conn



    
    

def verify_admin(admn_id , pswd,cursor):
    """
    error codes:
    1 : others
    2 : id incorrect
    3 : password incorrect

    0 : login successful
    """
    ad_l = []
    
    try:
        q_str = 'select * from admin_login_details where userid = ' + '"'+str(admn_id)+'"'
        rows_cnt = cursor.execute(q_str)
        a = cursor.fetchall()
        x = get_admin_detail(admn_id,cursor)
       
        fetch = 's'
    except:
        fetch  = 'f'
        
    if fetch == 's':
        if rows_cnt > 0:
            aid = 'c'
            
            if a[0]['password'] == pswd:
                ap = 'c'
                ad_l.append(0)
                if x[0] == 0:
                    ad_l.append(x[1])
                return ad_l
            else:
                ap = 'i'
                ad_l.append(3)
                return ad_l
        else:
            aid = 'i'
            ad_l.append(2)
            return ad_l
    else:
        ad_l.append(1)
        return ad_l
   
def verify_client(clnt_id , pswd,cursor):
    """
    error codes:
    1 : others
    2 : id incorrect
    3 : password incorrect

    0 : login successful
    """

    cd_l = []
    try:
        q_str = 'select * from client_login_details where userid = ' + '"'+str(clnt_id)+'"'
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        x = get_client_detail(clnt_id,cursor)
        
        fetch = 's'
    except:
        fetch  = 'f'
        
    if fetch == 's':
        if rows_cnt > 0:
            cid = 'c'
            
            if c[0]['password'] == pswd:
                ap = 'c'
                cd_l.append(0)
                if x[0] == 0:
                    cd_l.append(x[1])
                return cd_l
            else:
                cp = 'i'
                cd_l.append(3)
                return cd_l
        else:
            cid = 'i'
            cd_l.append(2)
            return cd_l
    else:
        cd_l.append(1)
        return cd_l
   


def get_admin_detail(admn_id,cursor):
    apd_l = []
    try:
        q_str = 'select * from admin_personal_details where userid = ' + '"'+str(admn_id)+'"'
        rows_cnt = cursor.execute(q_str)
        a = cursor.fetchall()
        fetch = 's'
    except:
        fetch  = 'f'
    if fetch == 's':
        apd_l.append(0)
        apd_l.append(a)
        return apd_l
    else:
        apd_l.append(1)
        return apd_l
    

def get_client_detail(clnt_id,cursor):
    cpd_l = []
    try:
        q_str = 'select * from client_personal_details where userid = ' + '"'+str(clnt_id)+'"'
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        fetch = 's'
    except:
        fetch  = 'f'
    if fetch == 's':
        cpd_l.append(0)
        cpd_l.append(c)
        return cpd_l
    else:
        cpd_l.append(1)
        return cpd_l 


def get_student_list(cursor,f = 0 , search_string = '' , sbi = 0  , sbn = 0):

    cl_l = []
    q_str = 'select * from client_personal_details'

    if(search_string == '' or f ==0):
        pass
    else:
        if(sbi == 0 and sbn == 0):
            sbn = 1
        if(sbn == 1):
            q_str = q_str + (' where name like "{}%"').format(search_string)
        elif(sbi == 1):
            q_str = q_str + (' where userid = "{}"').format(search_string)
    try:
        
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        fetch = 's'
    except:
        fetch  = 'f'
    if fetch == 's':
        cl_l.append(0)
        cl_l.append(c)
        return cl_l
    else:
        cl_l.append(1)
        return cl_l 
    
def get_transactions(cursor,bf = 0 ,sf = 0 ,dft =0, sbs = 0 , stid = '' ,sba = 0, admn_id = '', df = '',dt ='',status = ''):
    tl_l = []
    q_str = 'select * from transactions'
    cf = 0
    if bf==1 and sbs==1 and stid!='':
        q_str = q_str +  (' where client_id = "{}"').format(stid)
        cf=1
    if bf==1 and sba == 1 and admn_id !='':
        if cf==1:
            q_str = q_str +  (' and approver = "{}"').format(admn_id)

        else:
            q_str = q_str +  (' where approver = "{}"').format(admn_id)
            cf=1
    if sf==1 and status!='':
        if cf==1:
            q_str = q_str +  (' and approved = "{}"').format(status)
        else:
            q_str = q_str +  (' where approved = "{}"').format(status)
            cf =1 

    if dft == 1 and df != '':
        if dt == '':
            if cf == 1:
                q_str = q_str + (' and date_time >= "{}"').format(df)
            else:
                q_str = q_str + (' where date_time >= "{}"').format(df)
                cf=1
        else:
            if cf == 1:
                q_str = q_str + (' and date_time >= "{}" or date_time <= "{}"').format(df,dt)
            else:
                q_str = q_str + (' where date_time >= "{}" or date_time <= "{}"').format(df,dt)
                cf=1
        
        
        

    try:
        print(q_str)
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        fetch = 's'
    except:
        
        fetch  = 'f'
    if fetch == 's':
        tl_l.append(0)
        tl_l.append(c)
        return tl_l
    else:
        tl_l.append(1)
        return tl_l 
    


def get_approvals(cursor,bf=0,sf = 0,tf=0,dft=0,sbs=0,clnt_id = '', sba = 0 , admin_id='',status = '',tid = '',df='',dt=''):
    al_l = []
    q_str = 'select * from approvals'

    if ((clnt_id == '' and admn_id == '' and df == '' )or bf ==0)  and ( sf == 0 or status == '') and ( tf == 0 or tid =='') and (df == 0 or df ==''):
        pass
    else:
        cf = 0
        if(sbs == 0 and sba == 0 and bf ==1):
            sbs = 1
        if(sbs == 1 and bf==1 and clnt_id != ''):
            q_str = q_str + (' where requester_id = "{}"').format(clnt_id)
            cf = 1
        if(sba == 1 and bf ==1 and admin_id !=''):
            if cf ==1:
                q_str = q_str + (' and approver_id = "{}"').format(admn_id)
                cf = 1
            else:
                q_str = q_str + (' where approver_id = "{}"').format(admn_id)
                cf = 1
        if(sf ==1 and status !=''):
            if cf ==1:
                q_str = q_str + (' and approved = "{}"').format(status)
                cf = 1
            else:
                q_str = q_str + (' where approved = "{}"').format(status)
                cf = 1
        if(tf ==1 and tid !=''):
            if cf ==1:
                q_str = q_str + (' and tid = "{}"').format(tid)
                cf = 1
            else:
                q_str = q_str + (' where tid = "{}"').format(tid)
                cf = 1

        if(dft ==1 and df !=''):
            if cf ==1:
                if dt == '':
                    q_str = q_str + (' and posted_on >= "{}"').format(df)
                    cf=1
                else:
                    q_str = q_str + (' and posted_on >= "{}" and posted_on <= "{}"').format(df,dt)
                    cf = 1
            else:
                if dt == '':
                    q_str = q_str + (' where posted_on >= "{}" ').format(df,dt)
                    cf=1
                else:
                    q_str = q_str + (' where posted_on >= "{}" and posted_on <= "{}"').format(df,dt)
                    cf = 1
            
    try:
        
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        fetch = 's'
    except:
        fetch  = 'f'
    if fetch == 's':
        al_l.append(0)
        al_l.append(c)
        return al_l
    else:
        al_l.append(1)
        return al_l 

#try catch run query block

def run_query(cursor,q_str):
    ql_l = []
    try:
        
        rows_cnt = cursor.execute(q_str)
        c = cursor.fetchall()
        fetch = 's'
    except:
        fetch  = 'f'
    if fetch == 's':
        ql_l.append(0)
        ql_l.append(c)
        return ql_l
    else:
        ql_l.append(1)
        return ql_l 

#admin_login_details

def fecth_admin_login_detail(cursor,userid=''):
    q_str = 'select * from admin_login_details'
    
    if userid != '' :
        q_str = q_str +( ' where userid = "{}"').format(userid)
    return run_query(cursor,q_str)

#admin_login_details_update
def admin_login_details_update(cursor,userid='',aid=''):
    q_str = 'select * from admin_login_details_update'
    cf=0
    if userid != '' :
        q_str = q_str +( ' where userid = "{}"').format(userid)
        cf=1
    if aid != '':
        if cf == 1 :
            q_str = q_str +( ' and aid = "{}"').format(aid)
        else:
             q_str = q_str +( ' where aid = "{}"').format(aid)
    print(q_str)
    return run_query(cursor,q_str)

#admin_personal_details_update

def admin_personal_details_update(cursor,userid='',aid=''):
    q_str = 'select * from admin_personal_details_update'
    cf=0
    if userid != '' :
        q_str = q_str +( ' where userid = "{}"').format(userid)
        cf=1
    if aid != '':
        if cf == 1 :
            q_str = q_str +( ' and aid = "{}"').format(aid)
        else:
             q_str = q_str +( ' where aid = "{}"').format(aid)
    print(q_str)
    return run_query(cursor,q_str)
#client_login_details
def fecth_client_login_detail(cursor,userid=''):
    q_str = 'select * from client_login_details'
    
    if userid != '' :
        q_str = q_str +( ' where userid = "{}"').format(userid)
    return run_query(cursor,q_str)
#client_login_details_update
def client_login_details_update(cursor,userid='',aid=''):
    q_str = 'select * from client_login_details_update'
    cf=0
    if userid != '' :
        q_str = q_str +( ' where userid = "{}"').format(userid)
        cf=1
    if aid != '':
        if cf == 1 :
            q_str = q_str +( ' and aid = "{}"').format(aid)
        else:
             q_str = q_str +( ' where aid = "{}"').format(aid)
    print(q_str)
    return run_query(cursor,q_str)







    
    
   

