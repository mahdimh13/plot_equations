from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
import sympy as sp
import numpy as np
import sys


class EquationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Equation Input')
        self.setGeometry(100, 100, 400, 200)

        self.equation_label = QLabel('Enter the equation:', self)
        self.equation_label.setGeometry(50, 50, 100, 30)

        self.equation_input = QLineEdit(self)
        self.equation_input.setGeometry(160, 50, 200, 30)

        self.plot_button = QPushButton('Plot', self)
        self.plot_button.setGeometry(160, 100, 80, 30)
        self.plot_button.clicked.connect(self.plot_equation)

        self.save_button = QPushButton('Save', self)
        self.save_button.setGeometry(260, 100, 80, 30)
        self.save_button.clicked.connect(self.save_plot)

        self.error_label = QLabel(self)
        self.error_label.setGeometry(10, 160, 380, 30)
        self.error_label.setStyleSheet("color: red")

        layout = QVBoxLayout()
        layout.addWidget(self.equation_label)
        layout.addWidget(self.equation_input)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.error_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot_equation(self):
        self.error_label.setText("")
        self.equation = self.equation_input.text()
        self.plott()

    def save_plot(self):
        self.plott()
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save Plot', '', 'PNG (*.png);;JPEG (*.jpg *.jpeg)')
        if file_path:
            self.figure.savefig(file_path)

    def plott(self):
        x, y = sp.symbols('x y')

        try:
            equation = sp.sympify(self.equation)

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            if y in equation.free_symbols:
                eq_lambda = sp.lambdify((x, y), equation)

                x_vals = np.linspace(-50, 50, 100)
                y_vals = np.linspace(-50, 50, 100)

                X, Y = np.meshgrid(x_vals, y_vals)

                Z = eq_lambda(X, Y)

                levels = [0]
                contour = ax.contour(X, Y, Z, levels=levels)
                if contour.allkinds[0][0] is None:
                    raise ValueError("No valid plot found for the equation.")
            else:
                eq_lambda = sp.lambdify(x, equation)

                x_vals = np.linspace(-50, 50, 100)

                y_vals = eq_lambda(x_vals)

                ax.plot(x_vals, y_vals)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_title('Equation Plot')

            ax.grid(True)
            self.canvas.draw()

        except (sp.SympifyError, ValueError) as e:
            self.error_label.setText("Error: " + str(e))
        except sp.SympifyError:
            self.error_label.setText("Invalid equation. Please enter a valid equation.")


app = QApplication(sys.argv)
window = EquationWindow()
window.show()
sys.exit(app.exec_())
