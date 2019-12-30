import os
import kivy
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import data_supply as ds
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.utils.cropimage import crop_image
from kivymd.uix.date_picker import MDDatePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
import datetime
from kivy.uix.popup import Popup

student_list = []

sml = []

sl = [[], [], [], []]

popup = Popup()


class ScreenManager1(ScreenManager):
    def do_it(self):
        print(self.ids.client.text)

    def add_student_list(self):

        st_list = ds.send_student_list()
        global student_list
        student_list = []
        self.ids.std_lst.clear_widgets()
        i = 0

        for value in st_list[1]:
            x = [value['userid'], value['name']]
            student_list.append(x)
            onl = (OneLineListItem(id='litm' + str(value['userid']), text=str(value['userid']) + ':  ' + value['name']))
            onl.bind(on_release=self.disp_st_dtl)
            self.ids.std_lst.add_widget(onl)
            i = i + 1

    def update_student_list(self, sb, st):

        self.ids.std_lst.clear_widgets()
        i = 0
        global student_list

        for value in student_list:
            if st == '':
                onl = (OneLineListItem(id='litm' + str(value[0]), text=str(value[0]) + ':  ' + value[1]))
                onl.bind(on_release=self.disp_st_dtl)
                self.ids.std_lst.add_widget(onl)
            elif (sb == 'id' and str(value[0]) == st) or (sb == 'name' and value[1].find(str(st)) != -1):
                onl = (OneLineListItem(id='litm' + str(value[0]), text=str(value[0]) + ':  ' + value[1]))
                onl.bind(on_release=self.disp_st_dtl)
                self.ids.std_lst.add_widget(onl)
                i = i + 1

    # self.ids.std_lst.add_widget(OneLineListItem(id = 'litm'+str(value[0]),text= str(value[0])+':  '+value[1] ,
    # on_touch_up= lambda x: print('c')))

    def disp_st_dtl(self, i):
        print(i.text)
        x = i.text
        y = x.split(':')
        z = y[1].split(' ')
        self.ids.tile_s_2.text = y[0] + '\n' + z[len(z) - 2] + ' ' + z[len(z) - 1]
        self.ids.scr_mg1.current = 'student_detail'
        global sl
        sl[1].append('Student_List')
        print(sl)

    def login_admin(self, admin_id, pswd):
        x = ds.on_login_admin(admin_id, pswd)
        if x[0] == 'Login Successful':
            self.current = 'screenA'

            global sl
            print(sl)
            print(sl[0])
            sl[0].append('LoginA')
            print(sl)
        return x

    def refresh_std_list(self):

        self.add_student_list()
        self.ids.search_f.text = ''

        print('refresh complete')

    def search_student(self, txt, sb):
        self.update_student_list(sb, txt)


