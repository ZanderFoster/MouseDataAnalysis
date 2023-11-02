import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from pynput.mouse import Listener
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MouseMovementRecorder(QWidget):
    def __init__(self, line_color='green'):
        super().__init__()

        self.figure = Figure()
        self.figure = Figure(facecolor='#444444') 
        self.figure.set_tight_layout(True)  # Use tight layout to maximize space
        
        self.ax = self.figure.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)  # Hide x-axis scale
        self.ax.get_yaxis().set_visible(False)  # Hide y-axis scale
        self.ax.set_frame_on(False)  # Turn off the frame around the graph

        self.line, = self.ax.plot([], [], lw=1, color=line_color)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        layout = QVBoxLayout()

        layout.addWidget(self.canvas, stretch=1)  # stretch=1 allows the graph to expand vertically

        self.setLayout(layout)

        self.x_data, self.y_data = [], []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(10)  # Update the chart every 50 milliseconds

        self.mouse_listener = Listener(on_move=self.on_mouse_move)
        self.mouse_listener.start()

        # Set the background color of the graph
        self.ax.set_facecolor("#555555")

    def on_mouse_move(self, x, y):
        # Calculate relative coordinates based on the current canvas size
        canvas_width = self.canvas.width()
        canvas_height = self.canvas.height()
        x_relative = x / canvas_width
        y_relative = 1 - y / canvas_height  # Invert the y-coordinate
        self.x_data.append(x_relative)
        self.y_data.append(y_relative)

    def update_chart(self):
        # Check the size of the x_data list
        data_length = len(self.x_data)
        if data_length > 1000:
            # If there are more than 1000 data points, remove the oldest ones
            self.x_data = self.x_data[data_length - 1000:]
            self.y_data = self.y_data[data_length - 1000:]

        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = MouseMovementRecorder()
    window.setCentralWidget(central_widget)
    window.setWindowTitle("Mouse Movement Recorder")
    window.setStyleSheet("background-color: #444444;")
    window.show()
    sys.exit(app.exec_())
