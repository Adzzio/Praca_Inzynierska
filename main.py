import pymysql
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from Funkcje_Baza import *
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        button1 = MDRaisedButton(text='Towary')
        button1.bind(on_press=self.tow_menu)

        button2 = MDRaisedButton(text='WZ')
        button2.bind(on_press=self.WZ_menu)

        button3 = MDRaisedButton(text='PZ')
        button3.bind(on_press=self.PZ_menu)

        button4 = MDRaisedButton(text='Dostawcy')
        button4.bind(on_press=self.Dst_menu)

        button5 = MDRaisedButton(text='Odbiorcy')
        button5.bind(on_press=self.Odb_menu)

        button6 = MDRaisedButton(text='Zamknij Program')
        button6.bind(on_press=self.close_program)

        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)
        layout.add_widget(button6)
        self.message_label = MDLabel(text='', size = (50,50))
        layout.add_widget(self.message_label)
        self.add_widget(layout)

    def tow_menu(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'tow_select'


    def WZ_menu(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'menu_WZ'

    def PZ_menu(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'menu_PZ'

    def Dst_menu(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'menu_dst'

    def Odb_menu(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'menu_odb'

    def close_program(self, instance):
        self.message_label.text = 'Zamknij Program'
        App.get_running_app().stop()

class EditScreenTow(Screen):

    def __init__(self, **kwargs ):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        #self.menu_tow = menu_tow

        okno = MDLabel(text='Edycja Towaru')
        self.kod = MDLabel(text='', size = (5,5))
        self.nazwa = MDTextField(hint_text='Nazwa', text='')
        self.cena = MDTextField(hint_text='Cena', text='')

        layout.add_widget(okno)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.cena)

        button1 = MDRaisedButton(text='Potwierdz Edycje')
        button1.bind(on_press=self.tow_edit)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def tow_edit(self, instance):
        tow_kod = self.kod.text
        nazwa = self.nazwa.text
        ce = self.cena.text
        ce = zamien_przecinek_na_kropke(ce)
        self.kod.text = ''
        self.nazwa.text = ''
        self.cena.text = ''
        ce = round(float(ce),2)
        tow_edit(tow_kod, nazwa, ce)
        self.show_alert_dialog(instance, 'Towar ', tow_kod, ' został zmodyfikowany')
        self.go_back(instance)
        for d in self.menu_tow.dane_tow:
            k, n, i, c = d
            self.menu_tow.table.remove_row((
                str(k), str(n), str(i), str(c)
            ))

        self.menu_tow.dane_tow = select_tow2()
        for d in self.menu_tow.dane_tow:
            k, n, i, c = d
            c = round(c, 2)
            self.menu_tow.table.add_row((
                str(k), str(n), str(i), str(c)
            ))
        self.menu_tow.t2 = []

    def show_alert_dialog(self, instance, text, towar, text2):
        self.dialog = MDDialog(
            text=text + towar + text2,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'tow_select'

class AddScreenTow(Screen):
    def __init__(self,menu_tow, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.menu_tow = menu_tow

        okno = MDLabel(text='Dodanie Towaru')
        self.text1 = MDTextField(hint_text='Kod')
        self.text2 = MDTextField(hint_text='Nazwa')
        self.text3 = MDTextField(hint_text='Cena')

        layout.add_widget(okno)
        layout.add_widget(self.text1)
        layout.add_widget(self.text2)
        layout.add_widget(self.text3)

        button1 = MDRaisedButton(text='Dodaj')
        button1.bind(on_press=self.tow_add)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def tow_add(self, instance):
        tow_kod = self.text1.text
        nazwa = self.text2.text
        ce = self.text3.text
        ce = zamien_przecinek_na_kropke(ce)
        x = add_tow(tow_kod, nazwa, ce)
        if x == True:
            self.show_alert_dialog(instance, 'Taki towar już iztnieje w bazie')
        else:
            self.show_alert_dialog(instance, 'towar zostal dodany do bazy')
            self.go_back(instance)
            
            for d in self.menu_tow.dane_tow:
                k, n, i, c = d
                self.menu_tow.table.remove_row((
                    str(k), str(n), str(i), str(c)
                ))

            dane_tow = select_tow2()
            for d in dane_tow:
                k, n, i, c = d
                self.menu_tow.table.add_row((
                    str(k), str(n), str(i), str(c)
                ))
        self.text1.text = ''
        self.text2.text = ''
        self.text3.text = ''


    def show_alert_dialog(self, instance,text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'tow_select'

class TowSelectScreen(Screen):
    t = []
    t2 = []
    kod = ''
    cena = ''
    nazwa = ''
    dane_edit = None
    def __init__(self,dane_edit, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dane_edit = dane_edit

        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Ilość", dp(30)),
                ("Cena", dp(30))
            ],
        )
        self.dane_tow = select_tow2()

        for d in self.dane_tow:
            k, n, i, c = d
            self.table.add_row((
                str(k), str(n), str(i), str(c)
            ))
        layout.add_widget(self.table)

        # Bind tabel
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

        # Przycisk usuń
        del_button = MDRaisedButton(text="Usun Zaznaczone", height=1)
        del_button.bind(on_press=self.delete)
        layout.add_widget(del_button)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Dodaj towar", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk edytuj
        edit_button = MDRaisedButton(text="Edytuj towar", height=1)
        edit_button.bind(on_press=self.edit)
        layout.add_widget(edit_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'main_menu'

    def delete(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            for i in self.t:
                try:
                    delete_tow(i)
                except pymysql.err.IntegrityError as e:
                    if e.args[0] == 1451:
                        self.show_alert_dialog(instance, 'Ten towar jest na dokumencie')
                    else:
                        raise


        for d in self.dane_tow:
            k, n, i, c = d
            self.table.remove_row((
                str(k), str(n), str(i), str(c)
            ))
        dane_tow = select_tow2()
        for d in dane_tow:
            k, n, i, c = d
            self.table.add_row((
                str(k), str(n), str(i), str(c)
            ))
        self.t = []


    def add(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'add_tow'

    def edit(self, instance):
        if len(self.t3) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            self.manager.transition = SlideTransition(direction='left', duration=0.50)
            self.manager.current = 'edit_tow'
            self.dane_edit.kod.text = 'Kod: ' + self.t3[0]
            self.dane_edit.nazwa.text = self.t3[1]
            self.dane_edit.cena.text = self.t3[3]

    def show_alert_dialog(self, instance,text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)


    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

            self.t3 = self.t2[0]
            print(self.t2)
            print(self.t3)

class TowSelectScreenToPZ(Screen):
    t = []
    t2 = []
    kod = ''
    cena = ''
    nazwa = ''
    dane_edit = None
    dst = ''
    def __init__(self, add_pz, add_wz, edit_pz, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_pz = add_pz
        self.add_wz = add_wz
        self.edit_pz = edit_pz

        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli
        self.table = MDDataTable(
            use_pagination=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Ilość", dp(30)),
                ("Cena", dp(30))
            ],
        )
        self.dane_tow = select_tow2()

        for d in self.dane_tow:
            k, n, i, c = d
            self.table.add_row((
                str(k), str(n), str(i), str(c)
            ))
        layout.add_widget(self.table)

        # Bind tabel
        self.table.bind(on_row_press=self.do_doc)



        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)


    def do_doc(self, instance_table, instance_row):
        row_num = int(instance_row.index / len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        if self.add_pz.is_pz == 1:
            self.add_pz.kod.text = row_data[0]
            self.add_pz.nazwa.text = row_data[1]
            self.add_pz.cena.text = row_data[3]
        elif self.add_wz.is_wz == 1:
            self.add_wz.kod.text = row_data[0]
            self.add_wz.nazwa.text = row_data[1]
            self.add_wz.cena.text = row_data[3]
        elif self.edit_pz.is_pz_ed == 1:
            self.edit_pz.kod.text = row_data[0]
            self.edit_pz.nazwa.text = row_data[1]
            self.edit_pz.cena.text = row_data[3]
        elif self.edit_wz.is_wz_ed == 1:
            self.edit_wz.kod.text = row_data[0]
            self.edit_wz.nazwa.text = row_data[1]
            self.edit_wz.cena.text = row_data[3]
        self.go_back(instance_table)



    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        if self.add_wz.is_wz == 1:
            self.manager.current = 'add_WZ'
        elif self.add_pz.is_pz == 1:
            self.manager.current = 'add_PZ'
        elif self.edit_pz.is_pz_ed == 1:
            self.manager.current = 'edit_PZ'
        elif self.edit_wz.is_wz_ed == 1:
            self.manager.current = 'edit_WZ'

        self.add_wz.is_wz = 0
        self.add_pz.is_pz = 0
        self.add_pz.is_pz_ed = 0
        self.add_wz.is_wz_ed = 0


    def show_alert_dialog(self, instance,text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

class WZScreen(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    dane_WZ = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Numer", dp(30)),
                ("Wartość", dp(30)),
                ("Odbiorca", dp(30))
            ],
        )
        self.dane_WZ = select_WZ2()

        for d in self.dane_WZ:
            i, w, o = d
            self.table.add_row((
                str(i), str(w), str(o)
            ))
        layout.add_widget(self.table)

        # Bind tabel
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

        # Przycisk usuń
        del_button = MDRaisedButton(text="Usun Zaznaczone", height=1)
        del_button.bind(on_press=self.delete)
        layout.add_widget(del_button)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Wystaw WZ", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk edytuj
        edit_button = MDRaisedButton(text="Edytuj WZ", height=1)
        edit_button.bind(on_press=self.edit)
        layout.add_widget(edit_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'main_menu'

    def delete(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog2(instance, 'WZ nie został wybrany')
        else:
            for i in self.t:
                delete_WZ(i)
                self.show_alert_dialog(instance, 'WZ', i , 'została usunięnta')

            for d in self.dane_WZ:
                n, w, o = d
                self.table.remove_row((
                    str(n), str(w), str(o)
                ))
            self.dane_WZ = select_WZ2()
            for d in self.dane_WZ:
                n, w, o = d
                self.table.add_row((
                    str(n), str(w), str(o)
                ))
            self.t = []


    def show_alert_dialog(self, instance, text, towar, text2):
        self.dialog = MDDialog(
            text=text + towar + text2,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def show_alert_dialog2(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def add(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'add_WZ'

    def edit(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'WZ nie został wybrany')
        else:
            self.manager.transition = SlideTransition(direction='left', duration=0.50)
            wz, wz_p = select_wz_edit(self.t)
            wz = wz[0]
            self.edit_wz.odb.text = str(wz[0])
            for e in wz_p:
                i, w, tk, tn, c = e
                self.edit_wz.table.add_row((
                    str(tk), str(tn), str(c), str(i), str(w)
                ))
            self.wz_id = self.t
            self.wz_p = wz_p
            self.manager.current = 'edit_WZ'


    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class AddScreenWZ(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    towar_wz = []
    towar_wz_all = []
    odb_wz = ''
    is_wz = 0

    def __init__(self, dane_tow, dane_wz, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dane_tow = dane_tow
        self.dane_wz = dane_wz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.odb = MDTextField(hint_text='Odbiorca' )
        self.kod = MDTextField(hint_text='Kod', icon_right = 'language-python')
        self.nazwa = MDTextField(hint_text='Nazwa')
        self.cena = MDTextField(hint_text='Cena')
        self.ilosc = MDTextField(hint_text='Ilość')

        layout.add_widget(self.odb)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.cena)
        layout.add_widget(self.ilosc)

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Cena", dp(30)),
                ("Ilość", dp(30)),
                ("Wartość", dp(30)),
            ],
        )
        layout.add_widget(self.table)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Rejestruj", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk nastepny towar
        edit_button = MDRaisedButton(text="Zatwierdz towar/Dodaj kolejny towar", height=1)
        edit_button.bind(on_press=self.save)
        layout.add_widget(edit_button)

        # Przycisk usun
        edit_button = MDRaisedButton(text="Usun", height=1)
        edit_button.bind(on_press=self.delete)
        layout.add_widget(edit_button)

        tow_button = MDRaisedButton(text="Odbiorcy", height=1)
        tow_button.bind(on_press=self.to_dst)
        layout.add_widget(tow_button)

        # Dodaj przycisk Tow
        tow_button = MDRaisedButton(text="Towary", height=1)
        tow_button.bind(on_press=self.to_tow)
        layout.add_widget(tow_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_WZ'

    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def delete(self, instance):
        for i in self.t:
            for z in self.towar_wz_all:
                if i == z[0]:
                    k, n, c, i, w = z
                    self.table.remove_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))
                    self.towar_wz_all.remove(z)


        self.t = []

    def add(self, instance):
        if len(self.towar_wz_all) == 0:
            self.show_alert_dialog(instance, 'Nie można wystawić PZ bez pozycji')
        else:
            add_wz(self.towar_wz_all, self.odb_wz)
            for t in self.towar_wz_all:
                k, n, c, i, w = t
                self.table.remove_row((
                    str(k), str(n), str(c), str(i), str(w)
                ))
            self.show_alert_dialog(instance, 'Wz zostało wystawione')
            self.go_back(instance)
            for d in self.dane_wz.dane_WZ:
                n, w, o = d
                self.dane_wz.table.remove_row((
                    str(n), str(w), str(o)
                ))
            self.dane_wz.dane_WZ = select_WZ2()
            for d in self.dane_wz.dane_WZ:
                n, w, o = d
                self.dane_wz.table.add_row((
                    str(n), str(w), str(o)
                ))
            self.towar_wz_all = []


    def to_dst(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'odb_to_wz'
        self.is_pz = 1
    def to_tow(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'tow_pz_wz'
        self.is_wz = 1

    def save(self, instance):
        self.odb_wz = self.odb.text
        kod = self.kod.text
        nazwa = self.nazwa.text
        cena = self.cena.text
        cena = zamien_przecinek_na_kropke(cena)
        ilosc = self.ilosc.text
        odb_is = select_odb_where(self.odb_wz)
        if odb_is == False:
            self.show_alert_dialog(instance, 'Taki odbiorca nie występuje w bazie')
            pass
        else:
            if kod == '' or nazwa == '' or cena == '' or ilosc == '':
                self.show_alert_dialog(instance, 'Wszystkie pola są wymagane do wystawienia dokumentu')
                pass
            else:
                x = select_tow_where(kod)
                if x == False:
                    self.show_alert_dialog(instance, 'Taki towar nie występuje w bazie')
                else:
                    ilo_c = ilo_check(kod)
                    if int(ilo_c) <= int(ilosc):
                        self.show_alert_dialog(instance, 'Mie masz tyle tego towatu na stanie Aktualny stan to '+ str(ilo_c))
                        pass
                    else:
                        cena = round(float(cena), 2)
                        wartosc = float(ilosc) * float(cena)
                        self.towar_wz.append(kod)
                        self.towar_wz.append(nazwa)
                        self.towar_wz.append(cena)
                        self.towar_wz.append(ilosc)
                        self.towar_wz.append(wartosc)
                        self.towar_wz_all.append(self.towar_wz)
                        k, n, c, i, w = self.towar_wz
                        self.table.add_row((
                            str(k), str(n), str(c), str(i), str(w)
                        ))



        self.towar_wz = []



    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class AddScreenPZ(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    towar_pz = []
    towar_pz_all = []
    is_pz = 0

    def __init__(self, dane_tow, dane_pz, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dane_tow = dane_tow
        self.dane_pz = dane_pz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.dst = MDTextField(hint_text='Dostawca')
        self.kod = MDTextField(hint_text='Kod', icon_right = 'language-python')
        self.nazwa = MDTextField(hint_text='Nazwa')
        self.cena = MDTextField(hint_text='Cena')
        self.ilosc = MDTextField(hint_text='Ilość')

        layout.add_widget(self.dst)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.cena)
        layout.add_widget(self.ilosc)

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Cena", dp(30)),
                ("Ilość", dp(30)),
                ("Wartość", dp(30)),
            ],
        )
        layout.add_widget(self.table)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Rejestruj", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk nastepny towar
        edit_button = MDRaisedButton(text="Zatwierdz towar/Dodaj kolejny towar", height=1)
        edit_button.bind(on_press=self.save)
        layout.add_widget(edit_button)

        # Przycisk usun
        edit_button = MDRaisedButton(text="Usun", height=1)
        edit_button.bind(on_press=self.delete)
        layout.add_widget(edit_button)

        # Dodaj przycisk Tow
        tow_button = MDRaisedButton(text="Towary", height=1)
        tow_button.bind(on_press=self.to_tow)
        layout.add_widget(tow_button)

        # Dodaj przycisk Dst
        tow_button = MDRaisedButton(text="Dostawcy", height=1)
        tow_button.bind(on_press=self.to_dst)
        layout.add_widget(tow_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)


        self.add_widget(layout)


    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_PZ'

    def to_tow(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'tow_pz_wz'
        self.tow_do_pz.dst = self.dst.text
        self.is_pz = 1

    def to_dst(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'dst_to_pz'
        self.is_pz = 1





    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def show_alert_dialogTow(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="Tak",
                    on_release=self.tow_add,
                ),
                MDFlatButton(
                    text="Nie",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def tow_add(self, instance):
        tow_kod = self.kod.text
        nazwa = self.nazwa.text
        ce = self.cena.text
        x = add_tow(tow_kod, nazwa, ce)
        self.dialog_close(instance)
        self.show_alert_dialog(instance, 'Towar' + tow_kod + 'został dodany')
    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def delete(self, instance):
        for i in self.t:
            for z in self.towar_pz_all:
                if i == z[0]:
                    k, n, c, i, w = z
                    self.table.remove_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))
                    self.towar_pz_all.remove(z)


        self.t = []

    def add(self, instance):
        if len(self.towar_pz_all) == 0:
            self.show_alert_dialog(instance, 'Nie można wystawić PZ bez pozycji')
        else:
            add_pz(self.towar_pz_all, self.dst_pz)
            for t in self.towar_pz_all:
                k, n, c, i, w = t
                self.table.remove_row((
                    str(k), str(n), str(c), str(i), str(w)
                ))
            self.show_alert_dialog(instance, 'pz zostało wystawione')
            self.go_back(instance)
            for d in self.dane_pz.dane_PZ:
                n, w, o = d
                self.dane_pz.table.remove_row((
                    str(n), str(w), str(o)
                ))
            self.dane_pz.dane_PZ = select_PZ2()
            for d in self.dane_pz.dane_PZ:
                n, w, o = d
                self.dane_pz.table.add_row((
                    str(n), str(w), str(o)
                ))
            self.towar_pz_all = []


    def save(self, instance):
        self.dst_pz = self.dst.text
        kod = self.kod.text
        nazwa = self.nazwa.text
        cena = self.cena.text
        cena = zamien_przecinek_na_kropke(cena)
        ilosc = self.ilosc.text
        dst_is = select_dst_where(self.dst_pz)
        if dst_is == False:
            self.show_alert_dialog(instance, 'Taki odbiorca nie występuje w bazie')
            pass
        else:
            if kod == '' or nazwa == '' or cena == '' or ilosc == '':
                self.show_alert_dialog(instance, 'Wszystkie pola są wymagane do wystawienia dokumentu')
                pass
            else:
                x = select_tow_where(kod)
                if x == False:
                    self.show_alert_dialogTow(instance, 'Taki towar nie występuje w bazie./n Czy chcesz go dodać?')
                    pass
                else:
                    cena = round(float(cena), 2)
                    wartosc = float(ilosc) * float(cena)
                    self.towar_pz.append(kod)
                    self.towar_pz.append(nazwa)
                    self.towar_pz.append(cena)
                    self.towar_pz.append(ilosc)
                    self.towar_pz.append(wartosc)
                    self.towar_pz_all.append(self.towar_pz)
                    k, n, c, i, w = self.towar_pz
                    self.table.add_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))



        self.towar_pz = []



    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class EditScreenPZ(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    towar_pz = []
    towar_pz_all = []
    is_pz = 0
    pz_p = []

    def __init__(self, dane_tow, menu_pz,  **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dane_tow = dane_tow
        self.dane_pz = menu_pz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.dst = MDTextField(hint_text='Dostawca')
        self.kod = MDTextField(hint_text='Kod', icon_right = 'language-python')
        self.nazwa = MDTextField(hint_text='Nazwa')
        self.cena = MDTextField(hint_text='Cena')
        self.ilosc = MDTextField(hint_text='Ilość')

        layout.add_widget(self.dst)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.cena)
        layout.add_widget(self.ilosc)

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Cena", dp(30)),
                ("Ilość", dp(30)),
                ("Wartość", dp(30)),
            ],
        )
        layout.add_widget(self.table)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Rejestruj", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk nastepny towar
        edit_button = MDRaisedButton(text="Zatwierdz towar/Dodaj kolejny towar", height=1)
        edit_button.bind(on_press=self.save)
        layout.add_widget(edit_button)

        # Przycisk usun
        edit_button = MDRaisedButton(text="Usun", height=1)
        edit_button.bind(on_press=self.delete)
        layout.add_widget(edit_button)

        # Dodaj przycisk Tow
        tow_button = MDRaisedButton(text="Towary", height=1)
        tow_button.bind(on_press=self.to_tow)
        layout.add_widget(tow_button)

        # Dodaj przycisk Dst
        tow_button = MDRaisedButton(text="Dostawcy", height=1)
        tow_button.bind(on_press=self.to_dst)
        layout.add_widget(tow_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)



        self.add_widget(layout)

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.dane_pz.pz_p = list(self.dane_pz.pz_p)
        for x in self.dane_pz.pz_p:
            x = list(x)
            self.pz_p.append(x)
        for t in self.pz_p:
            i, w, k, n, c = t
            self.table.remove_row((
                str(k), str(n), str(c), str(i), str(w)
            ))
        self.pz_p = []
        self.manager.current = 'menu_PZ'

    def to_tow(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'tow_pz_wz'
        self.is_pz_ed = 1

    def to_dst(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'dst_to_pz'
        self.is_pz_ed = 1





    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def show_alert_dialogTow(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="Tak",
                    on_release=self.tow_add,
                ),
                MDFlatButton(
                    text="Nie",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def tow_add(self, instance):
        tow_kod = self.kod.text
        nazwa = self.nazwa.text
        ce = self.cena.text
        ce = zamien_przecinek_na_kropke(ce)
        x = add_tow(tow_kod, nazwa, ce)
        self.dialog_close(instance)
        self.show_alert_dialog(instance, 'Towar' + tow_kod + 'został dodany')
    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def delete(self, instance):
        for i in self.t:
            for z in self.dane_pz.pz_p:
                if i == z[2]:
                    i, w, k, n, c = z
                    self.table.remove_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))
                    self.dane_pz.pz_p = list(self.dane_pz.pz_p)
                    self.dane_pz.pz_p.remove(z)



        self.t = []

    def add(self, instance):
        self.dane_pz.pz_p = list(self.dane_pz.pz_p)
        for x in self.dane_pz.pz_p:
            x = list(x)
            self.pz_p.append(x)
        del_pz_p(self.dane_pz.pz_id)
        edit_pz(self.pz_p, self.dane_pz.pz_id)
        # for t in self.pz_p:
        #     i, w, k, n, c = t
        #     self.table.remove_row((
        #         str(k), str(n), str(c), str(i), str(w)
        #     ))
        self.pz_p = []
        self.show_alert_dialog(instance, 'pz zostało edytowane')
        self.go_back(instance)


    def save(self, instance):
        self.dst_pz = self.dst.text
        kod = self.kod.text
        nazwa = self.nazwa.text
        cena = self.cena.text
        cena = zamien_przecinek_na_kropke(cena)
        ilosc = self.ilosc.text
        dst_is = select_dst_where(self.dst_pz)
        if dst_is == False:
            self.show_alert_dialog(instance, 'Taki odbiorca nie występuje w bazie')
            pass
        else:
            if kod == '' or nazwa == '' or cena == '' or ilosc == '':
                self.show_alert_dialog(instance, 'Wszystkie pola są wymagane do wystawienia dokumentu')
                pass
            else:
                x = select_tow_where(kod)
                if x == False:
                    self.show_alert_dialogTow(instance, 'Taki towar nie występuje w bazie./n Czy chcesz go dodać?')
                    pass
                else:
                    cena = round(cena, 2)
                    wartosc = float(ilosc) * float(cena)
                    self.towar_pz.append(ilosc)
                    self.towar_pz.append(wartosc)
                    self.towar_pz.append(kod)
                    self.towar_pz.append(nazwa)
                    self.towar_pz.append(cena)
                    self.pz_p.append(self.towar_pz)
                    k, n, c, i, w = self.towar_pz
                    self.table.add_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))



        self.towar_pz = []



    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class EditScreenWZ(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    towar_wz = []
    towar_wz_all = []
    is_wz = 0
    wz_p = []

    def __init__(self, dane_tow, menu_wz,  **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dane_tow = dane_tow
        self.dane_wz = menu_wz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.odb = MDTextField(hint_text='Dostawca')
        self.kod = MDTextField(hint_text='Kod', icon_right = 'language-python')
        self.nazwa = MDTextField(hint_text='Nazwa')
        self.cena = MDTextField(hint_text='Cena')
        self.ilosc = MDTextField(hint_text='Ilość')

        layout.add_widget(self.odb)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.cena)
        layout.add_widget(self.ilosc)

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Cena", dp(30)),
                ("Ilość", dp(30)),
                ("Wartość", dp(30)),
            ],
        )
        layout.add_widget(self.table)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Rejestruj", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk nastepny towar
        edit_button = MDRaisedButton(text="Zatwierdz towar/Dodaj kolejny towar", height=1)
        edit_button.bind(on_press=self.save)
        layout.add_widget(edit_button)

        # Przycisk usun
        edit_button = MDRaisedButton(text="Usun", height=1)
        edit_button.bind(on_press=self.delete)
        layout.add_widget(edit_button)

        # Dodaj przycisk Tow
        tow_button = MDRaisedButton(text="Towary", height=1)
        tow_button.bind(on_press=self.to_tow)
        layout.add_widget(tow_button)

        # Dodaj przycisk odb
        tow_button = MDRaisedButton(text="Odbiorcy", height=1)
        tow_button.bind(on_press=self.to_odb)
        layout.add_widget(tow_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)



        self.add_widget(layout)

        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.dane_wz.wz_p = list(self.dane_wz.wz_p)
        for x in self.dane_wz.wz_p:
            x = list(x)
            self.wz_p.append(x)
        for t in self.wz_p:
            i, w, k, n, c = t
            self.table.remove_row((
                str(k), str(n), str(c), str(i), str(w)
            ))
        self.wz_p = []
        self.manager.current = 'menu_WZ'

    def to_tow(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'tow_pz_wz'
        self.is_wz_ed = 1

    def to_odb(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'odb_to_wz'
        self.is_wz_ed = 1





    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def show_alert_dialogTow(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="Tak",
                    on_release=self.tow_add,
                ),
                MDFlatButton(
                    text="Nie",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def tow_add(self, instance):
        tow_kod = self.kod.text
        nazwa = self.nazwa.text
        ce = self.cena.text
        ce = zamien_przecinek_na_kropke(ce)
        x = add_tow(tow_kod, nazwa, ce)
        self.dialog_close(instance)
        self.show_alert_dialog(instance, 'Towar' + tow_kod + 'został dodany')
    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def delete(self, instance):
        for i in self.t:
            for z in self.dane_wz.wz_p:
                if i == z[2]:
                    i, w, k, n, c = z
                    self.table.remove_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))
                    self.dane_wz.wz_p = list(self.dane_wz.wz_p)
                    self.dane_wz.wz_p.remove(z)

        self.t = []

    def add(self, instance):
        self.dane_wz.wz_p = list(self.dane_wz.wz_p)
        for x in self.dane_wz.wz_p:
            x = list(x)
            self.wz_p.append(x)
        del_wz_p(self.dane_wz.wz_id)
        edit_wz(self.wz_p, self.dane_wz.wz_id)
        self.wz_p = []
        self.show_alert_dialog(instance, 'pz zostało edytowane')
        self.go_back(instance)


    def save(self, instance):
        self.odb_wz = self.odb.text
        kod = self.kod.text
        nazwa = self.nazwa.text
        cena = self.cena.text
        cena = zamien_przecinek_na_kropke(cena)
        ilosc = self.ilosc.text
        odb_is = select_odb_where(self.odb_wz)
        if odb_is == False:
            self.show_alert_dialog(instance, 'Taki odbiorca nie występuje w bazie')
            pass
        else:
            if kod == '' or nazwa == '' or cena == '' or ilosc == '':
                self.show_alert_dialog(instance, 'Wszystkie pola są wymagane do wystawienia dokumentu')
                pass
            else:
                x = select_tow_where(kod)
                if x == False:
                    self.show_alert_dialogTow(instance, 'Taki towar nie występuje w bazie./n Czy chcesz go dodać?')
                    pass
                else:
                    cena = round(cena, 2)
                    wartosc = float(ilosc) * float(cena)
                    self.towar_pz.append(ilosc)
                    self.towar_pz.append(wartosc)
                    self.towar_pz.append(kod)
                    self.towar_pz.append(nazwa)
                    self.towar_pz.append(cena)
                    self.wz_p.append(self.towar_wz)
                    k, n, c, i, w = self.towar_wz
                    self.table.add_row((
                        str(k), str(n), str(c), str(i), str(w)
                    ))



        self.towar_wz = []



    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class MenuScreenPZ(Screen):
    t = []
    t2 = []
    text1 = ''
    text2 = ''
    text3 = ''
    dane_PZ = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Numer", dp(30)),
                ("Wartość", dp(30)),
                ("Dostawca", dp(30))
            ],
        )
        self.dane_PZ = select_PZ2()

        for d in self.dane_PZ:
            i, w, o = d
            self.table.add_row((
                str(i), str(w), str(o)
            ))
        layout.add_widget(self.table)

        # Bind tabel
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

        # Przycisk usuń
        del_button = MDRaisedButton(text="Usun Zaznaczone", height=1)
        del_button.bind(on_press=self.delete)
        layout.add_widget(del_button)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Wystaw PZ", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk edytuj
        edit_button = MDRaisedButton(text="Edytuj PZ", height=1)
        edit_button.bind(on_press=self.edit)
        layout.add_widget(edit_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'main_menu'

    def delete(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            for i in self.t:
                delete_PZ(i)
                self.show_alert_dialog(instance, 'PZ została usunięnta')

            for d in self.dane_PZ:
                n, w, o = d
                self.table.remove_row((
                    str(n), str(w), str(o)
                ))
            self.dane_PZ = select_PZ2()
            for d in self.dane_PZ:
                n, w, o = d
                self.table.add_row((
                    str(n), str(w), str(o)
                ))
            self.t = []

    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)


    def add(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'add_PZ'

    def edit(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            self.manager.transition = SlideTransition(direction='left', duration=0.50)
            pz, pz_p = select_pz_edit(self.t)
            pz = pz[0]
            self.edit_pz.dst.text = str(pz[0])
            for e in pz_p:
                i, w, tk, tn, c = e
                self.edit_pz.table.add_row((
                    str(tk), str(tn), str(c), str(i), str(w)
                ))
            self.pz_id = self.t
            self.pz_p = pz_p
            self.manager.current = 'edit_PZ'


    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)

class EditScreenDst(Screen):

    def __init__(self, **kwargs ):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)
        # edit_nazwa = dane_edit.nazwa
        # edit_kod = dane_edit.kod
        # edit_cena = dane_edit.cena
        self.okno = MDLabel(text='Edycjak Dostawcy')
        self.kod = MDLabel(text='',size = (50,50))
        self.nazwa = MDTextField(hint_text='Nazwa', text='')
        self.nip = MDTextField(hint_text='Nip', text='')

        layout.add_widget(self.okno)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.nip)

        button1 = MDRaisedButton(text='Potwierdz Edycje')
        button1.bind(on_press=self.dst_edit)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def dst_edit(self, instance):
        kod = self.kod.text
        nazwa = self.nazwa.text
        nip = self.nip.text
        kod = kod.replace('Kod: ', '')
        dst_edit(kod, nazwa, nip)
        self.show_alert_dialog(instance, 'Dostawca ', nazwa, ' został zmodyfikowany')
        self.go_back(instance)
        for d in self.menu_dst.dane_dst:
            k, n, ni = d
            self.menu_dst.table.remove_row((
                str(k), str(n), str(ni)
            ))

        dane_dst = select_dst2()
        for d in dane_dst:
            k, n, ni = d
            self.menu_dst.table.add_row((
                str(k), str(n), str(ni)
            ))

    def show_alert_dialog(self, instance, text, towar, text2):
        self.dialog = MDDialog(
            text=text + towar + text2,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_dst'

class MenuScreenDst(Screen):
    t = []
    t2 = []
    kod = ''
    nip = ''
    nazwa = ''

    def __init__(self,edit_dst, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.edit_dst = edit_dst
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Nip", dp(30))
            ],
        )
        self.dane_dst = select_dst2()


        for d in self.dane_dst:
            k, n, ni = d
            self.table.add_row((
                str(k), str(n), str(ni)
            ))

        layout.add_widget(self.table)

        # Bind tabeli
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

        # Przycisk usuń
        del_button = MDRaisedButton(text="Usun Zaznaczone", height=1)
        del_button.bind(on_press=self.delete)
        layout.add_widget(del_button)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Dodaj dostawce", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk edytuj
        edit_button = MDRaisedButton(text="Edytuj dostawce", height=1)
        edit_button.bind(on_press=self.edit)
        layout.add_widget(edit_button)

        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'main_menu'

    def delete(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            for i in self.t:
                try:
                    delete_dst(i)
                except pymysql.err.IntegrityError as e:
                    if e.args[0] == 1451:
                        self.show_alert_dialog(instance, 'Ten dostawca jest na dokumencie')
                    else:
                        raise

            for d in self.dane_dst:
                k, n, ni = d
                self.table.remove_row((
                    str(k), str(n), str(ni)
                ))
            self.dane_dst = select_dst2()
            for d in self.dane_dst:
                k, n, ni = d
                self.table.add_row((
                    str(k), str(n), str(ni)
                ))
            self.t = []
            self.t2 = []

    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)

    def add(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'add_dst'

    def edit(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            self.manager.transition = SlideTransition(direction='left', duration=0.50)
            self.manager.current = 'edit_dst'
            self.edit_dst.kod.text = 'Kod: ' + self.kod
            self.edit_dst.nazwa.text = self.nazwa
            self.edit_dst.nip.text = self.nip

    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)
            self.t3 = self.t2[0]
            self.kod = str(self.t3[0])
            self.nazwa = str(self.t3[1])
            self.nip = str(self.t3[2])

class MenuScreenDstPZ(Screen):
    t = []
    t2 = []
    kod = ''
    nip = ''
    nazwa = ''

    def __init__(self,add_pz, edit_pz, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_pz = add_pz
        self.edit_pz = edit_pz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Nip", dp(30))
            ],
        )
        self.dane_dst = select_dst2()


        for d in self.dane_dst:
            k, n, ni = d
            self.table.add_row((
                str(k), str(n), str(ni)
            ))

        layout.add_widget(self.table)

        # Bind tabeli
        self.table.bind(on_row_press=self.do_doc)


        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'add_PZ'

    def do_doc(self, instance_table, instance_row):
        row_num = int(instance_row.index / len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        self.add_pz.dst.text = row_data[0]
        self.go_back(instance_table)

class MenuScreenDstWZ(Screen):
    t = []
    t2 = []
    kod = ''
    nip = ''
    nazwa = ''

    def __init__(self,add_wz, edit_wz, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_wz = add_wz
        self.edit_wz = edit_wz
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Nip", dp(30))
            ],
        )
        self.dane_odb = select_odb2()


        for d in self.dane_odb:
            k, n, ni = d
            self.table.add_row((
                str(k), str(n), str(ni)
            ))

        layout.add_widget(self.table)

        # Bind tabeli
        self.table.bind(on_row_press=self.do_doc)


        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'add_WZ'

    def do_doc(self, instance_table, instance_row):
        row_num = int(instance_row.index / len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        self.add_wz.odb.text = row_data[0]
        self.go_back(instance_table)

class AddScreenOdb(Screen):
    def __init__(self, menu_odb, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.menu_odb = menu_odb

        okno = MDLabel(text='Dodanie Odbiorcy')
        self.text1 = MDTextField(hint_text='Kod')
        self.text2 = MDTextField(hint_text='Nazwa')
        self.text3 = MDTextField(hint_text='Nip')

        layout.add_widget(okno)
        layout.add_widget(self.text1)
        layout.add_widget(self.text2)
        layout.add_widget(self.text3)


        button1 = MDRaisedButton(text='Dodaj')
        button1.bind(on_press=self.odb_add)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def odb_add(self, instance):
        kod = self.text1.text
        nazwa = self.text2.text
        nip = self.text3.text
        x = add_odb(kod, nazwa, nip)
        if x == True:
            self.show_alert_dialog(instance)
        self.go_back(instance)
        for d in self.menu_odb.dane_odb:
            k, n, ni = d
            self.menu_odb.table.remove_row((
                str(k), str(n), str(ni)
            ))

        dane_odb = select_odb2()
        for d in dane_odb:
            k, n, ni = d
            self.menu_odb.table.add_row((
                str(k), str(n), str(ni)
            ))

    def show_alert_dialog(self, instance):
        self.dialog = MDDialog(
            text="Taki dostawce już istnieje w bazie",
            buttons=[
                MDFlatButton(
                    text="OK",
                    # on_click=self.dialog.close,
                ),
            ], )
        self.dialog.open()
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_odb'

class EditScreenOdb(Screen):

    def __init__(self, **kwargs ):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)
        # edit_nazwa = dane_edit.nazwa
        # edit_kod = dane_edit.kod
        # edit_cena = dane_edit.cena
        self.okno = MDLabel(text = 'Edycja Odbiorcy')
        self.kod = MDLabel(text='',size = (50,50))
        self.nazwa = MDTextField(hint_text='Nazwa', text='')
        self.nip = MDTextField(hint_text='Nip', text='')

        layout.add_widget(self.okno)
        layout.add_widget(self.kod)
        layout.add_widget(self.nazwa)
        layout.add_widget(self.nip)

        button1 = MDRaisedButton(text='Potwierdz Edycje')
        button1.bind(on_press=self.odb_edit)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def odb_edit(self, instance):
        kod = self.kod.text
        nazwa = self.nazwa.text
        nip = self.nip.text
        kod = kod.replace('Kod: ', '')
        odb_edit(kod, nazwa, nip)
        self.show_alert_dialog(instance, 'Odbiorca ', nazwa, ' został zmodyfikowany')
        self.go_back(instance)
        for d in self.menu_odb.dane_odb:
            k, n, ni = d
            self.menu_odb.table.remove_row((
                str(k), str(n), str(ni)
            ))

        dane_odb = select_odb2()
        for d in dane_odb:
            k, n, ni = d
            self.menu_odb.table.add_row((
                str(k), str(n), str(ni)
            ))

    def show_alert_dialog(self, instance, text, towar, text2):
        self.dialog = MDDialog(
            text=text + towar + text2,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_odb'

class MenuScreenOdb(Screen):
    t = []
    t2 = []
    kod = ''
    nip = ''
    nazwa = ''
    def __init__(self, edit_odb, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.edit_odb = edit_odb
        # Dodaj layout do umieszczenia danych
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        # Wyświetl dane z tabeli

        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            rows_num=25,
            column_data=[
                ("Kod", dp(30)),
                ("Nazwa", dp(30)),
                ("Nip", dp(30))
            ],
        )
        self.dane_odb = select_odb2()


        for d in self.dane_odb:
            k, n, ni = d
            self.table.add_row((
                str(k), str(n), str(ni)
            ))

        layout.add_widget(self.table)

        # Bind tabeli
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_check_press=self.checked2)

        # Przycisk usuń
        del_button = MDRaisedButton(text="Usun Zaznaczone", height=1)
        del_button.bind(on_press=self.delete)
        layout.add_widget(del_button)

        # Przycisk dodaj
        add_button = MDRaisedButton(text="Dodaj odbiorce", height=1)
        add_button.bind(on_press=self.add)
        layout.add_widget(add_button)

        # Przycisk edytuj
        edit_button = MDRaisedButton(text="Edytuj odbiorce", height=1)
        edit_button.bind(on_press=self.edit)
        layout.add_widget(edit_button)


        # Dodaj przycisk powrotu
        back_button = MDRaisedButton(text="Powrót", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'main_menu'

    def delete(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            for i in self.t:
                try:
                    delete_odb(i)
                except pymysql.err.IntegrityError as e:
                    if e.args[0] == 1451:
                        self.show_alert_dialog(instance, 'Ten dostawca jest na dokumencie')
                    else:
                        raise

            for d in self.dane_odb:
                k, n, ni = d
                self.table.remove_row((
                    str(k), str(n), str(ni)
                ))
            dane_odb = select_odb2()
            for d in dane_odb:
                k, n, ni = d
                self.table.add_row((
                    str(k), str(n), str(ni)
                ))
            self.t = []
            self.t2 = []

    def show_alert_dialog(self, instance, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_close,
                ),
            ], )
        self.dialog.open()

    def dialog_close(self, instance):
        self.dialog.dismiss(force=True)


    def add(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.50)
        self.manager.current = 'add_odb'

    def edit(self, instance):
        if len(self.t) == 0:
            self.show_alert_dialog(instance, 'Towar nie został wybrany')
        else:
            self.manager.transition = SlideTransition(direction='left', duration=0.50)
            self.manager.current = 'edit_odb'
            self.edit_odb.kod.text = 'Kod: ' + self.kod
            self.edit_odb.nazwa.text = self.nazwa
            self.edit_odb.nip.text = self.nip


    def checked(self, instance_table, current_row):
        found = False
        for item in self.t:
            if item == current_row[0]:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t.remove(current_row[0])
        else:
            # Do something else when no matching element is found
            self.t.append(current_row[0])

    def checked2(self, instance_table, current_row):
        found = False
        for item in self.t2:
            if item == current_row:
                found = True
                break
        if found:
            # Do something when a matching element is found
            self.t2.remove(current_row)
        else:
            # Do something else when no matching element is found
            self.t2.append(current_row)
            self.t3 = self.t2[0]
            self.kod = str(self.t3[0])
            self.nazwa = str(self.t3[1])
            self.nip = str(self.t3[2])

class AddScreenDst(Screen):
    def __init__(self, menu_dst, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)

        self.menu_dst = menu_dst

        okno = MDLabel(text='Dodanie Dostawcy')
        self.text1 = MDTextField(hint_text='Kod')
        self.text2 = MDTextField(hint_text='Nazwa')
        self.text3 = MDTextField(hint_text='Nip')

        layout.add_widget(okno)
        layout.add_widget(self.text1)
        layout.add_widget(self.text2)
        layout.add_widget(self.text3)


        button1 = MDRaisedButton(text='Dodaj')
        button1.bind(on_press=self.dst_add)
        layout.add_widget(button1)

        back_button = MDRaisedButton(text="Powrót/anuluj", height=1)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def dst_add(self, instance):
        kod = self.text1.text
        nazwa = self.text2.text
        nip = self.text3.text
        x = add_dst(kod, nazwa, nip)
        if x == True:
            self.show_alert_dialog(instance)
        else:
            self.go_back(instance)
        for d in self.menu_dst.dane_dst:
            k, n, ni = d
            self.menu_dst.table.remove_row((
                str(k), str(n), str(ni)
            ))

        dane_dst = select_dst2()
        for d in dane_dst:
            k, n, ni = d
            self.menu_dst.table.add_row((
                str(k), str(n), str(ni)
            ))

    def show_alert_dialog(self, instance):
        self.dialog = MDDialog(
            text="Taki dostawca już istnieje w bazie",
            buttons=[
                MDFlatButton(
                    text="OK",
                    # on_click=self.dialog.close,
                ),
            ], )
        self.dialog.open()
    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right', duration=0.50)
        self.manager.current = 'menu_dst'



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        screen_manager = ScreenManager()

        main_menu_screen = MainMenu(name='main_menu')
        edit_screen_tow = EditScreenTow(name='edit_tow')
        tow_select_screen = TowSelectScreen(name='tow_select', dane_edit = edit_screen_tow)
        menu_screen_wz = WZScreen(name='menu_WZ')
        menu_screen_pz = MenuScreenPZ(name='menu_PZ')
        edit_screen_odb = EditScreenOdb(name='edit_odb')
        edit_screen_dst = EditScreenDst(name='edit_dst')
        menu_screen_dst = MenuScreenDst(name='menu_dst', edit_dst = edit_screen_dst)
        menu_screen_odb = MenuScreenOdb(name='menu_odb', edit_odb = edit_screen_odb)
        add_screen_tow = AddScreenTow(name='add_tow', menu_tow = tow_select_screen)
        add_screen_odb = AddScreenOdb(name='add_odb', menu_odb = menu_screen_odb)
        add_screen_dst = AddScreenDst(name='add_dst', menu_dst = menu_screen_dst)
        add_screen_WZ = AddScreenWZ(name='add_WZ', dane_tow=tow_select_screen, dane_wz = menu_screen_wz)
        add_screen_PZ = AddScreenPZ(name='add_PZ', dane_tow=tow_select_screen, dane_pz = menu_screen_pz)
        edit_screen_pz = EditScreenPZ(name = 'edit_PZ', dane_tow=tow_select_screen, menu_pz = menu_screen_pz)
        edit_screen_wz = EditScreenWZ(name = 'edit_WZ', dane_tow=tow_select_screen, menu_wz = menu_screen_wz)
        tow_to_pz = TowSelectScreenToPZ(name='tow_pz_wz', add_pz=add_screen_PZ, add_wz=add_screen_WZ, edit_pz = edit_screen_pz)
        dst_to_pz = MenuScreenDstPZ(name='dst_to_pz', add_pz=add_screen_PZ, edit_pz = edit_screen_pz)
        odb_to_wz = MenuScreenDstWZ(name='odb_to_wz', add_wz=add_screen_WZ, edit_wz = edit_screen_wz)

        edit_screen_tow.menu_tow = tow_select_screen
        edit_screen_dst.menu_dst = menu_screen_dst
        edit_screen_odb.menu_odb = menu_screen_odb
        menu_screen_pz.edit_pz = edit_screen_pz
        menu_screen_wz.edit_wz = edit_screen_wz
        add_screen_PZ.tow_do_pz = tow_to_pz


        

        screen_manager.add_widget(main_menu_screen)
        screen_manager.add_widget(add_screen_tow)
        screen_manager.add_widget(edit_screen_tow)
        screen_manager.add_widget(edit_screen_odb)
        screen_manager.add_widget(edit_screen_dst)
        screen_manager.add_widget(add_screen_odb)
        screen_manager.add_widget(add_screen_WZ)
        screen_manager.add_widget(add_screen_PZ)
        screen_manager.add_widget(add_screen_dst)
        screen_manager.add_widget(menu_screen_wz)
        screen_manager.add_widget(menu_screen_pz)
        screen_manager.add_widget(menu_screen_dst)
        screen_manager.add_widget(menu_screen_odb)
        screen_manager.add_widget(tow_select_screen)
        screen_manager.add_widget(tow_to_pz)
        screen_manager.add_widget(odb_to_wz)
        screen_manager.add_widget(dst_to_pz)
        screen_manager.add_widget(edit_screen_pz)
        screen_manager.add_widget(edit_screen_wz)

        return screen_manager


if __name__ == '__main__':
    MainApp().run()

mydb.close()
