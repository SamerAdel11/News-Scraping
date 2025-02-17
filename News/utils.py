import os
class Save():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Gets the project root
    save_location = os.path.join(BASE_DIR, "Extracted Data")  # Creates an absolute path
    os.makedirs(save_location,exist_ok=True)

    @classmethod
    def text(cls,filename,data):
        if isinstance(data, list):
            file_path=os.path.join(cls.save_location,f"{filename}.txt")
            with open(file_path, "w") as file:
                file.writelines(f"{link}\n" for link in data)
        else:
            print("Data isn't list")

