import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import shutil
import os


class ConnectPage(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Directory: '))
        self.dir = TextInput()
        self.dir.text = "/storage/emulated/0/DCIM/Camera"
        self.add_widget(self.dir)
        self.add_widget(Label())
        self.submit = Button(text=' process')
        self.submit.bind(on_press=self.process_func)
        self.add_widget(self.submit)

    def process_func(self, instance):
        app.process_page.clear_info()
        directory = self.dir.text

        if not directory.strip():
            app.process_page.update_info('Please enter directory')
            app.screen_manager.current = "process"

        elif not os.path.exists(directory):
            app.process_page.update_info('Invalid directory')
            app.screen_manager.current = "process"
        else:
            all_files = os.listdir(directory)

            folders = [file for file in all_files if os.path.isdir(
                os.path.join(directory, file)) and file.startswith('IMG')]
            print('all_files: ', all_files)
            print('folders: ', folders)

            for folder in folders:
                for file in os.listdir(os.path.join(directory, folder)):
                    source = os.path.join(directory, folder, file)
                    destination = os.path.join(directory, file)
                    shutil.move(source, destination)
                    info = '\n copying: ' + file + '\n'
                    app.process_page.update_info(info)
                    app.screen_manager.current = "process"
            # delete folders
            app.process_page.update_info('Completed')
            app.screen_manager.current = "process"
            for folder in folders:
                os.rmdir(os.path.join(directory, folder))


class ProcessPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center", valign='middle', font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
        self.home_btn = Button(text='Home')
        self.home_btn.bind(on_press=self.redirect_home)
        self.add_widget(self.home_btn)

    def update_info(self, message):
        self.message.text += message

    def clear_info(self):
        self.message.text = ''

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

    def redirect_home(self, instance):
        app.screen_manager.current = "Welcome"


class Epic(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.connect_page = ConnectPage()
        screen = Screen(name='Welcome')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.process_page = ProcessPage()
        screen = Screen(name='process')
        screen.add_widget(self.process_page)
        self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    app = Epic()
    app.run()
