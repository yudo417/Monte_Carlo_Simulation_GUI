import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPointF
import time

class ArrowGridWidget(QWidget):
    def __init__(self, rows=5, cols=5):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.counter_num = 0
        self.angles = np.random.rand(self.rows, self.cols) * 360
        self.angles = self.angles.astype(int)
        
    def set_counter_num(self, num):
        self.counter_num = num

    def is_equal_angle(self):
        is_equal = True
        check_angle = self.angles[0, 0]
        for i in range(self.rows):
            for j in range(self.cols):
                if np.abs(check_angle - self.angles[i,j]) > 10:
                    is_equal = False
        return is_equal
    
    def inner_sum(self,temp_i,temp_j,temp_angle,isnew = False):
        sum = 0
        if (temp_i == 0 and temp_j == 0):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[0,1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[1,0])))
        elif (temp_i == 0 and temp_j == 4):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[0,3]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[1,4])))
        elif (temp_i == 4 and temp_j == 0):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[3,0]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[4,1])))
        elif (temp_i == 4 and temp_j == 4):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[3,4]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[4,3])))
        elif (temp_j == 0):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i-1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i+1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j+1])))
        elif (temp_j == 4):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i-1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i+1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j-1])))
        elif (temp_i == 0):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j-1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j+1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i+1,temp_j])))
        elif (temp_i == 4):
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j-1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j+1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i-1,temp_j])))
        else:
            sum = np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i-1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i+1,temp_j]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j-1]))) + np.cos(np.radians(np.abs((temp_angle if isnew else self.angles[temp_i,temp_j]) - self.angles[temp_i,temp_j+1])))
        return sum
    
    def randomize(self): #再実行
        self.counter_num = 0
        self.angles = np.random.rand(self.rows, self.cols) * 360
        max_iterations = 1000000  
        iteration_count = 0
        
        while(not self.is_equal_angle() and iteration_count < max_iterations):
            temp_i,temp_j = np.random.randint(0,5),np.random.randint(0,5)
            temp_angle = np.random.rand() * 360
            temp_angle = int(temp_angle)
            if self.inner_sum(temp_i,temp_j,temp_angle,isnew=True) > self.inner_sum(temp_i,temp_j,temp_angle):
                self.angles[temp_i,temp_j] = temp_angle
            self.counter_num += 1
            iteration_count += 1
            

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cell_w, cell_h = w / self.cols, h / self.rows
        arrow_len = min(cell_w, cell_h) * 0.4
        arrow_size = 8

        grid_pen = QPen(Qt.gray, 1)
        painter.setPen(grid_pen)
        
        for j in range(self.cols + 1):
            x = j * cell_w
            painter.drawLine(int(x), 0, int(x), int(h))
        
        for i in range(self.rows + 1):
            y = i * cell_h
            painter.drawLine(0, int(y), int(w), int(y))

        arrow_pen = QPen(Qt.blue, 3)
        painter.setPen(arrow_pen)
        painter.setBrush(QBrush(Qt.black))

        for i in range(self.rows):
            for j in range(self.cols):
                angle = self.angles[i, j]
                cx = j * cell_w + cell_w / 2
                cy = i * cell_h + cell_h / 2
                dx = np.cos(np.radians(angle)) * arrow_len
                dy = -np.sin(np.radians(angle)) * arrow_len 

                painter.drawLine(int(cx), int(cy), int(cx + dx), int(cy + dy))

                for delta in (-0.3, +0.3):
                    phi = angle + 180 + np.degrees(delta)
                    x = cx + dx + np.cos(np.radians(phi)) * arrow_size
                    y = cy + dy - np.sin(np.radians(phi)) * arrow_size
                    if delta == -0.3:
                        p1 = QPointF(x, y)
                    else:
                        p2 = QPointF(x, y)
                painter.drawPolygon(QPointF(int(cx+dx), int(cy+dy)), p1, p2)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("モンテカルロ・シミュレーションGUI")
        self.resize(600, 500)

        h_layout = QHBoxLayout(self)

        self.grid = ArrowGridWidget(rows=5, cols=5)
        h_layout.addWidget(self.grid, stretch=1)

        vbox = QVBoxLayout()
        
        self.count_num = 0
        self.count_label = QLabel(f"実行回数: {self.count_num}")
        self.grid.set_counter_num(self.count_num)
        
        # ボタン押して再実行
        def update_counter():
            self.grid.randomize()
            self.count_label.setText(f"実行回数: {self.grid.counter_num}")
        
        btn = QPushButton("ランダムに再配置")
        btn.clicked.connect(update_counter)
        
        vbox.addWidget(self.count_label)
        vbox.addWidget(btn)
        h_layout.addLayout(vbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
