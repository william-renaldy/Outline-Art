import PIL
from PIL import Image as im

import kivy
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.button import Button 
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image 
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivy.utils import platform
import threading
import os

import camera
import pencil
import recent

path=os.getcwd()

if platform == "android":
    import android
    from android.permissions import request_permissions, Permission 
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.INTERNET,Permission.CAMERA,Permission.MANAGE_DOCUMENTS])
    from android.storage import primary_external_storage_path

    primary_external_storage=primary_external_storage_path()

    path=os.path.join(primary_external_storage,"Outline Art")
    os.makedirs(path,exist_ok=True)
    
    path1=os.path.join(path,"Images")
    os.makedirs(path1,exist_ok=True)

    os.makedirs(os.path.join(path,"Sample"),exist_ok=True)

else:
    path1=os.path.join(path,"Images")
    os.makedirs(path1,exist_ok=True)
    os.makedirs(os.path.join(path1,"Sample"),exist_ok=True)



x=Window.size[0] #800
y=Window.size[1] #600


Window.clearcolor=(255/255,182/255,193/255,0)
#Window.clearcolor=(1,1,240/255,0)


class outline_art(GridLayout):
    def __init__(self,**kwargs):
        super(outline_art,self).__init__(**kwargs)

        self.cols=1
        Window.bind(on_keyboard=self.on_key)

        self.is_editor=False



        self.main_grid=GridLayout(cols=1,size_hint=(None,None),size=(x,y))
        self.add_widget(self.main_grid)

    
        #Top Grid
        self.top_grid=GridLayout(cols=2,size_hint=(None,None),size=(x,1.25*y/8))
        self.main_grid.add_widget(self.top_grid)
        self.top_grid.add_widget(Button(background_normal="top_info.jpg",background_down="top_info.jpg"))
      




        #Mid Grid
        self.mid_grid=GridLayout(cols=7,size_hint=(None,None),size=(x,2*y/8))
        self.main_grid.add_widget(self.mid_grid)
        y_mid=y/8
        

        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))




        self.mid_grid.add_widget(Label())
        self.recent_button=Button(background_normal="recent.jpg",background_down="recent.jpg")
        self.mid_grid.add_widget(self.recent_button)
        self.recent_button.bind(on_press=self.recent_function)
        self.mid_grid.add_widget(Label())

        self.choose_button=Button(background_normal="gallery.jpg",background_down="gallery.jpg")
        self.mid_grid.add_widget(self.choose_button)
        self.choose_button.bind(on_press=self.filechooser_func)


        self.mid_grid.add_widget(Label())

        self.camera_button=Button(background_normal="camera.jpg",background_down="camera.jpg")
        self.mid_grid.add_widget(self.camera_button)
        self.camera_button.bind(on_press=self.capture)
        

        self.mid_grid.add_widget(Label())





        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(2*x/10,y_mid/5)))
        self.mid_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))



        self.separator_grid=GridLayout(cols=1,size_hint=(None,None),size=(x,0.75*y/8))
        self.main_grid.add_widget(self.separator_grid)

        self.separator_grid.add_widget(Button(background_normal="line.jpg",background_down="line.jpg"))
        self.separator_grid.add_widget(Label(text="Sample Images",text_size=(x/1.05,None),color=(0,0,0,1),font_size=20))



 




        #Bottom Grid
        self.bottom_grid=GridLayout(cols=5,size_hint=(None,None),size=(x,4*y/8))
        self.main_grid.add_widget(self.bottom_grid)
        
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))


        self.bottom_grid.add_widget(Label())
        
        self.sample1=Button(background_normal="_12345_img_app_sample_10012022_1.jpg", background_down="_12345_img_app_sample_10012022_1.jpg")
        self.bottom_grid.add_widget(self.sample1)
        self.sample1.bind(on_press=self.editor_window)
        print(self.sample1.size)

        self.bottom_grid.add_widget(Label())

        self.sample2=Button(background_normal="_12345_img_app_sample_11012022_2.jpg", background_down="_12345_img_app_sample_11012022_2.jpg")
        self.bottom_grid.add_widget(self.sample2)
        self.sample2.bind(on_press=self.editor_window)

        self.bottom_grid.add_widget(Label())


        

        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))


        self.bottom_grid.add_widget(Label())
        
        self.sample3=Button(background_normal="_12345_img_app_sample_11012022_3.jpg",background_down="_12345_img_app_sample_11012022_3.jpg")
        self.bottom_grid.add_widget(self.sample3)
        self.sample3.bind(on_press=self.editor_window)
        print(self.sample3.size)
  

        self.bottom_grid.add_widget(Label())

        self.sample4=Button(background_normal="_12345_img_app_sample_11012022_4.jpg",background_down="_12345_img_app_sample_11012022_4.jpg")
        self.bottom_grid.add_widget(self.sample4)
        self.sample4.bind(on_press=self.editor_window)

        self.bottom_grid.add_widget(Label())

        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(3.5*x/10,y_mid/5)))
        self.bottom_grid.add_widget(Label(size_hint=(None,None),size=(x/10,y_mid/5)))

        self.filechooser_popup=Popup(title="Choose the image")
     





        self.editor_grid=GridLayout(cols=1,size_hint=(None,None),size=(x,y))
 

        self.editor_topgrid=GridLayout(cols=5,size_hint=(None,None),size=(x,y/2))
        self.editor_grid.add_widget(self.editor_topgrid)

        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))


        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.normal_image=Image()
        self.editor_topgrid.add_widget(self.normal_image)
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.edited_image=Image()
        
        self.editor_topgrid.add_widget(self.edited_image)

        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))


        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))
        self.editor_topgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/18)))

        


        self.editor_convertgrid=GridLayout(cols=3,size_hint=(None,None),size=(x,y/8))
        self.editor_grid.add_widget(self.editor_convertgrid)

        self.editor_convertgrid.add_widget(Label(size_hint=(None,None),size=(x/4,y/8)))
        self.convert=Button(text='Convert')
        self.convert.bind(on_press=self.sketch)
        self.editor_convertgrid.add_widget(self.convert)
        self.editor_convertgrid.add_widget(Label(size_hint=(None,None),size=(x/4,y/8)))

        self.editor_infogrid=GridLayout(cols=1,size_hint=(None,None),size=(x,y/6))
        self.editor_grid.add_widget(self.editor_infogrid)

        self.editor_info=Label(text_size=(x/1.5,None))
        self.editor_infogrid.add_widget(self.editor_info)


        self.editor_bottomgrid=GridLayout(cols=5,size_hint=(None,None),size=(x,5*y/24))
        self.editor_grid.add_widget(self.editor_bottomgrid)

        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/8)))

        self.back_to_home=Button(text="Back")
        self.editor_bottomgrid.add_widget(self.back_to_home)
        self.back_to_home.bind(on_press=self.on_press_back)
        
        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/8)))
        self.choose_file=Button(text="Choose File")
        self.editor_bottomgrid.add_widget(self.choose_file)
        self.choose_file.bind(on_press=self.filechooser_func)

        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/8)))

        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/12)))
        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/12)))
        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/12)))
        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/12)))
        self.editor_bottomgrid.add_widget(Label(size_hint=(None,None),size=(x/15,y/12)))

        self.recent_popup=Popup(title="Recent")

        
    def on_key(self,keyboard,keycode,*args):
        if keycode==27 and self.is_editor==True:
            self.on_press_back(None)
        elif keycode==27 and self.is_editor==False:
            Config.set("kivy","exit_on_escape","1")



    def filechooser_func(self,instance):
        if platform=="android":
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])
        self.filechooser_grid=GridLayout(cols=1)

        self.filechooser_maingrid=GridLayout(cols=1)
        self.filechooser_grid.add_widget(self.filechooser_maingrid)



        self.filechooser_bottomgrid=GridLayout(cols=1,size_hint=(None,None),size=(x,y/15))
        self.filechooser_grid.add_widget(self.filechooser_bottomgrid)

        self.select_button=Button(text='Select')
        self.filechooser_bottomgrid.add_widget(self.select_button)
        self.select_button.bind(on_press=self.file_selected_func)
        self.filechooser=FileChooserIconView()
        self.filechooser_maingrid.add_widget(self.filechooser)
        self.filechooser.filters=['*.png','*.jpg','*.jpeg','*svg']
        self.filechooser_popup.content=self.filechooser_grid
        self.filechooser_popup.open()


    def recent_function(self,instance):

        self.recent_grid=GridLayout(cols=1,size_hint=(None,None))
        self.recent_scroll=ScrollView(do_scroll_y=True)
        self.recent_scroll.add_widget(self.recent_grid)

        recent.check_exist()

        self.recent_images=recent.load()

        self.recent_image_button=[x for x in range(len(self.recent_images))]

        for index,name in enumerate(self.recent_images):
            self.recent_image_button[index]=Button(text=name,size_hint=(None,None),size=(x,y/8))
            self.recent_grid.add_widget(self.recent_image_button[index])
            self.recent_image_button[index].bind(on_press=self.editor_window)


        self.recent_grid.height=len(self.recent_images)*y/8

        if self.recent_image_button==[]:
            self.recent_popup.content=Label(text="No Recent Images",font_size=24)
        else:
            self.recent_popup.content=self.recent_scroll

        self.recent_popup.open()



    def on_press_back(self,instance):
        try:
            self.filechooser_popup.dismiss()
            self.remove_widget(self.editor_grid)
        except Exception as e:
            print(e)

        self.add_widget(self.main_grid)
        self.is_editor=False
        Window.clearcolor=(255/255,182/255,193/255,0)
        self.normal_image.source=""
        self.edited_image.source=""
        self.normal_image.reload()
        self.edited_image.reload()
        self.editor_info.text=""
        


    def file_selected_func(self,instance):

        if self.filechooser.selection!=[]:
            self.image_src=self.filechooser.selection[0]
            self.filechooser_popup.dismiss()
            self.image_name=os.path.split(self.image_src)[1]
            self.image_dir=os.path.split(self.image_src)[0]
            self.editor_window(None)


        
    def editor_window(self,instance):
        try:
            self.remove_widget(self.main_grid)
        except:
            pass

        try:
            self.filechooser_popup.dismiss()
        except:
            pass
        
        try:
            self.recent_popup.dismiss()
        except:
            pass
            

        Window.clearcolor=(30/255,30/255,30/255,0)
        self.is_editor=True
        Config.set("kivy","exit_on_escape","0")

        try:
            if instance in self.recent_image_button:
                self.image_src=instance.text
                self.image_name=os.path.split(self.image_src)[1]
                self.image_dir=os.path.split(self.image_src)[0]
        except:
            pass


        if instance in (self.sample1,self.sample2,self.sample3,self.sample4):
            self.image_dir=os.path.join(path,os.path.join("Images","Sample"))

            if instance==self.sample1:
                self.image_src="Sample_1.jpg"
                self.image_name="Sample_1.jpg"

            elif instance==self.sample2:
                self.image_src="Sample_2.jpg"
                self.image_name="Sample_2.jpg"

            elif instance==self.sample3:
                self.image_src="Sample_3.jpg"
                self.image_name="Sample_3.jpg"

            elif instance==self.sample4:
                self.image_src="Sample_4.jpg"
                self.image_name="Sample_4.jpg"



        try:
            self.add_widget(self.editor_grid)
        except:
            pass

        print(self.image_src)
        try:
            im.open(self.image_src)
        except PIL.UnidentifiedImageError:
            self.image_src="_no_image_found_.png"
            self.image_exist=False
        else:
            self.image_exist=True

        
        self.normal_image.source=self.image_src
        self.normal_image.reload()
 
        


    def capture(self,instance):
        self.capturing_grid=GridLayout(cols=1)
        self.capturing_label=Label(text="Capturing! Please Wait",font_size=20)
        self.capturing_grid.add_widget(self.capturing_label)
        self.captured_button=Button(text="Proceed")
        self.captured_button.bind(on_press=self.image_captured)
        self.capturing_popup=Popup(title="",size_hint=(None,None),size=(x/1.25,y/2),content=self.capturing_grid)
        self.capturing_popup.open()
        threading.Thread(target=self.capture_thread).start()

        
   

    def image_captured(self,instance):
        if instance.text=="Try Again":
            self.capturing_popup.dismiss()
            self.capture(None)

        else:
            self.capturing_popup.dismiss()
            self.editor_window(None)



    def capture_thread(self):
        if platform=="android":
            request_permissions([Permission.CAMERA])
        self.captured_image,self.image_name,self.image_dir,image_found=camera.capture(path)

        if (image_found):
            self.image_src=self.captured_image
            self.capturing_label.text="Image Captured"
            self.capturing_grid.add_widget(self.captured_button)

        else:
            self.image_src="_no_image_found_.png"
            self.capturing_label.text="Image Capturing Failed"
            self.captured_button.text="Try Again"
            self.capturing_grid.add_widget(self.captured_button)
    

    def sketch(self,instance):

        self.normal_image.reload()
        self.converted_image,image_converted=pencil.sketch(self.image_src,self.image_name,self.image_dir,self.image_exist)

        if(image_converted):
            self.edited_image.source=self.converted_image
            self.edited_image.reload()
            self.editor_info.text="Converted and Saved in {}".format(self.converted_image)
            recent.remove(self.image_src)
            recent.save(self.image_src)

        else:
            self.editor_info.text_size=(None,None)
            self.editor_info.text="Conversion Failed"

class myapp(App):
    def build(self):
        self.title="Outline Art"
        self.icon="logo.jpg"
        return outline_art()

if __name__=="__main__":
    myapp().run()