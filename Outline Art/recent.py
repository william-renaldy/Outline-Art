import csv
import os 

def save(last_file):

    if last_file not in ("Sample_1.jpg","Sample_2.jpg","Sample_3.jpg","Sample_4.jpg"):
        recent_files=[last_file]

        with open("recent.csv","r") as f:
            reader=csv.reader(f)
            
            for row in reader:
                existing_files=row


        if "existing_files" not in locals():
            existing_files=[]


        recent_files.extend(existing_files)

        with open("recent.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(recent_files)



def load():
    with open("recent.csv","r") as f:
        reader=csv.reader(f)
        
        for row in reader:
            recent_files=row
        
    if "recent_files" not in locals():
        recent_files=[]
        
    return recent_files


def remove(file_name):

    recent_files = load()

    if file_name in recent_files:
        recent_files.remove(file_name)
        with open("recent.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(recent_files)

def check_exist():
    files=load()
    recent_files=[]
    for f in files:
        if os.path.exists(f):
            recent_files.append(f)

    with open("recent.csv","w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(recent_files)