import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QTabWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gráfica de A y B")
        self.setGeometry(100, 100, 800, 400)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal (horizontal)
        main_layout = QHBoxLayout(self.central_widget)

        # Crear QTabWidget para las pestaÃ±as
        self.tabs = QTabWidget()

        # Establecer el ancho y alto mínimo del QTabWidget
        self.tabs.setMinimumWidth(250)
        self.tabs.setMinimumHeight(150)

        # Crear la pestaÃ±a para los parÃ¡metros A
        self.tab_A = QWidget()
        self.tabs.addTab(self.tab_A, "Parámetros A")

        # Crear la pestaÃ±a para los parÃ¡metros B
        self.tab_B = QWidget()
        self.tabs.addTab(self.tab_B, "Parámetros B")

        # Layout de la pestaña A
        layout_A = QVBoxLayout()
        self.label_A = QLabel("Valor A:")
        self.input_A = QLineEdit(self)
        self.label_A1 = QLabel("Valor A1:")
        self.input_A1 = QLineEdit(self)
        self.label_A2 = QLabel("Valor A2:")
        self.input_A2 = QLineEdit(self)
        self.label_A3 = QLabel("Valor A3:")
        self.input_A3 = QLineEdit(self)

        layout_A.addWidget(self.label_A)
        layout_A.addWidget(self.input_A)
        layout_A.addWidget(self.label_A1)
        layout_A.addWidget(self.input_A1)
        layout_A.addWidget(self.label_A2)
        layout_A.addWidget(self.input_A2)
        layout_A.addWidget(self.label_A3)
        layout_A.addWidget(self.input_A3)
        self.tab_A.setLayout(layout_A)

        # Layout de la pestaña B
        layout_B = QVBoxLayout()
        self.label_B = QLabel("Valor B:")
        self.input_B = QLineEdit(self)
        self.label_B1 = QLabel("Valor B1:")
        self.input_B1 = QLineEdit(self)
        self.label_B2 = QLabel("Valor B2:")
        self.input_B2 = QLineEdit(self)

        layout_B.addWidget(self.label_B)
        layout_B.addWidget(self.input_B)
        layout_B.addWidget(self.label_B1)
        layout_B.addWidget(self.input_B1)
        layout_B.addWidget(self.label_B2)
        layout_B.addWidget(self.input_B2)
        self.tab_B.setLayout(layout_B)

        # AÃ±adir el TabWidget al layout principal
        main_layout.addWidget(self.tabs)

        # Widget para la gráfica en el lado derecho
        self.graph_widget = QWidget(self)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.graph_layout.addWidget(self.canvas)
        main_layout.addWidget(self.graph_widget)

        # Establecer un tamaÃ±o máximo para la gráfica
        self.graph_widget.setMinimumWidth(480)
        self.graph_widget.setMinimumHeight(400)

        # Conectar las señales de cambio en los campos de texto y pestaÃ±as
        self.tabs.currentChanged.connect(self.check_inputs)  # Cuando cambia la pestaÃ±a
        self.input_A.textChanged.connect(self.check_inputs)
        self.input_A1.textChanged.connect(self.check_inputs)
        self.input_A2.textChanged.connect(self.check_inputs)
        self.input_A3.textChanged.connect(self.check_inputs)
        self.input_B.textChanged.connect(self.check_inputs)
        self.input_B1.textChanged.connect(self.check_inputs)
        self.input_B2.textChanged.connect(self.check_inputs)

    def check_inputs(self):
        # Verificar la pestaÃ±a activa
        current_tab = self.tabs.currentIndex()

        # Si la pestaÃ±a activa es la primera, generar grÃ¡fica de A*x^3 - A1*x^2 + A2*x + A3
        if current_tab == 0:
            try:
                A = float(self.input_A.text())
                A1 = float(self.input_A1.text())
                A2 = float(self.input_A2.text())
                A3 = float(self.input_A3.text())
                self.plot_graph_A(A, A1, A2, A3)
            except ValueError:
                return

        # Si la pestaÃ±a activa es la segunda, generar grÃ¡fica de B/x + B1/x^2 + B2/x^3
        elif current_tab == 1:
            try:
                B = float(self.input_B.text())
                B1 = float(self.input_B1.text())
                B2 = float(self.input_B2.text())
                self.plot_graph_B(B, B1, B2)
            except ValueError:
                return

    def plot_graph_A(self, A, A1, A2, A3):
        # Limpiar la grÃ¡fica anterior
        self.figure.clear()

        # Crear el eje para la nueva grÃ¡fica
        ax = self.figure.add_subplot(111)

        # Generar la grÃ¡fica de A*x^3 - A1*x^2 + A2*x + A3
        x = np.linspace(-10, 10, 100)
        y = A * x**3 - A1 * x**2 + A2 * x + A3

        ax.plot(x, y, label=f"A*x^3 - A1*x^2 + A2*x + A3")
        ax.legend()
        ax.set_title(f"GrÃ¡fica de A*x^3 - A1*x^2 + A2*x + A3")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        # Dibujar la nueva grÃ¡fica
        self.canvas.draw()

    def plot_graph_B(self, B, B1, B2):
        # Limpiar la grÃ¡fica anterior
        self.figure.clear()

        # Crear el eje para la nueva grÃ¡fica
        ax = self.figure.add_subplot(111)

        # Generar la grÃ¡fica de B/x + B1/x^2 + B2/x^3
        x = np.linspace(1, 10, 100)  # Evitamos el 0 para no dividir por 0
        y = B / x + B1 / x**2 + B2 / x**3

        ax.plot(x, y, label=f"B/x + B1/x^2 + B2/x^3")
        ax.legend()
        ax.set_title(f"GrÃ¡fica de B/x + B1/x^2 + B2/x^3")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        # Dibujar la nueva grÃ¡fica
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
