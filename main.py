import io
import sys
import openpyxl
import folium
import json
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QMainWindow, QFileDialog

class Window(QMainWindow):

    def add_geometry(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '')[0]
        if fname:
            with open(fname, encoding='utf-8') as f:
                gj = json.load(f)
            for i in gj['features']:
                if i['geometry']['type'] == "Point":
                    self.add_point(i)
                elif i['geometry']['type'] == "LineString":
                    self.add_polyline(i)
            self.w.show()

    def add_point(self, point):
        popup = ""
        for key in point["properties"]:
            if point["properties"][key] != None:
                popup += str(key) + ": " + str(point["properties"][key]) + "<br>"
        folium.Marker(location=[point['geometry']['coordinates'][1], point['geometry']['coordinates'][0]], popup=popup).add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.w.setHtml(self.data.getvalue().decode())

    def add_polyline(self, polyline):
        popup = ""
        for key in polyline["properties"]:
            if polyline["properties"][key] != None:
                popup += str(key) + ": " + str(polyline["properties"][key]) + "<br>"
        for i in polyline['geometry']['coordinates']:
            i[0], i[1] = i[1], i[0]
        folium.PolyLine(polyline['geometry']['coordinates'], weight=6, color="blue", popup=popup).add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.w.setHtml(self.data.getvalue().decode())

    def map(self):
        self.m = folium.Map(
            location=[59.938551824389663, 30.345898845072504],
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            zoom_start=13,
            attr='MANILOC'
        )

        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.w = QtWebEngineWidgets.QWebEngineView(self)
        self.w.setHtml(self.data.getvalue().decode())
        self.w.resize(640, 480)
        self.w.move(130, 0)

    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Route")
        self.setGeometry(300, 250, 770, 480)

        self.map()

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(15, 15)
        self.btn.setText("Geometry")
        self.btn.clicked.connect(self.add_geometry)



def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()