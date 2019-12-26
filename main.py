import os
from kivy.clock import Clock
import kivy
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import data_supply as ds
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.utils.cropimage import crop_image

student_list = []


class ScreenManager1(ScreenManager):
    def do_it(self):
        print(self.ids.client.text)

    def add_student_list(self):
        print(self.ids.scr_mg1.current == 'Student_List')

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

    def login_admin(self, admin_id, pswd):
        x = ds.on_login_admin(admin_id, pswd)
        if x[0] == 'Login Successful':
            self.current = 'screenA'
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
        print("added")


print(kivy.__version__)

if __name__ == '__main__':
    TryApp().run()
