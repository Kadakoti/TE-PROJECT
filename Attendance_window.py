from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication,QMainWindow
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import sys
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt
from csv import writer
import shutil
# class AddWindow(QMainWindow):
#     def __init__(self):
#         super(AddWindow,self).__init__()
#         uic.loadUi("./addwindow.ui",self)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("./outputwindow.ui", self)
        # Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.label_4.setText(current_date)
        self.label_5.setText(current_time)

        if (os.path.exists('encode.csv') and os.path.exists('name.txt') and os.path.exists('div.txt') and os.path.exists('rollno.txt'))== True:
            path = 'Add Images'
            attendance_list = os.listdir(path)
            if len(attendance_list)!=0:
                self.AddStudent(path, attendance_list)
            self.encode_list = loadtxt('encode.csv')
            self.class_names = []
            self.class_div = []
            self.Roll_no = []
            with open('name.txt', 'r') as filehandle:
                for line in filehandle:
                    currentPlace = line[:-1]
                    self.class_names.append(currentPlace)
            with open('div.txt', 'r') as filehandle:
                for line in filehandle:
                    currentPlace = line[:-1]
                    self.class_div.append(currentPlace)
            with open('rollno.txt', 'r') as filehandle:
                for line in filehandle:
                    currentPlace = line[:-1]
                    self.Roll_no.append(currentPlace)
        self.TimeList1 = []
        self.TimeList2 = []
        self.image = None
        date = str(np.datetime64('today', 'D'))
        self.attendance_file_name = './Attendance/' + date + '.csv'
        if(os.path.exists(self.attendance_file_name)==False):
            List = ['name', 'class', 'rollno', 'time', 'status']
            with open(self.attendance_file_name, 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()

    def AddStudent(self,path,attendance_list):
        images = []
        class_name=[]
        class_div=[]
        Roll_no=[]
        encode_list=[]
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            txt = os.path.splitext(cl)[0]
            data = txt.split('_')
            class_name.append(data[0])
            class_div.append(data[1])
            Roll_no.append(data[2])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encodes_cur_frame)
        data = np.array(encode_list)
        with open("encode.csv", "ab") as f:
            savetxt(f,data)
        # with open('encode.csv', 'a') as f_object:
        #     for i in range(len(encode_list)):
        #         ll=encode_list[i]
        #         writer_object = writer(f_object)
        #         writer_object.writerow(encode_list)
        #     f_object.close()
        file_object = open('name.txt', 'a')
        for i in range(len(class_name)):
            name=class_name[i]
            file_object.write('%s\n' %name)
        file_object.close()
        file_object = open('div.txt', 'a')
        for i in range(len(class_div)):
            div = class_div[i]
            file_object.write('%s\n' %div)
        file_object.close()
        file_object = open('rollno.txt', 'a')
        for i in range(len(Roll_no)):
            id = Roll_no[i]
            file_object.write('%s\n' %id)
        file_object.close()
        source_dir = './Add Images'
        target_dir = './Images'
        file_names = os.listdir(source_dir)
        for file_name in file_names:
            shutil.move(os.path.join(source_dir, file_name), target_dir)
        # for file in os.listdir(path):
        #         src_dir = "./Add Images"
        #         dst_dir = "./Images"
        #         shutil.move(src_dir, dst_dir)

    def startVideo(self, camera_name):
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
            self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        if (os.path.exists('encode.csv') and os.path.exists('name.txt') and os.path.exists('div.txt') and os.path.exists('rollno.txt')) == False:
            for file in os.listdir('Add Images'):
                src_dir = "./Add Images"
                dst_dir = "./Images"
                shutil.move(src_dir, dst_dir)
            path = 'Images'
            if not os.path.exists(path):
                os.mkdir(path)
            # known face encoding and known face name list
            images = []
            self.class_names = []
            self.class_div = []
            self.Roll_no = []
            self.encode_list = []
            self.TimeList1 = []
            self.TimeList2 = []
            attendance_list = os.listdir(path)

        # print(attendance_list)
            for cl in attendance_list:
                cur_img = cv2.imread(f'{path}/{cl}')
                images.append(cur_img)
                txt = os.path.splitext(cl)[0]
                data = txt.split('_')
                self.class_names.append(data[0])
                self.class_div.append(data[1])
                self.Roll_no.append(data[2])
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(img)
                encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
                # encode = face_recognition.face_encodings(img)[0]
                self.encode_list.append(encodes_cur_frame)
            with open('name.txt', 'w') as filehandle:
                for names in self.class_names:
                    filehandle.write('%s\n' % names)
            with open('div.txt', 'w') as filehandle:
                for div in self.class_div:
                    filehandle.write('%s\n' % div)
            with open('rollno.txt', 'w') as filehandle:
                for id in self.Roll_no:
                    filehandle.write('%s\n' % id)
            data1 = self.encode_list
            data = np.array(data1)
            savetxt('encode.csv', data)

        self.ClockInButton.clicked.connect(self.update_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names,class_div,Roll_no):
        def mark_attendance(name,class_names,class_div,Roll_no):
            if self.ClockInButton.isChecked():
                self.ClockInButton.setEnabled(False)
                with open(self.attendance_file_name, 'a') as f:
                    if name != 'unknown':
                        buttonReply = QMessageBox.question(self, 'Welcome ' + name, 'Are you Clocking In?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            i = class_names.index(name)
                            Div = class_div[i]
                            Id = Roll_no[i]
                            f.writelines(f'\n{name},{Div},{Id},{date_time_string},Clock In')
                            self.ClockInButton.setChecked(False)
                            self.NameLabel.setText(name)
                            self.DivLabel.setText(Div)
                            self.IdLabel.setText(Id)
                            self.StatusLabel.setText('Clocked In')
                            self.HoursLabel.setText('Measuring')
                            #self.MinLabel.setText('')
                            # self.CalculateElapse(name)
                            # print('Yes clicked and detected')
                            self.Time1 = datetime.datetime.now()
                            # print(self.Time1)
                            self.ClockInButton.setEnabled(True)
                        else:
                            print('Not clicked.')
                            self.ClockInButton.setEnabled(True)
            elif self.ClockOutButton.isChecked():
                self.ClockOutButton.setEnabled(False)
                with open(self.attendance_file_name, 'a') as f:
                    if name != 'unknown':
                        buttonReply = QMessageBox.question(self, 'Cheers ' + name, 'Are you Clocking Out?',
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            date_time_string = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            i = class_names.index(name)
                            Div = class_div[i]
                            Id = Roll_no[i]
                            f.writelines(f'\n{name},{Div},{Id},{date_time_string},Clock Out')
                            self.ClockOutButton.setChecked(False)

                            self.NameLabel.setText(name)
                            self.DivLabel.setText(Div)
                            self.IdLabel.setText(Id)
                            self.StatusLabel.setText('Clocked Out')
                            self.Time2 = datetime.datetime.now()
                            # print(self.Time2)
                            self.ElapseList(name)
                            self.TimeList2.append(datetime.datetime.now())
                            CheckInTime = self.TimeList1[-1]
                            CheckOutTime = self.TimeList2[-1]
                            self.ElapseHours = (CheckOutTime - CheckInTime)
                            #self.MinLabel.setText(
                             #   "{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60) % 60) + 'm')
                            x = self.ElapseHours.total_seconds()
                            s = x % 60
                            self.HoursLabel.setText(
                                "{:.0f}".format(abs(x / 60 ** 2)) + 'h '
                                "{:.0f}".format(abs(x / 60) % 60) + 'm '
                                 "{:.0f}".format(abs(s)) + 's ')
                            self.ClockOutButton.setEnabled(True)
                        else:
                            print('Not clicked.')
                            self.ClockOutButton.setEnabled(True)
        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.60)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            dis = str(np.round_(np.min(face_dis),decimals=3))
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            if match[best_match_index]:
                name = class_names[best_match_index]
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 40), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 24), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
                cv2.putText(frame, dis, (x1 + 6, y2 - 0), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
                i = class_names.index(name)
                Div = class_div[i]
                Id = Roll_no[i]
                self.NameLabel.setText(name)
                self.DivLabel.setText(Div)
                self.IdLabel.setText(Id)
            #if self.ClockInButton.isChec
            mark_attendance(name,class_names,class_div,Roll_no)

        return frame

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def ElapseList(self, name):
        with open(self.attendance_file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'Clock In':
                            if row[0] == name:
                                # print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[3], '%y/%m/%d %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'Clock Out':
                            if row[0] == name:
                                # print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[3], '%y/%m/%d %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                # print(Time2)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names,self.class_div,self.Roll_no, 1)

    def displayImage(self, image, encode_list, class_names,class_div,Roll_no, window=1):

        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names,class_div,Roll_no)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

