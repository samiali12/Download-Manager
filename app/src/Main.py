
# PyQt framework modules
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import  loadUiType

# python buil-tin or default modules
import sys
import urllib.request
import requests
import os
import datetime

# third party modules 
import humanize
from pafy import *




ui,_ = loadUiType(r'E:\video downloader\app\src\app.ui')

class App(QMainWindow, ui):

    def __init__(self, parent=None):
        super(App,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.InitUI()
        self.Handle_Buttons()


    def InitUI(self):
        pass

    def Handle_Buttons(self):

        #first two push button is handle event about files download from internet e.g html,pytho.. etc.
        self.pushButton.clicked.connect(self.Download)
        self.toolButton1.clicked.connect(self.Handle_Browse)
        # below push button is handle event about youtube video download tabs
        self.pushButton_7.clicked.connect(self.get_videoData)
        self.pushButton_8.clicked.connect(self.videoBrowse)
        self.pushButton_9.clicked.connect(self.videoDownload)
        # below push buttons is handle event about youtube playlist download tabs
        self.pushButton_4.clicked.connect(self.getVideoPlaylistData)
        self.pushButton_3.clicked.connect(self.videPlaylistBrowse)

    def Handle_Progress(self, blocknum, blocksize, total_size):
        readed_data = blocknum * blocksize
        if total_size > 0:
            percentage = (readed_data * 100) / total_size
            self.progressBar.setValue(percentage)
            QApplication.processEvents()


    def Handle_Browse(self):

        all_filter_files = "*.txt *.html *.pdf *.py *"
        save_locations = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter=all_filter_files)
        self.lineEdit2.setText(str(save_locations[0]))


    def Download(self):
        downloading_link = self.lineEdit1.text()
        save_file_path   = self.lineEdit2.text()

        if downloading_link == '':
            QMessageBox.warning(self,"URL Error", "Insert valid url")
        elif save_file_path == '':
            QMessageBox.warning(self,"Path Error", "Provide valid path")
        else:
            self.pushButton.setEnabled(False)
            self.lineEdit1.setEnabled(False)
            self.lineEdit2.setEnabled(False)

            try:
                urllib.request.urlretrieve(downloading_link, save_file_path, self.Handle_Progress)    
            except ValueError:

                QMessageBox.warning(self,"URL Error", "Unknow url type")
                self.lineEdit1.setText("")
                self.pushButton.setEnabled(True)
                self.lineEdit1.setEnabled(True)
                self.lineEdit2.setEnabled(True)

        QMessageBox.information(self,"Download","Download complete successfully")
        self.lineEdit1.setEnabled(True)
        self.lineEdit2.setEnabled(True)
        self.lineEdit1.setText("")
        self.lineEdit2.setText("")
        self.pushButton.setEnabled(True)
        self.progressBar.setValue(0)

    def get_videoData(self):
        videoURL = self.lineEdit_5.text()

        if videoURL == "":
            QMessageBox.warning(self,"URL Error", "Insert valid url")
            self.lineEdit_3.setText("")
        else:
            timeout = 5
            connection = True
            try:    
                request = requests.get(videoURL, timeout=timeout)
                QMessageBox.information(self,"Internet connection","Checking internet connection Please wait...")
            except(requests.ConnectionError, requests.Timeout) as exception:
                QMessageBox.warning(self,"Internet Connection","No internet connection found")
                
            while connection:
                try:    
                    request = requests.get(videoURL, timeout=timeout)
                except Exception:
                    pass
                else:
                    QMessageBox.information(self,"Internet Connection","Connected to internet")
                    connection = False

            videoURL = self.lineEdit_5.text()

            if videoURL == "":
                QMessageBox.warning(self,"URL Error", "Insert valid url")
                self.lineEdit_5.setText("")
            else:
                try:
                    video = pafy.new(videoURL)
                    video_stream = video.videostreams
                    
                    for stream in video_stream:
                        size = humanize.naturalsize(stream.get_filesize())
                        data = "{} {} {} {}".format(stream.mediatype,stream.extension, stream.quality,size)
                        self.videoQualityCombox.addItem(data)
                    
                    self.label_5.setText("Video : "+str(video.title))

                except ValueError:
                    QMessageBox.warning(self,"Video URL", "Invalid video URL")
                    self.lineEdit_5.setText("")

    def videoBrowse(self):
        save_locations = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="Videos (*.mp4 *.webm)")
        self.lineEdit_6.setText(str(save_locations[0]))

    def videoDownload(self):
        videoURL = self.lineEdit_5.text()
        videoSaveLocation = self.lineEdit_6.text()
        videoQuality = self.videoQualityCombox.currentIndex()

        print(videoQuality)

        if videoSaveLocation == "":
            QMessageBox.warning(self,"Path","Invalid path")
        else:
            video = pafy.new(videoURL)
            videoStream = video.videostreams
            download = videoStream[videoQuality].download(filepath=videoSaveLocation, callback=self.videoProgressbar)

        QMessageBox.information(self,"Downloading complete","Your Video has sucessfully download")
        self.progressBar_3.setValue(0)


    def videoProgressbar(self, total, recev, ratio, rate, time):
        receive_data = recev
        speed_rate = humanize.naturalsize(rate)
        remaining_time = str(datetime.timedelta(seconds = time))

        if total > 0:
            download_percentage = receive_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            self.label_10.setText(str(" {} KB/s".format(speed_rate[0:4])))
            self.label_12.setText(str(remaining_time))
            QApplication.processEvents()

                                ##########################################
                                ####### youtube video playlist coding ####
                                ##########################################

    def getVideoPlaylistData(self):
        playlist_url = self.lineEdit_3.text()
        playlist_path = self.lineEdit_4.text()
        timeout = 5
        connection = True

        if playlist_url == "":
            QMessageBox.warning(self,"URL Error", "Insert valid url")
            self.lineEdit_3.setText("")

        if playlist_path == "":
            QMessageBox.information(self,"Path","Invalid playlist path")

        else:
            try:    
                request = requests.get(playlist_url, timeout=timeout)
                QMessageBox.information(self,"Internet connection","Checking internet connection Please wait...")

            except(requests.ConnectionError, requests.Timeout) as exception:
                QMessageBox.warning(self,"Internet Connection","No internet connection found")
                
            while connection:
                try:
                    request = requests.get(playlist_url, timeout=timeout)
                except Exception:
                    pass
                else:

                    QMessageBox.information(self,"Internet Connection","Connected to internet")
                    connection = False
            
            playlist = get_playlist(playlist_url)
            playlist_videos = playlist['items'] 
            self.labelTotalVideos.setText(str(len(playlist_videos)))
            os.chdir(playlist_path)

            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))
            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            video_count = 1
            quality = self.comboBox.currentIndex()

            for  current_videos in playlist_videos:
                self.labelRemainingVideos.setText(str(len(playlist_videos) - video_count))
                current_video = current_videos['pafy']
                print(current_video)
                stream = current_video.videostreams
                download = stream[quality].download(callback=self.playlistProgressBar)
                video_count += 1

            QMessageBox.information(self,"Download Complete","Your playlist has been downloaded")

    def videPlaylistBrowse(self):
        save_locations = QFileDialog.getExistingDirectory(self,"Select download path")
        self.lineEdit_4.setText(save_locations)

    def playlistProgressBar(self,total, recev, ratio,rate,  time):
        receive_data = recev
        speed_rate = humanize.naturalsize(rate)
        remaining_time = str(datetime.timedelta(seconds = time))

        if total > 0:
            download_percentage = receive_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            self.label_13.setText(str(" {} KB/s".format(speed_rate[0:3])))
            self.label_7.setText(str(remaining_time))
            QApplication.processEvents()

# main function start from here 
if __name__ == "__main__":
    application = QApplication(sys.argv)
    appWindow   = App()
    appWindow.show()
    sys.exit(application.exec_())