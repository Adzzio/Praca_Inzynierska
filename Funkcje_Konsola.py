from Connect import cur, mydb
from shlex import join
import pymysql


def spr_1(x, query_select):
    try:
        cur.execute(query_select, x)
        x_c = cur.fetchall()[0]
        x_c = join([value for value in x_c.values()])
        return x_c
    except IndexError:
        pass

def spr_2(x, query_select):
    try:
        cur.execute(query_select, x)
        x_c = cur.fetchall()[0]
        x_c = join(str([value for value in x_c.values()]))
        return x_c
    except IndexError:
        pass

def spr_ilo(x, query_select):
    try:
        cur.execute(query_select, x)
        x_c = cur.fetchall()[0]
        x_c = x_c.get('ilo_is')
        return x_c
    except IndexError:
        pass


def select_tow():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM tow")
    tow = cur.fetchall()
    print('Kod_twoaru, Nazwa, Ilość, Cena')
    for t in tow:
        print(t)
        print(type(t))

#select_tow()

def select_dst():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM dst")
    dst = cur.fetchall()
    print('Lp, Nazwa, Nip')
    for d in dst:
        print(d)

#select_dst()

def select_odb():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM odb")
    odb = cur.fetchall()
    print('Lp, Nazwa, Nip')
    for o in odb:
        print(o)

#select_odb()

def dst_add():
    print('Dodawanie dostawcy do kartoteki')
    dst_kod = input('Podaj kod dostawcy: ')
    cur = mydb.cursor()
    query_select = "select kod_dst from dst where kod_dst = %s"
    while dst_kod == '':
        print('kod dostawcy nie może być pusta')
        dst_kod = input('Podaj kod dostawcy: ')
    tow_is = spr_1(dst_kod, query_select)
    while dst_kod == tow_is:
        print('Taki kod już jest w kartotece')
        dst_kod = input('Podaj kod dostawcy: ')
    name = input('Podaj nazwe dostawcy: ')
    nip = input('Podaj nip dostawcy: ')
    query_insert = "insert into dst (kod_dst,name_dst,nip) values (%s, %s, %s)"
    try:
        cur.execute(query_insert, (dst_kod, name, nip))
        print(f'Dostawca {dst_kod} został dodany do bazy')
        mydb.commit()
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            print('Taki kod już jest w kartotece')
            dst_add()
        else:
            raise

#dst_add()

def odb_add():
    print('Dodawanie odbiorcy do kartoteki')
    odb_kod = input('Podaj kod odbiorcy: ')
    cur = mydb.cursor()
    query_select = "select kod_odb from odb where kod_odb = %s"
    while odb_kod == '':
        print('kod odbiorcy nie może być pusta')
        odb_kod = input('Podaj kod odbiorcy: ')
    tow_is = spr_1(odb_kod, query_select)
    while odb_kod == tow_is:
        print('Taki kod już jest w kartotece')
        odb_kod = input('Podaj kod odbiorcy: ')
    name = input('Podaj nazwe odbiorcy: ')
    nip = input('Podaj nip odbiorcy: ')
    query_insert = "insert into odb (kod_odb,name_odb,nip) values (%s, %s, %s)"
    try:
        cur.execute(query_insert, (odb_kod, name, nip))
        print(f'Dostawca {odb_kod} został dodany do bazy')
        mydb.commit()
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            print('Taki kod już jest w kartotece')
            odb_add()
        else:
            raise

#odb_add()

def tow_add():
    print('Dodawanie towaru do kartoteki')
    tow_kod = input('Podaj kod towaru: ')
    cur = mydb.cursor()
    query_select = "select tow_kod from tow where tow_kod = %s"
    while tow_kod == '':
        print('kod towaru nie może być pusta')
        tow_kod = input('Podaj kod towaru: ')
    tow_is = spr_1(tow_kod, query_select)
    while tow_kod == tow_is:
        print('Taki kod już jest w kartotece')
        tow_kod = input('Podaj kod towaru: ')
    name = input('Podaj nazwe towaru: ')
    query_insert = "insert into tow (tow_kod,tow_name) values (%s, %s)"
    try:
        cur.execute(query_insert, (tow_kod,name))
        print(f'Dostawca {tow_kod} został dodany do bazy')
        mydb.commit()
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            print('Taki kod już jest w kartotece')
            tow_add()
        else:
            raise


#tow_add()

