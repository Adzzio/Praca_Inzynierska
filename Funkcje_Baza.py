from Connect import mydb
from prettytable import PrettyTable
def select_tow():
    cur = mydb.cursor()
    cur.execute("SELECT tow_kod, tow_name, ilo_is,ce FROM tow order by tow_kod desc ;")
    tow = cur.fetchall()
    return tow

def select_tow_where(tow):
    cur = mydb.cursor()
    query_select = 'SELECT tow_kod FROM tow where tow_kod = %s;'
    cur.execute(query_select, tow)
    tow = cur.fetchall()
    if tow != ():
        tow = tow[0]
        tow = tow[0]
        print(tow)
        return tow
    elif tow == ():
        return False


def select_WZ():
    cur = mydb.cursor()
    cur.execute("SELECT wz.idwz, wz.val, odb.name_odb FROM wz INNER JOIN odb ON wz.odb_kod_odb = odb.kod_odb;")
    WZ = cur.fetchall()
    return WZ

def select_WZ_where(WZ):
    cur = mydb.cursor()
    query_select = 'SELECT wz.idwz FROM WZ where wz.idwz = %s;'
    cur.execute(query_select, WZ)
    WZ = cur.fetchall()
    #tow = tow[0]
    #tow = tow[0]
    print(WZ)
    return WZ

def select_PZ():
    cur = mydb.cursor()
    cur.execute("SELECT pz.idpz, pz.val, dst.name_dst FROM pz INNER JOIN dst ON pz.dst_kod_dst = dst.kod_dst;")
    PZ = cur.fetchall()
    return PZ



def select_PZ_where(pz):
    cur = mydb.cursor()
    query_select = 'SELECT pz.idpz FROM pz where pz.idpz = %s;'
    cur.execute(query_select, pz)
    pz = cur.fetchall()
    #tow = tow[0]
    #tow = tow[0]
    #print(PZ)
    return pz

def select_odb_where(kod):
    cur = mydb.cursor()
    query_select = 'SELECT kod_odb FROM odb where kod_odb = %s;'
    cur.execute(query_select, kod)
    odb = cur.fetchall()

    if odb != ():
        odb = odb[0]
        odb = odb[0]
        print(odb)
        return odb
    elif odb == ():
        return False


def select_dst_where(kod):
    cur = mydb.cursor()
    query_select = 'SELECT kod_dst FROM dst where kod_dst = %s;'
    cur.execute(query_select, kod)
    dst = cur.fetchall()
    #print(dst)
    #dst = dst[0]
    #print(dst)
    return dst

def convert_to_dict(tow):
  results = []
  for row in tow:
    results.append({
        "tow_kod": row[0],
        "tow_name": row[1],
        "ilo_is": row[2],
        "ce": row[3],
    })
  return results

def convert_to_dict_odb(odb):
  results = []
  for row in odb:
    results.append({
        "tow_kod": row[0],
        "tow_name": row[1],
        "ilo_is": row[2]
    })
  return results


def convert_to_dict_dst(dst):
  results = []
  for row in dst:
    results.append({
        "tow_kod": row[0],
        "tow_name": row[1],
        "ilo_is": row[2]
    })
  return results

def convert_to_dict_WZ(WZ):
  results = []
  for row in WZ:
    results.append({
        "idwz": row[0],
        "val": row[1],
        "name_odb": row[2]
    })
  return results


def convert_to_dict_PZ(PZ):
  results = []
  for row in PZ:
    results.append({
        "idwz": row[0],
        "val": row[1],
        "name_odb": row[2]
    })
  return results


def delete_tow(tow):
    cur = mydb.cursor()
    query_del = "delete from tow where tow_kod = %s;"
    cur.execute(query_del,tow)
    mydb.commit()

def delete_odb(odb):
    cur = mydb.cursor()
    query_del = "delete from odb where kod_odb = %s;"
    cur.execute(query_del,odb)
    mydb.commit()

def delete_dst(dst):
    cur = mydb.cursor()
    query_del = "delete from dst where kod_dst = %s;"
    cur.execute(query_del,dst)
    mydb.commit()

