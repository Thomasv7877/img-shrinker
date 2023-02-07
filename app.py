from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget, QGridLayout, QSlider
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
#from pyqt6_tools import *
from PIL import Image
import sys
import os


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Shrinker")
        self.resize(800, 600)
        self.setAcceptDrops(True)

        self.button1 = QPushButton(self)
        self.button1.setText("Shrink to 33%")
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setFixedWidth(self.width())

        self.imageHeight = self.height() - self.button1.height()

        self.label = QLabel(self)
        self.label.setText("Drag image(s) here\n+")
        self.label.setFont(QFont('Arial', 16))
        self.label.setAlignment(Qt.Alignment.AlignCenter)
        self.label.setFixedHeight(self.imageHeight)
        self.blankLabel = True
        
        self.slider = QSlider(Qt.Orientations.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(33)
        self.slider.valueChanged.connect(self.valuechange)

        self.urls = []
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 0, 0, Qt.Alignment.AlignCenter)
        widget = QWidget()
        widget.setMaximumWidth(self.width())
        widget.setMaximumHeight(self.height() - self.button1.height()) # - self.slider.height()
        widget.setLayout(self.grid)

        #test_urls = [ [10,12,14] ,[0,1,2] ]
        # test_urls = [[1]]
        # print(len(test_urls[0]))
        # newpos = []
        # fd = len(test_urls) - 1
        # if len(test_urls[fd]) / 4 == 1:
        #     fd = fd + 1
        # sd = len(test_urls[fd]) % 4
        # if len(self.urls) == 0:
        #     sd = 0

        # newpos.append(fd)
        # newpos.append(sd)
        # print(newpos)

        layout = QVBoxLayout()
        layout.addStretch()
        #layout.addWidget(self.label)
        layout.addWidget(widget)
        #layout.addWidget(button1, alignment=Qt.Alignment.AlignBottom)
        layout.addWidget(self.slider)
        layout.addWidget(self.button1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # def dropEvent(self, event):
    #     files = [u.toLocalFile() for u in event.mimeData().urls()]
    #     for f in files:
    #         print(f)
    #         self.imagePath = f
    #         pixmap = QPixmap(f)
    #         self.label.setPixmap(pixmap.scaled(self.width(),self.imageHeight,aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
    #         self.label.setAlignment(Qt.Alignment.AlignCenter)

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            pixmap = QPixmap(f)
            tempLabel = QLabel()
            tempLabel.setPixmap(pixmap.scaled(self.width() / 4,self.imageHeight,aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            #tempLabel.setPixmap(pixmap.scaled(self.width(),self.imageHeight,aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode= Qt.TransformationMode.SmoothTransformation))
            #tempLabel.setPixmap(pixmap)
            #tempLabel.setAlignment(Qt.Alignment.AlignCenter)
            print(self.getPos())
            pos = self.getPos()
            self.grid.addWidget(tempLabel, pos[0], pos[1], Qt.Alignment.AlignCenter)
            self.urls.append(f)

    def compressMe(self, files):
        for file in files:
            filepath = os.path.join(os.getcwd(), file)
            picture = Image.open(filepath)
            ext = file[-3:]
            proto = "JPEG" if ext.lower() == 'jpg' else "png"
            picture.save(file[:-4] + "_Compressed." + ext, proto, optimize = True, quality = self.slider.value())

    def button1_clicked(self, event):
        #print("Button 1 clicked for image: " + self.imagePath)
        self.compressMe(self.urls)

    def getPos(self):
        length = len(self.urls)
        x = int(length / 4)
        y = length % 4
        # if self.blankLabel:
        #     y = y - 1
        #     self.blankLabel = False
        return [x,y]
        
    def valuechange(self):
      size = self.slider.value()
      self.button1.setText("Shrink to " + str(size) + "%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec())