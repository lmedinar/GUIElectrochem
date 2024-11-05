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
    QSplitter,
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from matplotlib.figure import Figure
import numpy as np

F = 96485
R = 8.31446261815324
T = 298


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gráfica de A y B con Pestañas")
        self.setGeometry(100, 100, 800, 400)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crear QTabWidget para las pestañas
        self.tabs = QTabWidget()

        # Establecer el ancho y alto mínimo del QTabWidget
        self.tabs.setMinimumWidth(550)
        self.tabs.setMinimumHeight(600)

        # Crear un QDoubleValidator para validar valores flotantes
        float_validator = QDoubleValidator()
        float_validator.setNotation(
            QDoubleValidator.StandardNotation
        )  # Formato estándar
        float_validator.setDecimals(12)  # Permitir hasta 3 decimales

        # Crear un QIntValidator para validar valores enteros
        int_validator = QIntValidator()

        # Crear la pestaña para los parámetros A
        self.tab_A = QWidget()
        self.tabs.addTab(self.tab_A, "Caso A")

        # Crear la pestaña para los parámetros B
        self.tab_B = QWidget()
        self.tabs.addTab(self.tab_B, "Caso B")

        # Crear la pestaña para los parámetros C
        self.tab_C = QWidget()
        self.tabs.addTab(self.tab_C, "Caso C")

        # Crear la pestaña para los parámetros D
        self.tab_D = QWidget()
        self.tabs.addTab(self.tab_D, "Caso D")

        # Crear la pestaña para los parámetros E
        self.tab_E = QWidget()
        self.tabs.addTab(self.tab_E, "Caso E")

        # Layout de la pestaña A
        layout_A = QVBoxLayout()
        self.label_DescA = QLabel(
            "Descripción:\n\nR está ausente, pero O está presente.\n"
        )
        self.label_An = QLabel("Electrones(n):")
        self.input_An = QLineEdit(self)
        self.input_An.setValidator(int_validator)
        self.input_An.setText("1")
        self.label_AArea = QLabel("Área (cm²):")
        self.input_AArea = QLineEdit(self)
        self.input_AArea.setValidator(float_validator)
        self.input_AArea.setText("1.0")
        self.label_Amo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Amo = QLineEdit(self)
        self.input_Amo.setValidator(float_validator)
        self.input_Amo.setText("0.5")
        self.label_Amr = QLabel("Coef. de transferencia de masa R:")
        self.input_Amr = QLineEdit(self)
        self.input_Amr.setValidator(float_validator)
        self.input_Amr.setText("0.3")
        # self.label_Acoxo = QLabel("Concentración O en x = 0:")
        # self.input_Acoxo = QLineEdit(self)
        # self.input_Acoxo.setValidator(float_validator)
        # self.input_Acoxo.setText("1.0")
        self.label_Aco = QLabel("Concentración O*:")
        self.input_Aco = QLineEdit(self)
        self.input_Aco.setValidator(float_validator)
        self.input_Aco.setText("1.0")
        # self.input_Aco.setDisabled(True)  # Desactivar
        # self.label_Acrxo = QLabel("Concentración R en x = 0:")
        # self.input_Acrxo = QLineEdit(self)
        # self.input_Acrxo.setValidator(float_validator)
        # self.input_Acrxo.setText("0.4")
        self.label_Acr = QLabel("Concentración R* (No aplica):")
        self.input_Acr = QLineEdit(self)
        self.input_Acr.setValidator(float_validator)
        self.input_Acr.setText("0.0")
        self.input_Acr.setDisabled(True)  # Desactiva
        self.label_AEo = QLabel("E°':")
        self.input_AEo = QLineEdit(self)
        self.input_AEo.setValidator(float_validator)
        self.input_AEo.setText("0.5")

        layout_A.addWidget(self.label_DescA)
        layout_A.addWidget(self.label_An)
        layout_A.addWidget(self.input_An)
        layout_A.addWidget(self.label_AArea)
        layout_A.addWidget(self.input_AArea)
        layout_A.addWidget(self.label_Amo)
        layout_A.addWidget(self.input_Amo)
        layout_A.addWidget(self.label_Amr)
        layout_A.addWidget(self.input_Amr)
        # layout_A.addWidget(self.label_Acoxo)
        # layout_A.addWidget(self.input_Acoxo)
        layout_A.addWidget(self.label_Aco)
        layout_A.addWidget(self.input_Aco)
        # layout_A.addWidget(self.label_Acrxo)
        # layout_A.addWidget(self.input_Acrxo)
        layout_A.addWidget(self.label_Acr)
        layout_A.addWidget(self.input_Acr)
        layout_A.addWidget(self.label_AEo)
        layout_A.addWidget(self.input_AEo)

        spacerA = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_A.addItem(spacerA)

        self.tab_A.setLayout(layout_A)

        # Layout de la pestaña B
        layout_B = QVBoxLayout()
        self.label_DescB = QLabel(
            "Descripción:\n\nO y R están presentes desde el inicio.\n"
        )
        self.label_Bn = QLabel("Electrones(n):")
        self.input_Bn = QLineEdit(self)
        self.input_Bn.setValidator(int_validator)
        self.input_Bn.setText("1")
        self.label_BArea = QLabel("Área (cm²):")
        self.input_BArea = QLineEdit(self)
        self.input_BArea.setValidator(float_validator)
        self.input_BArea.setText("1.0")
        self.label_Bmo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Bmo = QLineEdit(self)
        self.input_Bmo.setValidator(float_validator)
        self.input_Bmo.setText("0.5")
        self.label_Bmr = QLabel("Coef. de transferencia de masa R:")
        self.input_Bmr = QLineEdit(self)
        self.input_Bmr.setValidator(float_validator)
        self.input_Bmr.setText("0.3")
        # self.label_Bcoxo = QLabel("Concentración 0 en x = 0:")
        # self.input_Bcoxo = QLineEdit(self)
        # self.input_Bcoxo.setValidator(float_validator)
        # self.input_Bcoxo.setText("1.2")
        self.label_Bco = QLabel("Concentración O*:")
        self.input_Bco = QLineEdit(self)
        self.input_Bco.setValidator(float_validator)
        self.input_Bco.setText("0.3")
        # self.label_Bcrxo = QLabel("Concentración R en x = 0:")
        # self.input_Bcrxo = QLineEdit(self)
        # self.input_Bcrxo.setValidator(float_validator)
        # self.input_Bcrxo.setText("1.0")
        self.label_Bcr = QLabel("Concentración R*:")
        self.input_Bcr = QLineEdit(self)
        self.input_Bcr.setValidator(float_validator)
        self.input_Bcr.setText("0.2")
        self.label_BEo = QLabel("E°':")
        self.input_BEo = QLineEdit(self)
        self.input_BEo.setValidator(float_validator)
        self.input_BEo.setText("-0.3")

        layout_B.addWidget(self.label_DescB)
        layout_B.addWidget(self.label_Bn)
        layout_B.addWidget(self.input_Bn)
        layout_B.addWidget(self.label_BArea)
        layout_B.addWidget(self.input_BArea)
        layout_B.addWidget(self.label_Bmo)
        layout_B.addWidget(self.input_Bmo)
        layout_B.addWidget(self.label_Bmr)
        layout_B.addWidget(self.input_Bmr)
        # layout_B.addWidget(self.label_Bcoxo)
        # layout_B.addWidget(self.input_Bcoxo)
        layout_B.addWidget(self.label_Bco)
        layout_B.addWidget(self.input_Bco)
        # layout_B.addWidget(self.label_Bcrxo)
        # layout_B.addWidget(self.input_Bcrxo)
        layout_B.addWidget(self.label_Bcr)
        layout_B.addWidget(self.input_Bcr)
        layout_B.addWidget(self.label_BEo)
        layout_B.addWidget(self.input_BEo)

        spacerB = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_B.addItem(spacerB)

        self.tab_B.setLayout(layout_B)

        # Layout de la pestaña C
        layout_C = QVBoxLayout()
        self.label_DescC = QLabel(
            "Descripción:\n\nR está presente, pero está O ausente.\n"
        )
        self.label_Cn = QLabel("Electrones(n):")
        self.input_Cn = QLineEdit(self)
        self.input_Cn.setValidator(int_validator)
        self.input_Cn.setText("1")
        self.label_CArea = QLabel("Área (cm²):")
        self.input_CArea = QLineEdit(self)
        self.input_CArea.setValidator(float_validator)
        self.input_CArea.setText("1.0")
        self.label_Cmo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Cmo = QLineEdit(self)
        self.input_Cmo.setValidator(float_validator)
        self.input_Cmo.setText("0.5")
        self.label_Cmr = QLabel("Coef. de transferencia de masa R:")
        self.input_Cmr = QLineEdit(self)
        self.input_Cmr.setValidator(float_validator)
        self.input_Cmr.setText("0.3")
        self.label_Cco = QLabel("Concentración O* (no aplica):")
        self.input_Cco = QLineEdit(self)
        self.input_Cco.setValidator(float_validator)
        self.input_Cco.setText("0")
        self.input_Cco.setDisabled(True)  # Desactiva
        self.label_Ccr = QLabel("Concentración R*:")
        self.input_Ccr = QLineEdit(self)
        self.input_Ccr.setValidator(float_validator)
        self.input_Ccr.setText("0.9")
        self.label_CEo = QLabel("E°':")
        self.input_CEo = QLineEdit(self)
        self.input_CEo.setValidator(float_validator)
        self.input_CEo.setText("0.2")

        layout_C.addWidget(self.label_DescC)
        layout_C.addWidget(self.label_Cn)
        layout_C.addWidget(self.input_Cn)
        layout_C.addWidget(self.label_CArea)
        layout_C.addWidget(self.input_CArea)
        layout_C.addWidget(self.label_Cmo)
        layout_C.addWidget(self.input_Cmo)
        layout_C.addWidget(self.label_Cmr)
        layout_C.addWidget(self.input_Cmr)
        layout_C.addWidget(self.label_Cco)
        layout_C.addWidget(self.input_Cco)
        layout_C.addWidget(self.label_Ccr)
        layout_C.addWidget(self.input_Ccr)
        layout_C.addWidget(self.label_CEo)
        layout_C.addWidget(self.input_CEo)

        spacerC = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_C.addItem(spacerC)

        self.tab_C.setLayout(layout_C)

        # Crear el widget para la gráfica
        self.graph_widget = QWidget(self)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph_layout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canvas)

        # Crear el splitter para dividir los widgets
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tabs)  # Añadir las pestañas
        splitter.addWidget(self.graph_widget)  # Añadir la gráfica

        # Establecer el ratio 2:3
        splitter.setStretchFactor(0, 3)  # La primera parte (tabs) ocupa 2 partes
        splitter.setStretchFactor(1, 2)  # La segunda parte (gráfica) ocupa 3 partes

        # Añadir el splitter al layout principal
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(splitter)

        # Conectar las señales de cambio en los campos de texto y pestañas
        self.tabs.currentChanged.connect(self.check_inputs)  # Cuando cambia la pestaña

        self.input_An.textChanged.connect(self.check_inputs)
        self.input_AArea.textChanged.connect(self.check_inputs)
        self.input_Amo.textChanged.connect(self.check_inputs)
        self.input_Amr.textChanged.connect(self.check_inputs)
        # self.input_Acoxo.textChanged.connect(self.check_inputs)
        self.input_Aco.textChanged.connect(self.check_inputs)
        # self.input_Acrxo.textChanged.connect(self.check_inputs)
        self.input_Acr.textChanged.connect(self.check_inputs)
        self.input_AEo.textChanged.connect(self.check_inputs)

        self.input_Bn.textChanged.connect(self.check_inputs)
        self.input_BArea.textChanged.connect(self.check_inputs)
        self.input_Bmo.textChanged.connect(self.check_inputs)
        self.input_Bmr.textChanged.connect(self.check_inputs)
        # self.input_Bcoxo.textChanged.connect(self.check_inputs)
        self.input_Bco.textChanged.connect(self.check_inputs)
        # self.input_Bcrxo.textChanged.connect(self.check_inputs)
        self.input_Bcr.textChanged.connect(self.check_inputs)
        self.input_BEo.textChanged.connect(self.check_inputs)

        self.input_Cn.textChanged.connect(self.check_inputs)
        self.input_CArea.textChanged.connect(self.check_inputs)
        self.input_Cmo.textChanged.connect(self.check_inputs)
        self.input_Cmr.textChanged.connect(self.check_inputs)
        self.input_Cco.textChanged.connect(self.check_inputs)
        self.input_Ccr.textChanged.connect(self.check_inputs)
        self.input_CEo.textChanged.connect(self.check_inputs)

    def check_inputs(self):
        # Verificar la pestaña activa
        current_tab = self.tabs.currentIndex()

        # Si la pestaña activa es la primera, generar gráfica
        if current_tab == 0:
            try:
                An = float(self.input_An.text())
                AArea = float(self.input_AArea.text())
                Amo = float(self.input_Amo.text())
                Amr = float(self.input_Amr.text())
                # Acoxo = float(self.input_Acoxo.text())
                Aco = float(self.input_Aco.text())
                # Acrxo = float(self.input_Acrxo.text())
                Acr = float(self.input_Acr.text())
                AEo = float(self.input_AEo.text())
                print("Variables A correctas")
                self.plot_graph_A(An, AArea, Amo, Amr, Aco, Acr, AEo)
            except ValueError:
                print("Error de valor")
                return

        # Si la pestaña activa es la segunda, generar gráfica
        elif current_tab == 1:
            try:
                Bn = float(self.input_Bn.text())
                BArea = float(self.input_BArea.text())
                Bmo = float(self.input_Bmo.text())
                Bmr = float(self.input_Bmr.text())
                # Bcoxo = float(self.input_Bcoxo.text())
                Bco = float(self.input_Bco.text())
                # Bcrxo = float(self.input_Bcrxo.text())
                Bcr = float(self.input_Bcr.text())
                BEo = float(self.input_BEo.text())
                print("Variables B correctas")
                self.plot_graph_B(Bn, BArea, Bmo, Bmr, Bco, Bcr, BEo)
            except ValueError:
                print("Error de valor")
                return

        # Si la pestaña activa es la tercera, generar gráfica
        elif current_tab == 2:
            try:
                Cn = float(self.input_Cn.text())
                CArea = float(self.input_CArea.text())
                Cmo = float(self.input_Cmo.text())
                Cmr = float(self.input_Cmr.text())
                Cco = float(self.input_Cco.text())
                Ccr = float(self.input_Ccr.text())
                CEo = float(self.input_CEo.text())
                print("Variables C correctas")
                self.plot_graph_C(Cn, CArea, Cmo, Cmr, Cco, Ccr, CEo)
            except ValueError:
                print("Error de valor")
                return

    def plot_graph_A(self, An, AArea, Amo, Amr, Aco, Acr, AEo):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LC = Amo * An * F * AArea * 0.0001 * Aco
        try:
            E_central = AEo - R * T * np.log(Amo / Amr) / An / F
            exponencial = (Amr / Amo) * np.exp((An * F) * (AEo - E) / (R * T))
            I = I_LC * exponencial / (1 + exponencial)
        except:
            print("Ignorando división por cero")
            return
        # print("I:", I)
        print("I_LC:", I_LC)
        print("E_central:", E_central)

        recta_ilcx = np.array([np.min(E), np.max(E)])
        recta_ilcy = np.array([0, 0])
        recta_ilax = np.array([np.min(E), np.max(E)])
        recta_ilay = np.array([I_LC, I_LC])
        Vx = np.array([E_central, E_central])
        Vy = np.array([np.min(I), np.max(I)])
        ax.plot(
            Vx,
            Vy,
            linestyle="--",
            linewidth=2,
            color="#F72226",
            label=f"$E_½$ = {E_central:.6f} V",
        )
        ax.plot(
            recta_ilax,
            recta_ilay,
            linestyle="--",
            linewidth=2,
            color="#6364FC",
            label="$I_{LC}$" + f" = {I_LC:.6f} mA",
        )
        ax.plot(
            recta_ilcx,
            recta_ilcy,
            linestyle="--",
            linewidth=2,
            color="#861491",
            label=f"0 A",
        )
        ax.set_xticks(np.linspace(-2, 2, 11))  # divisions on the x-axis
        ax.plot(E, I, linewidth=3, color="#101030")
        ax.grid(True)
        ax.legend()
        ax.set_title(f"Corriente contra Potencial")
        ax.set_xlabel("E (V)")
        ax.set_ylabel("I (mA)")

        # Dibujar la nueva gráfica
        self.canvas.draw()

    def plot_graph_B(self, Bn, BArea, Bmo, Bmr, Bco, Bcr, BEo):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LC = Bmo * Bn * F * BArea * 0.0001 * Bco
        I_LA = -Bmr * Bn * F * BArea * 0.0001 * Bcr
        try:
            E_central = BEo - R * T * np.log(Bmo / Bmr) / Bn / F
            exponencial = (Bmr / Bmo) * np.exp((Bn * F) * (BEo - E) / (R * T))
            I = (I_LC * exponencial + I_LA) / (1 + exponencial)
        except:
            print("Ignorando división por cero")
            return
        # print("I:", I)
        print("I_LC:", I_LC)
        print("I_LA:", -I_LA)
        print("E_central:", E_central)

        recta_ilcx = np.array([np.min(E), np.max(E)])
        recta_ilcy = np.array([I_LA, I_LA])
        recta_ilax = np.array([np.min(E), np.max(E)])
        recta_ilay = np.array([I_LC, I_LC])
        Vx = np.array([E_central, E_central])
        Vy = np.array([np.min(I), np.max(I)])
        ax.plot(
            Vx,
            Vy,
            linestyle="--",
            linewidth=2,
            color="#F72226",
            label=f"$E_½$ = {E_central:.6f} V",
        )
        ax.plot(
            recta_ilax,
            recta_ilay,
            linestyle="--",
            linewidth=2,
            color="#6364FC",
            label="$I_{LC}$" + f" = {I_LC:.6f} mA",
        )
        # print(E)
        # print(I)
        ax.plot(
            recta_ilcx,
            np.array([0, 0]),
            linestyle="--",
            linewidth=2,
            color="#861491",
            label=f"0 A",
        )
        ax.plot(
            recta_ilcx,
            recta_ilcy,
            linestyle="--",
            linewidth=2,
            color="#168491",
            label="$I_{LA}$" + f" = {I_LA:.6f} mA",
        )
        ax.set_xticks(np.linspace(-2, 2, 11))  # divisions on the x-axis
        ax.plot(E, I, linewidth=3, color="#101030")
        ax.grid(True)
        ax.legend()
        ax.set_title(f"Corriente contra Potencial")
        ax.set_xlabel("E (V)")
        ax.set_ylabel("I (mA)")

        # Dibujar gŕafica
        self.canvas.draw()

    def plot_graph_C(self, Cn, CArea, Cmo, Cmr, Cco, Ccr, CEo):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LA = -Cmr * Cn * F * CArea * 0.0001 * Ccr
        try:
            E_central = CEo - R * T * np.log(Cmo / Cmr) / Cn / F
            exponencial = (Cmr / Cmo) * np.exp((Cn * F) * (CEo - E) / (R * T))
            I = I_LA / (1 + exponencial)
        except:
            print("Ignorando división por cero")
            return
        print("I_LA:", I_LA)
        print("E_central:", E_central)

        recta_ilcx = np.array([np.min(E), np.max(E)])
        recta_ilcy = np.array([I_LA, I_LA])
        Vx = np.array([E_central, E_central])
        Vy = np.array([np.min(I), np.max(I)])
        ax.plot(
            Vx,
            Vy,
            linestyle="--",
            linewidth=2,
            color="#F72226",
            label=f"$E_½$ = {E_central:.6f} V",
        )
        ax.plot(
            recta_ilcx,
            np.array([0, 0]),
            linestyle="--",
            linewidth=2,
            color="#861491",
            label=f"0 A",
        )
        ax.plot(
            recta_ilcx,
            recta_ilcy,
            linestyle="--",
            linewidth=2,
            color="#168491",
            label="$I_{LA}$" + f" = {I_LA:.6f} mA",
        )
        ax.set_xticks(np.linspace(-2, 2, 11))  # divisions on the x-axis
        ax.plot(E, I, linewidth=3, color="#101030")
        ax.grid(True)
        ax.legend()
        ax.set_title(f"Corriente contra Potencial")
        ax.set_xlabel("E (V)")
        ax.set_ylabel("I (mA)")

        print("completadooooooooooo")
        # Dibujar gŕafica
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    window.check_inputs()
    sys.exit(app.exec_())