def wyst_pz():
    print('Wystawienie dokumentu pz')
    dst_kod = input('Podaj kod dostawcy: ')
    dst_kod = int(dst_kod)
    query_select = "select kod_dst from dst where kod_dst = %s"
    dst_kod_c = spr_2(dst_kod,query_select)
    while dst_kod == ''  or  dst_kod_c == None:
        if dst_kod == '':
            print('Kod dostawcy nie moze być pusty')
            dst_kod = int(input('Podaj kod dostawcy: '))
        elif dst_kod_c == None:
            try:
                print('Kod dostawcy nie występuje w bazie')
                dst_kod = int(input('Podaj inny kod dostawcy: '))
                dst_kod_c = spr_2(dst_kod, query_select)
            except:
                pass


    print('Dodaj towar = 1')
    print('Zakoncz dokument = 2')
    op = int(input(''))
    pz_p = []
    pz_p_i = []
    pz_p_v = []
    while op != 2:
        match op:
            case 1:
                tow_kod = input('Podaj kod towaru: ')
                query_select = "select tow_kod from tow where tow_kod = %s"
                tow_is = spr_1(tow_kod, query_select)
                while tow_kod == '' or tow_is == None:
                    if tow_kod == '':
                        print('kod towaru nie może być pusta')
                    elif tow_is == None:
                            print('Taki kod nie jest w kartotece')
                            tow_kod = input('Podaj kod towaru: ')
                            tow_is = spr_1(tow_kod, query_select)
                tow_ilo = input('Podaj ilość towaru: ')
                while tow_ilo == '' or tow_ilo == 0:
                    if tow_ilo == '':
                        print('ilość towaru nie może być pusta')
                        tow_ilo = input('Podaj kod towaru: ')
                    elif tow_ilo == 0:
                        print('ilość towaru nie może być 0')
                        tow_ilo = input('Podaj kod towaru: ')
                tow_val = input('Podaj wartość towaru: ')
                while tow_val == '' or tow_val == 0:
                    if tow_val == '':
                        print('Wartość towaru nie może być pusta')
                        tow_val = input('Podaj kod towaru: ')
                    elif tow_val == 0:
                        print('Wartość towaru nie może być 0')
                        tow_val = input('Podaj kod towaru: ')

                pz_p.append(tow_kod)
                print(pz_p)
                pz_p_i.append(tow_ilo)
                print(pz_p_i)
                pz_p_v.append(tow_val)
                print(pz_p_v)
                print('Dodaj towar = 1')
                print('Zakoncz dokument = 2')
                op = int(input(''))


    query_select = "select idpz from pz order by idpz desc "
    cur.execute(query_select)
    x_c = cur.fetchall()[0]
    x_c = x_c.get('idpz')
    if x_c == ():
        pz_id = 0
    else:
        pz_id = int(x_c) + 1
    query_insert = "insert into pz (idpz,dst_kod_dst,dok_id) values (%s,%s,%s)"
    cur.execute(query_insert,(pz_id,dst_kod,'pz'))

    query_insert = "insert into pz_p (tow_tow_kod,pz_idpz,ilo,val) values (%s,%s,%s,%s)"
    query_update = "update tow set ilo_is = %s, ce = %s where tow_kod = %s"
    query_select = "select ilo_is from tow where tow_kod = %s"
    pz_len = len(pz_p)
    val = 0
    for i in range(pz_len):
        i1 = pz_p[i]
        i2 = pz_p_i[i]
        i3 = pz_p_v[i]
        val = val + (int(i2) * int(i3))
        cur.execute(query_select, i1)
        x_c = cur.fetchall()[0]
        x_c = x_c.get('ilo_is')
        if x_c == None:
            x_c = 0
        x_c = int(x_c) + int(i2)
        cur.execute(query_update, (x_c,i3,i1))
        cur.execute(query_insert, (i1, pz_id, i2, i3))
    query_update = "update pz set val = %s where idpz = %s"
    cur.execute(query_update, (val,pz_id))
    mydb.commit()


#wyst_pz()