def delete_WZ(WZ):
    WZ = WZ
    cur = mydb.cursor()
    query_sel2 = "select tow_tow_kod, ilo from wz_p where wz_idwz = %s;"
    query_sel = "select tow_kod, ilo_is from tow where tow_kod = %s;"
    query_upd = "update tow set ilo_is = %s where tow_kod = %s;"
    query_del = "delete from wz where idwz = %s;"
    query_del2 = "delete from wz_p where wz_idwz = %s;"
    cur.execute(query_sel2, WZ)
    wz_p = cur.fetchall()
    print(wz_p)
    for x in wz_p:
        cur.execute(query_sel, x[0])
        tow = cur.fetchall()[0]
        print(tow)
        print(x)
        ilo_is = tow[1] + x[1]
        cur.execute(query_upd, (ilo_is, x[0]))
    cur.execute(query_del2,WZ)
    cur.execute(query_del,WZ)
    mydb.commit()

def delete_PZ(PZ):
    cur = mydb.cursor()
    query_sel2 = "select tow_tow_kod, ilo from pz_p where pz_idpz = %s;"
    query_sel = "select tow_kod, ilo_is from tow where tow_kod = %s;"
    query_upd = "update tow set ilo_is = %s where tow_kod = %s;"
    query_del = "delete from pz where idpz = %s;"
    query_del2 = "delete from pz_p where pz_idpz = %s;"
    cur.execute(query_sel2, PZ)
    pz_p = cur.fetchall()
    # print(len(wz_p))
    for x in pz_p:
        cur.execute(query_sel, x[0])
        tow = cur.fetchall()[0]
        ilo_is = tow[1] - x[1]
        cur.execute(query_upd, (ilo_is, x[0]))
    cur.execute(query_del2, PZ)
    cur.execute(query_del, PZ)
    mydb.commit()


def add_tow(tow_kod, nazwa, ce):
    cur = mydb.cursor()
    tow_is = select_tow_where(tow_kod)
    if tow_is == tow_kod:
        #print('kod towaru juz występuje w bazie')
        x=True
    else:
        query_add = "insert into tow (tow_kod, tow_name, ilo_is, ce) values (%s,%s, 0, %s);"
        cur.execute(query_add, (tow_kod, nazwa, ce))
        mydb.commit()
        x=False
    return x

def display_data_in_table(self, dane_tow):
    table = PrettyTable()
    table.field_names = ["Towar", "Kod", "Ilość", "Cena"]

    for item in dane_tow:
        table.add_row([item['tow_name'], item['tow_kod'], item['ilo_is'], item['ce']])
    return table

def select_tow2():
    dane = select_tow()
    dane_tow = [convert_to_dict(dane) for item in dane]
    dane_tow = dane_tow[0]
    dane_tow = [tuple(d.values()) for d in dane_tow]
    return dane_tow

def select_odb():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM odb order by kod_odb desc ;")
    odb = cur.fetchall()
    return odb


def select_odb2():
    dane = select_odb()
    dane_odb = [convert_to_dict_odb(dane) for item in dane]
    dane_odb = dane_odb[0]
    dane_odb = [tuple(d.values()) for d in dane_odb]
    return dane_odb


def select_dst():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM dst order by kod_dst desc ;")
    dst = cur.fetchall()
    return dst


def select_dst2():
    dane = select_dst()
    dane_dst = [convert_to_dict_dst(dane) for item in dane]
    dane_dst = dane_dst[0]
    dane_dst = [tuple(d.values()) for d in dane_dst]
    return dane_dst

def select_WZ2():
    dane = select_WZ()
    dane_WZ = [convert_to_dict_WZ(dane) for item in dane]
    if len(dane_WZ) == 0:
        pass
    else:
        dane_WZ = dane_WZ[0]
        dane_WZ = [tuple(d.values()) for d in dane_WZ]
    return dane_WZ

def select_PZ2():
    dane = select_PZ()
    dane_PZ = [convert_to_dict_WZ(dane) for item in dane]
    dane_PZ = dane_PZ[0]
    dane_PZ = [tuple(d.values()) for d in dane_PZ]
    return dane_PZ


def add_odb(kod, nazwa, nip):
    cur = mydb.cursor()
    kod_is = select_odb_where(kod)
    if kod_is == kod:
        print('kod towaru juz występuje w bazie')
        x = True
        return x
    else:
        query_add = "insert into odb (kod_odb, name_odb, nip) values (%s,%s,%s);"
        cur.execute(query_add, (kod, nazwa, nip))
        mydb.commit()


