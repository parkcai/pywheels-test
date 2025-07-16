from time import sleep
from pywheels.file_tools import guarantee_file_exist
from pywheels.file_tools import copy_file
from pywheels.file_tools import delete_file


def main():
    
    guarantee_file_exist(
        file_path = "file_tools-test/temp_folder",
        is_directory = True,
    )
    
    print("Temp folder has been created."); sleep(6)
    
    guarantee_file_exist("file_tools-test/temp_folder/temp_file1.txt")
    
    print("Temp file 1 has been created."); sleep(6)
    
    copy_file(
        source_file_path = "file_tools-test/temp_folder/temp_file1.txt",
        destination_file_path = "file_tools-test/temp_folder/temp_file2.txt",
    )
    
    print("Temp file 1 has been copied to temp file 2."); sleep(6)
    
    delete_file("file_tools-test/temp_folder")
    
    print("Temp folder has been removed recursively.")
    
    
if __name__ == "__main__":
    
    main()
    
