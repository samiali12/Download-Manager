import urllib.request

request.

def videoProgressbar(self, total, recev, ration, rate, time):
        
        receive_data = recev

        if total > 0:
            download_percentage = receive_data * 100 / total
            #self.progressBar_3.setValue(download_percentage)
            QApplication.processEvents()
       #https://www.youtube.com/watch?v=eLk6ZCTtcvU   C:/Users/Home/Desktop/