def add_dst(kod, nazwa, nip):
    cur = mydb.cursor()
    kod_is = select_dst_where(kod)
    if kod_is == kod:
        x = True
    else:
        query_add = "insert into dst (kod_dst, name_dst, nip) values (%s,%s,%s);"
        cur.execute(query_add, (kod, nazwa, nip))
        mydb.commit()
        x = False
    return x

def tow_edit(kod, nazwa, cena):
    cur = mydb.cursor()
    kod = kod.replace('Kod: ', '')
    queue_update = "update tow set tow_name = %s , ce = %s where tow_kod = %s"
    cur.execute(queue_update, (nazwa, cena, kod))
    mydb.commit()

def dst_edit(kod, nazwa, nip):
    cur = mydb.cursor()
    kod = kod.replace('Kod: ', '')
    queue_update = "update dst set name_dst = %s , nip = %s where kod_dst = %s"
    cur.execute(queue_update, (nazwa, nip, kod))
    mydb.commit()

def odb_edit(kod, nazwa, nip):
    cur = mydb.cursor()
    kod = kod.replace('Kod: ', '')
    queue_update = "update odb set name_odb = %s , nip = %s where kod_odb = %s"
    cur.execute(queue_update, (nazwa, nip, kod))
    mydb.commit()


def add_wz(pozycje,odb):
    cw = 0
    cc = 0
    cur = mydb.cursor()
    query_insert_wz = "insert into wz (odb_kod_odb,dok_id) values (%s, %s)"
    query_insert_wz_p = "insert into wz_p (val,tow_tow_kod,wz_idwz,ilo) values (%s,%s,%s,%s)"
    query_update_tow = "update tow set ilo_is = %s where tow_kod = %s"
    select_tow_ilo = "select ilo_is from tow where tow_kod = %s"
    query_select_wz = "select idwz from wz order by idwz desc"
    query_update_wz = "update wz set val = %s where idwz = %s"
    cur.execute(query_select_wz)
    wz = cur.fetchall()
    print(wz)
    if wz == ():
        wz = 1
    else:
        wz = wz[0]
        wz = wz[0] + 1
    print(wz)
    cur.execute(query_insert_wz, (odb, 'wz'))
    mydb.commit()
    for i in pozycje:
        k = i[0]
        c = i[2]
        j = i[3]
        print(c)
        print(j)
        w = float(c) * float(j)
        cur.execute(select_tow_ilo, k)
        tow_ilo = cur.fetchall()[0]
        tow_ilo_ost = float(tow_ilo[0]) - float(j)
        cw = cw + w
        cc = cc + cw
        print(wz)
        cur.execute(query_insert_wz_p, (w, k, wz, j))
        cur.execute(query_update_tow, (tow_ilo_ost, k))
    cur.execute(query_update_wz, (cc, wz))
    (mydb.commit())


def add_pz(pozycje, dst, tow_ilo_ost=None):
    cw = 0
    cc = 0
    cur = mydb.cursor()
    query_insert_pz = "insert into pz (dst_kod_dst,dok_id,idpz) values (%s, %s, %s)"
    query_insert_pz_p = "insert into pz_p (val,tow_tow_kod,pz_idpz,ilo) values (%s,%s,%s,%s)"
    query_update_tow = "update tow set ilo_is = %s where tow_kod = %s"
    select_tow_ilo = "select ilo_is from tow where tow_kod = %s"
    query_select_pz = "select idpz from pz order by idpz desc"
    query_update_pz = "update pz set val = %s where idpz = %s"
    cur.execute(query_select_pz)
    pz = cur.fetchall()
    print(pz)
    if pz == ():
        pz = 1
    else:
        pz = pz[0]
        pz = pz[0] + 1
    print(pz)
    cur.execute(query_insert_pz, (dst, 'pz', pz))
    mydb.commit()
    for i in pozycje:
        k = i[0]
        c = i[2]
        j = i[3]
        print(c)
        print(j)
        w = float(c) * float(j)
        cur.execute(select_tow_ilo, k)
        tow_ilo = cur.fetchall()[0]
        tow_ilo_ost = float(tow_ilo[0]) + float(j)
        cw = cw + w
        cc = cc + cw
        print(pz)
        cur.execute(query_insert_pz_p, (w, k, pz, j))
        cur.execute(query_update_tow, (tow_ilo_ost, k))
    cur.execute(query_update_pz, (cc, pz))
    (mydb.commit())


