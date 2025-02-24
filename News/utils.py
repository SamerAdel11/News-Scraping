import os
import shutil
class Save():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gets the project root
    save_location = os.path.join(BASE_DIR, "Extracted Data")  # Creates an absolute path
    os.makedirs(save_location,exist_ok=True)
    
    @classmethod
    def empty_folder(cls):
        for file in os.listdir(cls.save_location):
            file_path=os.path.join(cls.save_location,file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
    @classmethod
    def text(cls,filename,data):
        if isinstance(data, list):
            file_path=os.path.join(cls.save_location,f"{filename}.txt")
            with open(file_path, "w") as file:
                file.writelines(f"{link}\n" for link in data)
        else:
            print("Data isn't list")
    @classmethod
    def html(cls,filename,data):
        file_path=os.path.join(cls.save_location,f"{filename}.html")
        with open(file_path,"w") as file:
            file.write(str(data))
        

