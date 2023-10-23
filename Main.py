########################################################
# Author:     Filip Segota
# Course:     Advance CS topics (CSC 310, Spring 2021)
# Assignment: Italy & Covid reporting Assignment in 2020
########################################################

import sys
from regions import *
import folium
import io
from Data import *
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QMessageBox,
    QDialog,
)
from PyQt5.QtGui import QFont
import PyQt5.QtCore as qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from googletrans import Translator


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Italy Covid Report 2021")
        self.setFixedSize(600, 600)
        self.data = Data()
        self.regions = self.data.get_region()
        self.content()
        self.show()

    def content(self):
        select_region_h_box1 = QHBoxLayout()
        select_region_h_box1.addSpacing(10)
        self.select_region_label = QLabel("Select Region", self)
        select_region_h_box1.addWidget(self.select_region_label)
        self.select_region_combo = QComboBox(self)
        self.select_region_combo.addItems(self.regions)
        select_region_h_box1.addWidget(self.select_region_combo)
        self.select_region_botton = QPushButton("Check Region", self)
        self.select_region_botton.pressed.connect(self.italyRegionClicked)
        select_region_h_box1.addWidget(self.select_region_botton)

        select_region_main_v_box = QVBoxLayout()

        self.italy_lbl = QLabel("Italy Region Covid Report", self)
        self.italy_lbl.setStyleSheet("border: 0.5px solid gray")
        select_region_main_v_box.addWidget(self.italy_lbl)
        select_region_main_v_box.addLayout(select_region_h_box1)
        select_region_main_v_box.setSpacing(15)
        select_region_main_v_box.addStretch()

        language_h_box = QHBoxLayout()
        self.language_lbl = QLabel("Select Language", self)
        self.language_combobox = QComboBox()
        options = [
            ("English", "en"),
            ("Italian", "it"),
            ("Spanish", "es"),
            ("Chinese", "zh-CN"),
        ]
        for i, (text, lang) in enumerate(options):
            self.language_combobox.addItem(text)
            self.language_combobox.setItemData(i, lang)

        language_h_box.addWidget(self.language_lbl)
        self.language_combobox.currentIndexChanged.connect(self.languageChanged)

        language_h_box.addWidget(self.language_combobox)
        language_h_box.addStretch()
        select_region_main_v_box.addLayout(language_h_box)

        region_map_box = QVBoxLayout()

        self.coordinate_title = "This is a title"
        self.coordinate = coordinate["Campania"]

        m = folium.Map(tiles="Stamen Terrain", zoom_start=6, location=self.coordinate)

        def foliumHtml(lo):
            if lo != "Italy":
                stats = self.data.getRegionStats(str(lo))
                return f"""
                 <h1 style='color:#7b113a;'> {lo} </h1>
                 <hr/>
                 <p style='color:#7b113a;font-size:20px;'>Region Population: {stats['region_population']}</p>
                 <p style='color:#7b113a;font-size:20px;'>Total Covid Case: {stats['case_number']}</p>
                 <p style='color:#7b113a;font-size:20px;'>Daily Cases: {stats['expectedChanges']}</p>
                 <p style='color:#7b113a;font-size:20px;'>Percentage: {stats['percentage']}%</p>
                 """
            else:
                return f"""
                 <h1> {lo}</h1>
                 <p>European country with a long Mediterranean coastline, has left a powerful mark on Western culture and cuisine.</p>
                 """

        for lo in coordinate:
            html = foliumHtml(lo)
            iframe = folium.IFrame(html=html, width=300, height=250)
            popUp = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location=coordinate[lo],
                popup=popUp,
                icon=folium.DivIcon(
                    html=f"""
                     <div><svg>
                         <circle cx="50" cy="50" r="40" fill="#7b113a" opacity=".4"/>
                         <rect x="35", y="35" width="30" height="30", fill="#fff600", opacity=".3" 
                     </svg></div>"""
                ),
            ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        region_map_box.addWidget(webView)

        h_box = QVBoxLayout()
        h_box.addLayout(select_region_main_v_box)
        h_box.addLayout(region_map_box)
        self.setLayout(h_box)

    def languageChanged(self, index):
        data = self.language_combobox.itemData(index)

        translator = Translator()
        self.language_lbl.setText(
            translator.translate("Select Language", dest=data).text
        )
        self.italy_lbl.setText(
            translator.translate("Italy Region Covid Report", dest=data).text
        )
        self.select_region_label.setText(
            translator.translate("Select Region", dest=data).text
        )
        self.select_region_botton.setText(
            translator.translate("Check Region", dest=data).text
        )

    def italyRegionClicked(self):
        stats = self.data.getRegionStats(self.select_region_combo.currentText())
        self.italyRegionStatistics(stats)

    def italyRegionStatistics(self, stats):
        regionDialog = QDialog(self)
        regionDialog.setFixedSize(390, 230)
        regionDialog.setWindowTitle(f"{stats['region']} Report".capitalize())

        d_title = QLabel(f"{stats['region']}", self)
        d_title.setFont(QFont("Times", 25, QFont.Light))
        d_title.setAlignment(qt.Qt.AlignCenter)

        r1_box = QHBoxLayout()
        r1_box.addStretch()
        region_label = QLabel("Region :", self)
        region_label.setFont(QFont("Times", 25, QFont.Light))
        region_text = QLabel(f"{stats['region']}", self)
        region_text.setFont(QFont("Times", 25, QFont.Light))
        r1_box.addWidget(region_label)
        r1_box.addWidget(region_text)
        r1_box.addStretch()

        r2_box = QHBoxLayout()
        r2_box.addStretch()
        population_label = QLabel("Population :", self)
        population_label.setFont(QFont("Times", 25, QFont.Light))
        population_text = QLabel(f"{stats['population']}", self)
        population_text.setFont(QFont("Times", 25, QFont.Light))
        r2_box.addWidget(population_label)
        r2_box.addWidget(population_text)
        r2_box.addStretch()

        r3_box = QHBoxLayout()
        r3_box.addStretch()
        region_population_label = QLabel("Region Population :", self)
        region_population_label.setFont(QFont("Times", 25, QFont.Light))
        region_population_text = QLabel(f"{stats['region_population']}", self)
        region_population_text.setFont(QFont("Times", 25, QFont.Light))
        r3_box.addWidget(region_population_label)
        r3_box.addWidget(region_population_text)
        r3_box.addStretch()

        r4_box = QHBoxLayout()
        r4_box.addStretch()
        case_number_label = QLabel("Total Covid Case :", self)
        case_number_label.setFont(QFont("Times", 25, QFont.Light))
        case_number_text = QLabel(f"{stats['case_number']}", self)
        case_number_text.setFont(QFont("Times", 25, QFont.Light))
        r4_box.addWidget(case_number_label)
        r4_box.addWidget(case_number_text)
        r4_box.addStretch()

        r5_box = QHBoxLayout()
        r5_box.addStretch()
        expected_changes_label = QLabel("Daily Cases  :", self)
        expected_changes_label.setFont(QFont("Times", 25, QFont.Light))
        expected_changes_text = QLabel(f"{stats['expectedChanges']}", self)
        expected_changes_text.setFont(QFont("Times", 25, QFont.Light))
        r5_box.addWidget(expected_changes_label)
        r5_box.addWidget(expected_changes_text)
        r5_box.addStretch()

        r6_box = QHBoxLayout()
        r6_box.addStretch()
        cal_percentage_label = QLabel("Percentage :", self)
        cal_percentage_label.setFont(QFont("Times", 25, QFont.Light))
        cal_percentage_text = QLabel(f"{stats['percentage']}%", self)
        cal_percentage_text.setFont(QFont("Times", 25, QFont.Light))
        r6_box.addWidget(cal_percentage_label)
        r6_box.addWidget(cal_percentage_text)
        r6_box.addStretch()

        main_v_box = QVBoxLayout()
        main_v_box.setSpacing(10)
        main_v_box.addLayout(r1_box)
        main_v_box.addLayout(r2_box)
        main_v_box.addLayout(r3_box)
        main_v_box.addLayout(r4_box)
        main_v_box.addLayout(r5_box)
        main_v_box.addLayout(r6_box)
        main_v_box.addStretch()

        regionDialog.setLayout(main_v_box)
        regionDialog.exec_()


app = QApplication(sys.argv)
app.setStyleSheet(
    """
        QWidget {
            font-size: 20px;
            font-family:Times;
        }
    """
)
mw = Main()
sys.exit(app.exec_())
