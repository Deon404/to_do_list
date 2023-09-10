from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label
from kivy.config import Config

# Set the app icon (replace 'icon.png' with your icon file)
Config.set('kivy', 'window_icon', 'app_icon.png')



class TodoListApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.load_tasks()

    def build(self):
        self.title = "To-Do List [Sidon]"
        root = BoxLayout(orientation='vertical', padding=10)
        
        self.task_input = TextInput(hint_text="Enter a task", multiline=False, size_hint=(1, None))
        add_button = MDRaisedButton(text="Add Task", size_hint=(1, None), on_release=self.add_task)
        
        self.task_list = BoxLayout(orientation='vertical', spacing=5)
        
        root.add_widget(self.task_input)
        root.add_widget(add_button)
        root.add_widget(self.task_list)
        
        self.update_task_list()
        
        return root
    


    def add_task(self, instance):      
       task_text = self.task_input.text.strip()
       if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.save_tasks()
            self.update_task_list()
            self.task_input.text = ""

    def update_task_list(self):
        self.task_list.clear_widgets()
        for index, task_data in enumerate(self.tasks):
            task_text = task_data["text"]
            completed = task_data["completed"]
            task_label = Label(text=f"{index + 1}. {task_text}", color=(0, 0, 0, 1) if not completed else (0.5, 0.5, 0.5, 1))
            
            delete_button = MDRaisedButton(text="Delete", size_hint=(None, None), height=30, on_release=lambda x, idx=index: self.delete_task(idx))
            
            complete_button_text = "Complete" if not completed else "Incomplete"
            complete_button = MDRaisedButton(text=complete_button_text, size_hint=(None, None), height=30, on_release=lambda x, idx=index: self.toggle_complete_task(idx))
            
            task_layout = BoxLayout(orientation='horizontal', spacing=5)
            task_layout.add_widget(task_label)
            task_layout.add_widget(delete_button)
            task_layout.add_widget(complete_button)
            
            self.task_list.add_widget(task_layout)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            self.update_task_list()

    def toggle_complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.update_task_list()

    def save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task_data in self.tasks:
                file.write(f"{task_data['text']}|{task_data['completed']}\n")

    def load_tasks(self):
        try:
            with open('tasks.txt', 'r') as file:
                for line in file.readlines():
                    task_text, completed = line.strip().split("|")
                    self.tasks.append({"text": task_text, "completed": completed == "True"})
        except FileNotFoundError:
            self.tasks = []

if __name__ == '__main__':
    TodoListApp().run()