class TryApp(MDApp):
    admin_details = []

    def build(self):
        Window.softinput_mode = 'below_target'
        return ScreenManager1()

    def on_start(self):
        self.prepare_sml()
        Window.bind(on_keyboard=self.my_key_handler)

    def on_yes(self, screen):

        global popup
        if screen == 'Student_List':
            self.root.ids.scr_mg_as.current = 'new_student1'
            self.root.ids.scr_mg1.current = 'Student_List'
            sl[2] = []
            sl[1].pop(-1)
        elif screen == 'LoginA':

            self.root.ids.nda.active_item._active = False
            self.root.ids.nda.active_item = self.root.ids.nav_home
            self.root.ids.nda.active_item._active = True
            self.root.current = 'LoginA'
            self.root.ids.scr_mg1.current = 'Home'
            print(self.root.ids.nav_home)

            self.root.ids.scr_mg_as.current = 'new_student1'
            sl[1] = []
            sl[0].pop(-1)
        print('didmoiss in yes')
        popup.dismiss()

    def on_no(self, screen):
        global popup
        print('didmoiss in no')
        popup.dismiss()

    def show_popup(self, title, content, screen):
        global popup
        content_layout = FloatLayout()
        text_label = MDLabel(text=content, pos_hint={"top": 1, "center_x": 0.5}, size_hint=[1, 0.7])
        button1 = MDRaisedButton(text='No', pos_hint={"top": 0.25, "x": 0.10}, size_hint=[0.30, 0.20])
        button2 = MDRaisedButton(text='Yes', pos_hint={"top": 0.25, "x": 0.60}, size_hint=[0.30, 0.20])
        button2.bind(on_release=lambda x: self.on_yes(screen))
        button1.bind(on_release=lambda x: self.on_no(screen))
        content_layout.add_widget(text_label)
        content_layout.add_widget(button1)
        content_layout.add_widget(button2)
        popup = Popup(title=title, content=content_layout, size_hint=[0.7, 0.3], background='bg_blue.jpeg',
                      separator_color=[0, 0, 0, 1], title_color=[0, 0, 0, 1])

    def my_key_handler(self, window, key, *largs):

        global popup
        print(key)
        print()
        global sml
        global sl
        print(sml[0][0])
        print(sl[0][0])
        if key == 27:
            if sl[2] != []:
                sml[2][0].current = sl[2][-1]
                sl[2].pop(-1)
                return True
            if sl[1] != []:
                print(sl)
                print(sl[1][-1])
                if sl[1][-1] == 'Student_List':
                    if self.root.ids.scr_mg1.current == 'new_student':
                        self.show_popup("Don't Add New Student", 'Do you want to leave without adding student ',
                                        'Student_List')
                        popup.open()
                    elif self.root.ids.scr_mg1.current == 'student_detail':
                        self.back_to_slist_from_sdtl()

                    return True

                else:
                    if sl[1][-1] == 'Home':
                        self.root.ids.nda.active_item._active = False
                        self.root.ids.nda.active_item = self.root.ids.nav_home
                        self.root.ids.nda.active_item._active = True

                    sml[1][0].current = sl[1][-1]

                    sl[1].pop(-1)
                    return True
            if sl[0] != []:
                print(' in 0')
                if sl[0][-1] == 'LoginA':
                    print(' la')
                    self.show_popup('Log Out', 'Are you sure you want to LogOut ? ', 'LoginA')
                    popup.open()
                    return True

            return False

    def on_nav_switch(self, text):
        global sl
        print(sl)
        if (sl[1] != [] and sl[1][-1] != 'Home'):
            if text == 'Logout':
                print ('active 11')
                self.show_popup('Log Out', 'Are you sure you want to LogOut ? ', 'LoginA')
                popup.open()
        else:
            if text == 'Profile':
                self.root.ids.scr_mg1.current = 'Profile'
                if 'Home' not in sl[1]:
                    sl[1].append('Home')


            elif text == 'Student List':
                self.root.ids.scr_mg1.current = 'Student_List'
                if 'Home' not in sl[1]:
                    sl[1].append('Home')
            elif text == 'Accept Payment':
                self.root.ids.scr_mg1.current = 'Accept_Payment'
                if 'Home' not in sl[1]:
                    sl[1].append('Home')
            elif text == 'Transactions':
                self.root.ids.scr_mg1.current = 'Transactions'
                if 'Home' not in sl[1]:
                    sl[1].append('Home')
            elif text == 'Pending Approvals':
                self.root.ids.scr_mg1.current = 'Pending_Approvals'
                if 'Home' not in sl[1]:
                    sl[1].append('Home')
            elif text == 'Logout':
                self.show_popup('Log Out', 'Are you sure you want to LogOut ? ', 'LoginA')
                popup.open()

            elif text == 'Home':
                self.root.ids.scr_mg1.current = 'Home'
                if 'Home' in sl[1]:
                    sl[1].remove('Home')
            print(sl)

    def prepare_sml(self):
        global sml
        global sl

        x = [self.root, self.root, 'Welcome']

        sml.append(x)
        x = [self.root.ids.scr_mg1, self.root, 'Home']

        sml.append(x)
        x = [self.root.ids.scr_mg_as, self.root.ids.scr_mg1, 'new_student1']

        sml.append(x)
        x = [self.root.ids.scr_mg2, self.root, 'Home']

        sml.append(x)
        print(sml)

    def crop_image_for_tile(self, instance: object, size: object, path_to_crop_image: object) -> object:
        if not os.path.exists(os.path.join(self.directory, path_to_crop_image)):
            size = (int(size[0]), int(size[1]))
            path_to_origin_image = path_to_crop_image.replace('_tile_crop', '')
            crop_image(size, path_to_origin_image, path_to_crop_image)
        instance.source = path_to_crop_image

    def on_login_admin(self, admin_id, pswd):
        TryApp.admin_details = self.root.login_admin(admin_id, pswd)

    def prepare_student_profile(self, instance, size):
        url = "http://images.all-free-download.com/images/graphicthumb/img_9774_517863.jpg"
        img_name = 'profile_a.jpg'
        fp = ds.download_image(url, img_name)
        self.crop_image_for_tile(instance, size, fp)

    def prepare_admin_profile(self, instance, size):
        img_name = 'profile_a.jpg'
        url = "http://images.all-free-download.com/images/graphicthumb/img_9774_517863.jpg"
        fp = ds.download_image(url, img_name)
        self.crop_image_for_tile(instance, size, fp)

        self.root.ids.tile_a_2.text = TryApp.admin_details[1][0]['name']
        self.root.ids.pc_a.secondary_text = TryApp.admin_details[1][0]['primary_contact']
        self.root.ids.sc_a.secondary_text = TryApp.admin_details[1][0]['secondary_contact']
        self.root.ids.ei_a.secondary_text = TryApp.admin_details[1][0]['email']
        self.root.ids.ad_a.secondary_text = TryApp.admin_details[1][0]['address']
        self.root.ids.ds_a.secondary_text = TryApp.admin_details[1][0]['designation']

    def add_new_student(self):
        self.root.ids.scr_mg1.current = 'new_student'
        global sl
        sl[1].append('Student_List')
        print(sl)
        print("added")

    def show_example_date_picker(self, *args):

        if True:
            x = self.root.ids.date_picker_label.text
            y = x.split('/')
            if x != '':
                pd = datetime.date(int(y[2]), int(y[1]), int(y[0]))
            else:
                pd = datetime.date.today()

            try:
                MDDatePicker(self.set_previous_date,
                             pd.year, pd.month, pd.day).open()
            except AttributeError:
                MDDatePicker(self.set_previous_date).open()
        else:

            MDDatePicker(self.set_previous_date).open()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        x = str(date_obj)
        y = x.split('-')
        z = y[2] + '/' + y[1] + '/' + y[0]

        self.root.ids.date_picker_label.text = str(z)

    def back_to_slist_fr_adds(self):
        self.show_popup("Don't Add New Student", 'Do you want to leave without adding student ',
                        'Student_List')
        popup.open()

        print("came back")
        global sl

        print(sl)
        print("came back")

    def back_to_slist_from_sdtl(self):
        global sl
        self.root.ids.scr_mg1.current = 'Student_List'
        if sl[1] != [] and sl[1][-1] == 'Student_List':
            sl[1].pop(-1)

    def add_new_student_next(self):
        global sl

        curr_scr = self.root.ids.scr_mg_as.current
        if curr_scr == 'new_student1':
            self.root.ids.scr_mg_as.current = 'new_student2'
            sl[2].append('new_student1')
            print(sl)
        if curr_scr == 'new_student2':
            self.root.ids.scr_mg_as.current = 'new_student3'
            sl[2].append('new_student2')
            print(sl)
        if curr_scr == 'new_student3':
            self.root.ids.scr_mg_as.current = 'pickers'
            sl[2].append('new_student3')
            print(sl)

        if curr_scr == 'pickers':
            self.root.ids.scr_mg_as.current = 'new_student4'
            sl[2].append('pickers')
            print(sl)

        if curr_scr == 'new_student4':
            print(self.root.ids.as_add.text)
            self.root.ids.scr_mg_as.current = 'new_student5'
            sl[2].append('new_student4')
            print(sl)
        if curr_scr == 'new_student5':
            self.root.ids.scr_mg_as.current = 'new_student6'
            sl[2].append('new_student5')
            print(sl)
        if curr_scr == 'new_student6':
            self.root.ids.scr_mg_as.current = 'new_student7'
            sl[2].append('new_student6')
            print(sl)

        if curr_scr == 'new_student7':
            self.root.ids.scr_mg_as.current = 'new_student8'
            sl[2].append('new_student7')
            print(sl)
        if curr_scr == 'new_student8':
            self.root.ids.scr_mg_as.current = 'picker_doj'
            sl[2].append('new_student8')
            print(sl)

        if curr_scr == 'picker_doj':
            self.root.ids.scr_mg_as.current = 'new_student9'
            sl[2].append('picker_doj')
            print(sl)
        if curr_scr == 'new_student9':
            self.root.ids.scr_mg_as.current = 'new_student10'
            sl[2].append('new_student9')
            print(sl)

        if curr_scr == 'new_student10':
            print("end@")
            sl[2].append('new_student10')
            print(sl)

    def on_add_student_previous(self):
        global sl
        self.root.ids.scr_mg_as.current = sl[2][-1]
        sl[2].pop(-1)
        print(sl)


print(kivy.__version__)

if __name__ == '__main__':
    TryApp().run()