def wyst_wz():
    print('Wystawienie dokumentu wz')
    odb_kod = input('Podaj kod odbiorcy: ')
    odb_kod = int(odb_kod)
    query_select = "select kod_odb from odb where kod_odb = %s"
    odb_kod_c = spr_2(odb_kod,query_select)
    while odb_kod == ''  or  odb_kod_c == None:
        if odb_kod == '':
            print('Kod odbiorcy nie moze być pusty')
            odb_kod = int(input('Podaj kod odbiorcy: '))
        elif odb_kod_c == None:
            try:
                print('Kod odbiorcy nie występuje w bazie')
                odb_kod = int(input('Podaj inny kod odbiorcy: '))
                odb_kod_c = spr_2(odb_kod, query_select)
            except:
                pass


    print('Dodaj towar = 1')
    print('Zakoncz dokument = 2')
    op = int(input(''))
    wz_p = []
    wz_p_i = []
    wz_p_v = []
    while op != 2:
        match op:
            case 1:
                tow_kod = input('Podaj kod towaru: ')
                query_select = "select tow_kod from tow where tow_kod = %s"
                query_select_ilo = "select ilo_is from tow where tow_kod = %s"
                query_select_val = "select ce from tow where tow_kod = %s"
                tow_is = spr_1(tow_kod, query_select)
                ilo_is = float(spr_ilo(tow_kod,query_select_ilo))
                while tow_kod == '' or tow_is == None or ilo_is <= 0:
                    if tow_kod == '':
                        print('kod towaru nie może być pusta')
                    elif tow_is == None:
                            print('Taki kod nie jest w kartotece')
                            tow_kod = input('Podaj kod towaru: ')
                            tow_is = spr_1(tow_kod, query_select)
                    elif ilo_is <= 0:
                        print('Nie masz tego towaru na stanie')
                        pass
                tow_ilo = float(input('Podaj ilość towaru: '))
                while tow_ilo == '' or tow_ilo == 0 or ilo_is < tow_ilo:
                    if tow_ilo == '':
                        print('ilość towaru nie może być pusta')
                        tow_ilo = input('Podaj ilość towaru: ')
                    elif tow_ilo == 0:
                        print('ilość towaru nie może być 0')
                        tow_ilo = input('Podaj ilość towaru: ')
                    elif ilo_is < tow_ilo:
                        print('Nie masz tyle togo towaru na stanie')
                        print('Ilość towaru na stanie jest równa: ' + ilo_is)
                        tow_ilo = input('Podaj ilość towaru: ')
                tow_val = input('Podaj wartość towaru: ')
                while tow_val == '' or tow_val == 0:
                    if tow_val == '':
                        print('Wartość towaru nie może być pusta')
                        tow_val = input('Podaj kod towaru: ')
                    elif tow_val == 0:
                        print('Wartość towaru nie może być 0')
                        tow_val = input('Podaj kod towaru: ')


                wz_p.append(tow_kod)
                print(wz_p)
                wz_p_i.append(tow_ilo)
                print(wz_p_i)
                wz_p_v.append(tow_val)
                print(wz_p_v)
                print('Dodaj towar = 1')
                print('Zakoncz dokument = 2')
                op = int(input(''))


    query_select = "select idwz from wz order by idwz desc "
    cur.execute(query_select)
    x_c = cur.fetchall()
    if x_c == ():
        x_c = [{'idwz':0}]
    x_c = x_c[0]
    x_c = x_c.get('idwz')
    if x_c == ():
        wz_id = 0
    else:
        wz_id = int(x_c) + 1
    query_insert = "insert into wz (idwz,odb_kod_odb,dok_id) values (%s,%s,%s)"
    cur.execute(query_insert,(wz_id,odb_kod,'wz'))

    query_insert = "insert into wz_p (tow_tow_kod,wz_idwz,ilo,val) values (%s,%s,%s,%s)"
    query_update = "update tow set ilo_is = %s, ce = %s where tow_kod = %s"
    query_select = "select ilo_is from tow where tow_kod = %s"
    wz_len = len(wz_p)
    val = 0
    for i in range(wz_len):
        i1 = wz_p[i]
        i2 = wz_p_i[i]
        i3 = wz_p_v[i]
        val = val + (int(i2) * int(i3))
        cur.execute(query_select, i1)
        x_c = cur.fetchall()[0]
        x_c = x_c.get('ilo_is')
        if x_c == None:
            x_c = 0
        x_c = int(x_c) - int(i2)
        cur.execute(query_update, (x_c,i3,i1))
        cur.execute(query_insert, (i1, wz_id, i2, i3))
    query_update = "update wz set val = %s where idwz = %s"
    cur.execute(query_update, (val,wz_id))
    mydb.commit()


#wyst_wz()