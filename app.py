import glob
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk


def clock_tower() :
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, clock_tower)

def check_path(path) :
    dir = os.path.dirname(path)
    if not os.path.exists(dir) :
        os.makedirs(dir)

def check_haarcascade() :
    exists = os.path.isfile("Internal_files\\haarcascade_frontalface_default.xml")
    if exists :
        pass
    else :
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def regis_face() :
    window = tk.Tk()
    window.geometry("1200x720")

    window.title("FACE RECOGNITION ATTENDANCE SYSTEM")
    window.configure(background='#67f7ed')

    def start_capture() :
        check_haarcascade()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
        check_path("StudentDetails/")
        check_path("Training_images/")
        serial = 0
        exists = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists :
            with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1 :
                reader1 = csv.reader(csvFile1)
                for l in reader1 :
                    serial = serial + 1
            serial = (serial // 2)
            csvFile1.close()
        else :
            with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1 :
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1
            csvFile1.close()
        Id = (txt.get())
        name = (txt2.get())
        if ((name.isalpha()) or (' ' in name)) :
            cam = cv2.VideoCapture(0)
            harcascadePath = "Internal_files\\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True) :
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces :
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite(
                        "Training_images\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                        gray[y :y + h, x :x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q') :
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100 :
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            row = [serial, '', Id, '', name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile :
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message2.configure(text=res)
        else :
            if (name.isalpha() == False) :
                res = "Enter Correct name"
                message9.configure(text=res)

    def train_images() :
        check_haarcascade()
        check_path("Internal_files/")
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "Internal_files\\haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, ID = getImagesAndLabels("Training_images")
        try :
            recognizer.train(faces, np.array(ID))
        except :
            mess._show(title='No Registrations', message='Please Register someone first!!!')
            return
        recognizer.save("Internal_files\Trainner.yml")
        res = "Profile Saved Successfully"
        message2.configure(text=res)
        message9.configure(text='Total Registered Faces : ' + str(ID[0]))



    def getImagesAndLabels(path) :
        # get the path of all the files in the folder
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empth face list
        faces = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths :
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(ID)
        return faces, Ids


    datef = tk.Label(window, text=day + "-" + month + "-" + year, fg="black", bg="#67f7ed", width=20, height=1,
                     font=('times', 30, ' bold '))
    datef.place(x=360, y=70)

    message3 = tk.Label(window, text="REGISTER FACE", fg="red", bg="#30dbb9", width=55, height=1,
                        font=('serif', 35, ' bold '))
    message3.place(x=-190, y=0)

    id = tk.Label(window, text="ID or Roll No.", fg="black", bg="#67f7ed", width=40,
                  activebackground="white",
                  font=('times', 20, ' bold '))
    id.place(x=280, y=150)

    txt = tk.Entry(window, width=46, fg="black", font=('times', 20, ' bold '))
    txt.place(x=280, y=200)
    id = tk.Label(window, text="Name", fg="black", bg="#67f7ed", width=40,
                  activebackground="white",
                  font=('times', 20, ' bold '))
    id.place(x=280, y=250)

    txt2 = tk.Entry(window, width=46, fg="black", font=('times', 20, ' bold '))
    txt2.place(x=280, y=300)
    Button2 = tk.Button(window, text="Start Capturing", command=start_capture, fg="red", bg="#30dbb9", width=40,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    Button2.place(x=280, y=380)
    Button3 = tk.Button(window, text="Save Profile", command=train_images, fg="red", bg="#30dbb9", width=40,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    Button3.place(x=280, y=460)
    Button4 = tk.Button(window, text="Back", command=window.destroy, fg="red", bg="#30dbb9", width=40,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    Button4.place(x=280, y=540)

    message2 = tk.Label(window, text="", fg="black", bg="#67f7ed", width=40,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    message2.place(x=280, y=600)

    message9 = tk.Label(window, text="", fg="black", bg="#67f7ed", width=40,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    message9.place(x=280, y=650)

    res = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists :
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1 :
            reader1 = csv.reader(csvFile1)
            for l in reader1 :
                res = res + 1
        res = (res // 2) - 1
        csvFile1.close()
    else :
        res = 0
    message9.configure(text='Total Registered Faces : ' + str(res))

    window.mainloop()

def passwordo():


    f = open("Internal_files\password.txt", "r")
    key = f.read()

    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        regis_face()

    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def take_attendance():
    check_haarcascade()
    check_path("Attendance/")
    check_path("StudentDetails/")

    attendance=''
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("Internal_files\Trainner.yml")
    if exists3:
        recognizer.read("Internal_files\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "Internal_files\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)

        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + "_.csv")
    if exists:
        with open("Attendance\Attendance_" + date + "_.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + "_.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()

def view_attendance() :
    window = tk.Tk()
    window.geometry("1200x720")

    window.title("FACE RECOGNITION ATTENDANCE SYSTEM")
    window.configure(background='#67f7ed')

    datef = tk.Label(window, text="Today's Date : " + day + "-" + month + "-" + year, fg="black", bg="#67f7ed",
                     width=40, height=1,
                     font=('times', 30, ' bold '))
    datef.place(x=120, y=70)

    message3 = tk.Label(window, text="VIEW ATTENDANCE", fg="red", bg="#30dbb9", width=55, height=1,
                        font=('serif', 35, ' bold '))
    message3.place(x=-190, y=0)

    a = []
    b = []
    c = []
    m = glob.glob('Attendance\*.csv')
    for i in m :
        a = i.split('_')
        b = a[1]
        c.append(b)

    global tv
    tv = ttk.Treeview(window, height=13, columns=('name', 'date', 'time'))

    tv.column('#0', width=82)
    tv.column('name', width=130)
    tv.column('date', width=133)
    tv.column('time', width=133)
    tv.grid(row=7, column=4, padx=(250, 0), pady=(400, 0), columnspan=4)
    tv.heading('#0', text='ID')
    tv.heading('name', text='NAME')
    tv.heading('date', text='DATE')
    tv.heading('time', text='TIME')

    def get_data() :
        global tv
        for k in tv.get_children() :
            tv.delete(k)
        with open("Attendance\Attendance_" + clicked.get() + "_.csv", 'r') as csvFile1 :
            reader1 = csv.reader(csvFile1)
            i = 0

            for lines in reader1 :
                i = i + 1
                if (i > 1) :
                    if (i % 2 != 0) :
                        iidd = str(lines[0]) + '  '
                        tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))

    c = c[: :-1]
    options = c

    # datatype of menu text
    clicked = tk.StringVar(window)

    # initial menu text
    clicked.set(options[0])

    id = tk.Label(window, text="Select date", fg="black", bg="#67f7ed", width=40,
                  activebackground="white",
                  font=('times', 20, ' bold '))
    id.place(x=270, y=150)

    txt = tk.OptionMenu(window, clicked, *options)
    txt.config(width=43, fg="black", font=('times', 20, ' bold '))
    txt.place(x=280, y=200)

    Button2 = tk.Button(window, text="Get Data", command=get_data, fg="red", bg="#30dbb9", width=25,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    Button2.place(x=385, y=275)

    Button2 = tk.Button(window, text="Back", command=window.destroy, fg="red", bg="#30dbb9", width=25,
                        activebackground="white",
                        font=('times', 20, ' bold '))
    Button2.place(x=385, y=335)

    scroll = ttk.Scrollbar(window, orient='vertical', command=tv.yview)
    scroll.grid(row=7, column=4, padx=(820, 100), pady=(400, 0), sticky='ns')
    tv.configure(yscrollcommand=scroll.set)


ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%B-%Y')
day, month, year = date.split("-")



window = tk.Tk()
window.geometry("1200x720")
window.iconphoto(True, tk.PhotoImage(file="icon1.gif"))


window.title("FACE RECOGNITION ATTENDANCE SYSTEM")
window.configure(background='#67f7ed')

datef = tk.Label(window, text=day + "-" + month + "-" + year, fg="black", bg="#67f7ed", width=20, height=1,
                 font=('times', 30, ' bold '))
datef.place(x=350, y=70)

clock = tk.Label(window, fg="black", bg="#67f7ed", width=20, height=1, font=('times', 22, ' bold '))
clock.place(x=430, y=150)
clock_tower()

message3 = tk.Label(window, text="FACE RECOGNITION ATTENDANCE SYSTEM", fg="red", bg="#30dbb9", width=55, height=1,
                    font=('serif', 35, ' bold '))
message3.place(x=-190, y=0)


image1 = Image.open("icon1.jpg")
new=(160,160)
image1=image1.resize(new)
test = ImageTk.PhotoImage(image1)

label1 = tk.Label(image=test)
label1.image = test

# Position image
label1.place(x=518, y=200)






Button = tk.Button(window, text="Register Face", command=passwordo, fg="red", bg="#30dbb9", width=40,
                   activebackground="white",
                   font=('times', 20, ' bold '))
Button.place(x=280, y=380)
Button1 = tk.Button(window, text="Take Attendance", command=take_attendance, fg="red", bg="#30dbb9", width=40,
                    activebackground="white",
                    font=('times', 20, ' bold '))
Button1.place(x=280, y=460)
Button2 = tk.Button(window, text="View Attendance", command=view_attendance, fg="red", bg="#30dbb9", width=40,
                    activebackground="white",
                    font=('times', 20, ' bold '))
Button2.place(x=280, y=540)
Button3 = tk.Button(window, text="Quit", command=window.destroy, fg="red", bg="#30dbb9", width=40,
                    activebackground="white",
                    font=('times', 20, ' bold '))
Button3.place(x=280, y=620)

window.mainloop()
