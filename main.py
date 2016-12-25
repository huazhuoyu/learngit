#-*-coding:utf-8;-*-
#qpy:2
#qpy:kivy

import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.listview import ListView,ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.pagelayout import PageLayout
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
import PIL
import os

class Picture(Scatter):
    source = StringProperty(None)


class HongBao(PageLayout):
    def __init__(self, **kwargs):
        super(HongBao, self).__init__(**kwargs)
        self.filename = kivy.resources.resource_find('/mnt/sdcard/com.hipipal.qpyplus/projects/hongbao/hb.jpg')
        self.init_ui()

    def add_arrt(self,gridLayout,attr_name,value):
        gridLayout.add_widget(Label(text=attr_name))
        attr_input = TextInput(text=value, multiline=False)
        gridLayout.add_widget(attr_input)

        return attr_input



    def init_ui(self):
        self.gridLayout=GridLayout(cols = 1,spacing = [0, 4])

        self.gridLayout1=GridLayout(cols = 2,spacing = [0, 9])

        self.color_min_input=self.add_arrt(self.gridLayout1,'color_min','20')
        self.color_max_input=self.add_arrt(self.gridLayout1,'color_max','120')
        self.fangcha_input=self.add_arrt(self.gridLayout1,'fangcha','15000')
        self.up_down_input=self.add_arrt(self.gridLayout1,'up_down','8')
        #self.left_right_input=self.add_arrt(self.gridLayout1,'left_right','0')


        self.jisuan_btn_a = Button(text='chick_a', )
        self.gridLayout1.add_widget(self.jisuan_btn_a)
        self.jisuan_btn_b = Button(text='chick_b',)
        self.gridLayout1.add_widget(self.jisuan_btn_b)

        self.gridLayout.add_widget(self.gridLayout1)

        self.jisuan_btn_a.bind(on_press=self.jisuan_a)
        self.jisuan_btn_b.bind(on_press=self.jisuan_b)

        self.image_hb = Image(source=self.filename)
        self.gridLayout.add_widget(self.image_hb)



        self.floatlayout = FloatLayout()
        self.fc = FileChooserListView()
        self.fc.path='/mnt/sdcard/DCIM/'
        self.floatlayout.add_widget(self.fc)
        self.get_file_btn = Button(text='chick_a', size_hint=(0.2, .1), pos=(20, 20))

        self.floatlayout.add_widget(self.get_file_btn)
        self.get_file_btn.bind(on_press=self.get_file)

        self.add_widget(self.floatlayout)
        self.add_widget(self.gridLayout)

    def get_file(self, instance):
        filename=os.path.join(os.path.dirname(self.filename),os.path.basename(self.fc.selection[0]))
        print self.fc.selection[0],' -'*20
        
        im_tmp=PIL.Image.open(self.fc.selection[0])
        w, h = im_tmp.size

        minx = int(w * 230.0 / 720)
        maxx = int(w * 487 / 720)
        miny = int(h * (1280 - 520) / 1280)
        maxy = int(h * (1280 - 264) / 1280)

        if h>1000:
            im_tmp=im_tmp.crop([minx, miny, maxx, maxy])

        im_tmp.save(filename, 'jpeg')
        self.filename=filename
        
        self.floatlayout.opacity=0
        self.updata_image()
        self.page=1
        print  'filename :',self.filename

    def remove_line(self,mode='a'):

        im2 = PIL.Image.open(self.filename)
        im3 = im2.copy()
        w2, h2 = im2.size
        im2_pix = im2.load()
        im3_pix = im3.load()

        color_min = int(self.color_min_input.text)
        color_max = int(self.color_max_input.text)
        fangcha_max = int(self.fangcha_input.text)
        up_down = int(self.up_down_input.text)
        black_in_line=False
        current_y=0


        for y in range(up_down+1, h2):
            x_color_r = 0
            x_color_g = 0
            x_color_b = 0
            for x in range(0, w2):
                r, g, b = im2_pix[x, y]
                x_color_r += r
                x_color_g += g
                x_color_b += b

            pingjun_r = x_color_r / w2
            pingjun_g = x_color_g / w2
            pingjun_b = x_color_b / w2

            fangcha_r = 0
            fangcha_g = 0
            fangcha_b = 0

            for x in range(0, w2):
                r, g, b = im2_pix[x, y]
                fangcha_r += abs(pingjun_r - r)
                fangcha_g += abs(pingjun_g - g)
                fangcha_b += abs(pingjun_b - b)

            if (fangcha_r + fangcha_g + fangcha_b) < fangcha_max and color_min < pingjun_r < color_max and color_min < pingjun_g < color_max and color_min < pingjun_b < color_max:
                #print y, '****' * 30, '  ', fangcha_r + fangcha_g + fangcha_b, pingjun_r, pingjun_g, pingjun_r
                if black_in_line==False:
                    current_y=y
                    black_in_line=True
                for x2 in range(0, w2):
                    if mode=='a':
                        im3_pix[x2, y] = im2_pix[x2, current_y-2]
                    else:
                        im3_pix[x2, y] = im2_pix[x2, y - up_down]
            else:
                
                if black_in_line==True:
                    black_in_line=False
                    if mode=='a':
                        for x2 in range(0, w2):
                            im3_pix[x2, y] = im2_pix[x2, current_y  - up_down]
                
                #print y, '----' * 30, '  ', fangcha_r + fangcha_g + fangcha_b, pingjun_r, pingjun_g, pingjun_r


        return im3


    def jisuan_a(self, instance):
        im3=self.remove_line().resize([600,600])
        filenamea=self.filename.rsplit('.',1)[0]+'a.jpg'
        im3.save(filenamea, 'jpeg')

        self.updata_image(filenamea)
        
    def jisuan_b(self, instance):
        im3 = self.remove_line('b').resize([600,600])
        filenamea = self.filename.rsplit('.', 1)[0] + 'a.jpg'
        im3.save(filenamea , 'jpeg')

        self.updata_image(filenamea)

    def updata_image(self,filenamea=None):
        if filenamea is None:
            filenamea=self.filename

        image_hb2 = Image(source=filenamea)
        self.gridLayout.remove_widget(self.image_hb)
        self.image_hb = image_hb2
        self.gridLayout.add_widget(self.image_hb, 0)
        self.image_hb.reload()



class TestApp(App):

    def build(self):
        return HongBao()
        
if __name__=='__main__':
    TestApp().run()