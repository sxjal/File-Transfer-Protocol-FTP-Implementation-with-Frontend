import struct
import os

def local_files():
    
    files_dict = {}
    print ("Local Files")
    
    for file_name in os.listdir("Files"):
        file_size = os.path.getsize(os.path.join("Files",file_name))
        files_dict[file_name] = file_size
        print(f"{file_name} | {file_size} bytes")

    return "200" 

def files_on_server(conn):
   
    print("Requesting files...\n")
    file_dict = {}
    try:
        # First get the number of files in the directory
        number_of_files = struct.unpack("i", conn.recv(4))[0]
        print(f"number_of_files {number_of_files}")
        # Then enter into a loop to receive details of each, one by one
        for i in range(int(number_of_files)):
            # Get the file name size first to slightly lessen amount transferred over socket
           
            file_name_size = struct.unpack("i", conn.recv(4))[0]
            conn.send("351".encode())
            print(f"file_name_size {file_name_size}")
           
            file_name = conn.recv(file_name_size).decode()
            conn.send("352".encode())
            
            # Also get the file size for each item in the server
            file_size = struct.unpack("i", conn.recv(4))[0]
            conn.send("353".encode())
            print(f"file_size {file_size}")
             
            file_dict[file_name] = file_size
             
            # Make sure that the client and server are synchronized
            conn.send("200".encode())
        # Get total size of directory
        for file_name, file_size in file_dict.items():
            print(f"{file_name} | {file_size} bytes")
            
        total_directory_size = struct.unpack("i", conn.recv(4))[0]  
        conn.send("355".encode())
        print("Total directory size: {}b".format(total_directory_size))
    except Exception as e:
        print("Couldn't retrieve listing")
        print(e)
        return "205"
    try:
        # Final check
        conn.send("200".encode())
        return "200"
    except Exception as e:
        print("Couldn't get final server confirmation")
        print(e)
        return "205"