def ilo_check(tow):
    cur = mydb.cursor()
    query_select_ilo = "select ilo_is from tow where tow_kod = %s"
    cur.execute(query_select_ilo, tow)
    ilo = cur.fetchall()
    if ilo == ():
        ilo = 1
    else:
        ilo = ilo[0]
        ilo = ilo[0]
    return ilo

def select_pz_edit(pz):
    cur = mydb.cursor()
    query_select_pz = "select dst_kod_dst from pz where idpz = %s"
    print(pz)
    query_select_pz_p = "select ilo, val, tow_tow_kod, tow.tow_name, tow.ce from pz_p left join tow on pz_p.tow_tow_kod = tow.tow_kod where pz_idpz = %s"
    cur.execute(query_select_pz, pz)
    x_pz = cur.fetchall()
    cur.execute(query_select_pz_p, pz)
    y_pz = cur.fetchall()
    return x_pz, y_pz

def select_wz_edit(wz):
    cur = mydb.cursor()
    query_select_wz = "select odb_kod_odb from wz where idwz = %s"
    print(wz)
    query_select_wz_p = "select ilo, val, tow_tow_kod, tow.tow_name, tow.ce from wz_p left join tow on wz_p.tow_tow_kod = tow.tow_kod where wz_idwz = %s"
    cur.execute(query_select_wz, wz)
    x_wz = cur.fetchall()
    cur.execute(query_select_wz_p, wz)
    y_wz = cur.fetchall()
    return x_wz, y_wz

def del_pz_p(PZ):
    cur = mydb.cursor()
    query_del2 = "delete from pz_p where pz_idpz = %s;"
    cur.execute(query_del2, PZ)
    mydb.commit()

def del_wz_p(WZ):
    cur = mydb.cursor()
    query_del2 = "delete from wz_p where wz_idwz = %s;"
    cur.execute(query_del2, WZ)
    mydb.commit()


def edit_pz(pozycje, pz):
    cw = 0
    cc = 0
    cur = mydb.cursor()
    query_insert_pz_p = "insert into pz_p (val,tow_tow_kod,pz_idpz,ilo) values (%s,%s,%s,%s)"
    query_update_towar = "update tow set ilo_is = %s where tow_kod = %s"
    select_tow_ilo = "select ilo_is from tow where tow_kod = %s"
    query_select_pz = "select idpz from pz order by idpz desc"
    query_update_pz = "update pz set val = %s where idpz = %s"
    cur.execute(query_select_pz)
    print(pozycje)
    for i in pozycje:
        #print(i)
        k = i[2]
        c = i[4]
        j = i[0]
        w = float(c) * float(j)
        cur.execute(select_tow_ilo, k)
        tow_ilo = cur.fetchall()[0]
        tow_ilo_ost = float(tow_ilo[0]) + float(j)
        cw = cw + w
        cc = cc + cw
        cur.execute(query_insert_pz_p, (w, k, pz, j))
        cur.execute(query_update_towar, (tow_ilo_ost, k))
    cur.execute(query_update_pz, (cc, pz))
    mydb.commit()


def edit_wz(pozycje, wz):
    cw = 0
    cc = 0
    cur = mydb.cursor()
    query_insert_pz_p = "insert into wz_p (val,tow_tow_kod,pz_idpz,ilo) values (%s,%s,%s,%s)"
    query_update_towar = "update tow set ilo_is = %s where tow_kod = %s"
    select_tow_ilo = "select ilo_is from tow where tow_kod = %s"
    query_select_pz = "select idwz from wz order by idwz desc"
    query_update_pz = "update wz set val = %s where idwz = %s"
    cur.execute(query_select_pz)
    print(pozycje)
    for i in pozycje:
        #print(i)
        k = i[2]
        c = i[4]
        j = i[0]
        w = float(c) * float(j)
        cur.execute(select_tow_ilo, k)
        tow_ilo = cur.fetchall()[0]
        tow_ilo_ost = float(tow_ilo[0]) + float(j)
        cw = cw + w
        cc = cc + cw
        cur.execute(query_insert_pz_p, (w, k, wz, j))
        cur.execute(query_update_towar, (tow_ilo_ost, k))
    cur.execute(query_update_pz, (cc, wz))
    mydb.commit()

def zamien_przecinek_na_kropke(tekst):
    if ',' in tekst:
        tekst = tekst.replace(',', '.')
    return tekst