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
from PyQt5.QtCore import Qt, QSettings
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QIcon
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from matplotlib.figure import Figure
import numpy as np

F = 96485
R = 8.31446261815324
T = 298


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("bubbles.ico"))

        # Preferencia persistente de idioma
        self.settings = QSettings("Lmedinar", "ElectrochemGrapher")
        self.lang = self.settings.value("lang", "es")  # 'es' por defecto

        self.setWindowTitle("Gráficadora de reacciones electroquímicas")
        self.setGeometry(100, 100, 800, 400)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crear QTabWidget para las pestañas
        self.tabs = QTabWidget()

        # Establecer el ancho y alto mínimo del QTabWidget
        self.tabs.setMinimumWidth(550)
        self.tabs.setMinimumHeight(750)

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

        # Crear la pestaña para los parámetros F
        self.tab_F = QWidget()
        self.tabs.addTab(self.tab_F, "Caso F")

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

        # Layout de la pestaña D
        layout_D = QVBoxLayout()
        self.label_DescD = QLabel("Descripción:\n\nR es insoluble.\n")
        self.label_Dn = QLabel("Electrones(n):")
        self.input_Dn = QLineEdit(self)
        self.input_Dn.setValidator(int_validator)
        self.input_Dn.setText("1")
        self.label_DArea = QLabel("Área (cm²):")
        self.input_DArea = QLineEdit(self)
        self.input_DArea.setValidator(float_validator)
        self.input_DArea.setText("1.0")
        self.label_Dmo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Dmo = QLineEdit(self)
        self.input_Dmo.setValidator(float_validator)
        self.input_Dmo.setText("0.5")
        self.label_Dmr = QLabel("Coef. de transferencia de masa R (no aplica):")
        self.input_Dmr = QLineEdit(self)
        self.input_Dmr.setValidator(float_validator)
        self.input_Dmr.setText("0")
        self.input_Dmr.setDisabled(True)  # Desactiva
        self.label_Dco = QLabel("Concentración O* (no aplica):")
        self.input_Dco = QLineEdit(self)
        self.input_Dco.setValidator(float_validator)
        self.input_Dco.setText("0.6")
        self.label_Dcr = QLabel("Concentración R* (no aplica):")
        self.input_Dcr = QLineEdit(self)
        self.input_Dcr.setValidator(float_validator)
        self.input_Dcr.setText("0")
        self.input_Dcr.setDisabled(True)
        self.label_DEo = QLabel("E°':")
        self.input_DEo = QLineEdit(self)
        self.input_DEo.setValidator(float_validator)
        self.input_DEo.setText("0.2")

        layout_D.addWidget(self.label_DescD)
        layout_D.addWidget(self.label_Dn)
        layout_D.addWidget(self.input_Dn)
        layout_D.addWidget(self.label_DArea)
        layout_D.addWidget(self.input_DArea)
        layout_D.addWidget(self.label_Dmo)
        layout_D.addWidget(self.input_Dmo)
        layout_D.addWidget(self.label_Dmr)
        layout_D.addWidget(self.input_Dmr)
        layout_D.addWidget(self.label_Dco)
        layout_D.addWidget(self.input_Dco)
        layout_D.addWidget(self.label_Dcr)
        layout_D.addWidget(self.input_Dcr)
        layout_D.addWidget(self.label_DEo)
        layout_D.addWidget(self.input_DEo)

        spacerD = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_D.addItem(spacerD)

        self.tab_D.setLayout(layout_D)

        # Layout de la pestaña E
        layout_E = QVBoxLayout()
        self.label_DescE = QLabel(
            "Descripción:\n\nHay un agente acomplejante (Y) que afecta a la especie O (reacciones reversibles).\n"
        )
        self.label_En = QLabel("Electrones(n):")
        self.input_En = QLineEdit(self)
        self.input_En.setValidator(int_validator)
        self.input_En.setText("1")
        self.label_EArea = QLabel("Área (cm²):")
        self.input_EArea = QLineEdit(self)
        self.input_EArea.setValidator(float_validator)
        self.input_EArea.setText("1.0")
        self.label_Emo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Emo = QLineEdit(self)
        self.input_Emo.setValidator(float_validator)
        self.input_Emo.setText("0.5")
        self.label_Emr = QLabel("Coef. de transferencia de masa R:")
        self.input_Emr = QLineEdit(self)
        self.input_Emr.setValidator(float_validator)
        self.input_Emr.setText("0.3")
        self.label_Eco = QLabel("Concentración O*:")
        self.input_Eco = QLineEdit(self)
        self.input_Eco.setValidator(float_validator)
        self.input_Eco.setText("1.0")
        self.label_Ecr = QLabel("Concentración R* (no aplica):")
        self.input_Ecr = QLineEdit(self)
        self.input_Ecr.setValidator(float_validator)
        self.input_Ecr.setText("0")
        self.input_Ecr.setDisabled(True)
        self.label_EEo = QLabel("E°':")
        self.input_EEo = QLineEdit(self)
        self.input_EEo.setValidator(float_validator)
        self.input_EEo.setText("0.5")
        self.label_Ema = QLabel("Coef. de transferencia de masa A:")
        self.input_Ema = QLineEdit(self)
        self.input_Ema.setValidator(float_validator)
        self.input_Ema.setText("0.5")
        self.label_Eca = QLabel("Concentración de A*:")
        self.input_Eca = QLineEdit(self)
        self.input_Eca.setValidator(float_validator)
        self.input_Eca.setText("4.0")
        self.label_Ecy = QLabel("Concentración de Y*:")
        self.input_Ecy = QLineEdit(self)
        self.input_Ecy.setValidator(float_validator)
        self.input_Ecy.setText("0.7")
        self.label_Eq = QLabel("Coeficiente estequiométrico q para Y*:")
        self.input_Eq = QLineEdit(self)
        self.input_Eq.setValidator(int_validator)
        self.input_Eq.setText("1")

        layout_E.addWidget(self.label_DescE)
        layout_E.addWidget(self.label_En)
        layout_E.addWidget(self.input_En)
        layout_E.addWidget(self.label_EArea)
        layout_E.addWidget(self.input_EArea)
        layout_E.addWidget(self.label_Emo)
        layout_E.addWidget(self.input_Emo)
        layout_E.addWidget(self.label_Emr)
        layout_E.addWidget(self.input_Emr)
        layout_E.addWidget(self.label_Eco)
        layout_E.addWidget(self.input_Eco)
        layout_E.addWidget(self.label_Ecr)
        layout_E.addWidget(self.input_Ecr)
        layout_E.addWidget(self.label_EEo)
        layout_E.addWidget(self.input_EEo)
        layout_E.addWidget(self.label_Ema)
        layout_E.addWidget(self.input_Ema)
        layout_E.addWidget(self.label_Eca)
        layout_E.addWidget(self.input_Eca)
        layout_E.addWidget(self.label_Ecy)
        layout_E.addWidget(self.input_Ecy)
        layout_E.addWidget(self.label_Eq)
        layout_E.addWidget(self.input_Eq)

        spacerE = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_E.addItem(spacerE)

        self.tab_E.setLayout(layout_E)

        # Layout de la pestaña F
        layout_F = QVBoxLayout()
        self.label_DescF = QLabel(
            "Descripción:\n\n El agente Y facilita la reacción (reacciones irreversibles).\n"
        )
        self.label_Fn = QLabel("Electrones(n):")
        self.input_Fn = QLineEdit(self)
        self.input_Fn.setValidator(int_validator)
        self.input_Fn.setText("1")
        self.label_FArea = QLabel("Área (cm²):")
        self.input_FArea = QLineEdit(self)
        self.input_FArea.setValidator(float_validator)
        self.input_FArea.setText("1.0")
        self.label_Fmo = QLabel("Coef. de transferencia de masa 0:")
        self.input_Fmo = QLineEdit(self)
        self.input_Fmo.setValidator(float_validator)
        self.input_Fmo.setText("0.5")
        self.label_Fmr = QLabel("Coef. de transferencia de masa R:")
        self.input_Fmr = QLineEdit(self)
        self.input_Fmr.setValidator(float_validator)
        self.input_Fmr.setText("0.3")
        self.label_Fco = QLabel("Concentración O*:")
        self.input_Fco = QLineEdit(self)
        self.input_Fco.setValidator(float_validator)
        self.input_Fco.setText("1.0")
        self.label_Fcr = QLabel("Concentración R* (no aplica):")
        self.input_Fcr = QLineEdit(self)
        self.input_Fcr.setValidator(float_validator)
        self.input_Fcr.setText("0")
        self.input_Fcr.setDisabled(True)
        self.label_FEo = QLabel("E°':")
        self.input_FEo = QLineEdit(self)
        self.input_FEo.setValidator(float_validator)
        self.input_FEo.setText("0.5")
        self.label_Fma = QLabel("Coef. de transferencia de masa A:")
        self.input_Fma = QLineEdit(self)
        self.input_Fma.setValidator(float_validator)
        self.input_Fma.setText("0.5")
        self.label_Fca = QLabel("Concentración de A*:")
        self.input_Fca = QLineEdit(self)
        self.input_Fca.setValidator(float_validator)
        self.input_Fca.setText("4.0")
        self.label_Fcy = QLabel("Concentración de Y*:")
        self.input_Fcy = QLineEdit(self)
        self.input_Fcy.setValidator(float_validator)
        self.input_Fcy.setText("0.7")
        self.label_Fq = QLabel("Coeficiente estequiométrico q para Y*:")
        self.input_Fq = QLineEdit(self)
        self.input_Fq.setValidator(int_validator)
        self.input_Fq.setText("1")
        self.label_Fu = QLabel("Espesor de capa de reacción (µm):")
        self.input_Fu = QLineEdit(self)
        self.input_Fu.setValidator(float_validator)
        self.input_Fu.setText("30")

        layout_F.addWidget(self.label_DescF)
        layout_F.addWidget(self.label_Fn)
        layout_F.addWidget(self.input_Fn)
        layout_F.addWidget(self.label_FArea)
        layout_F.addWidget(self.input_FArea)
        layout_F.addWidget(self.label_Fmo)
        layout_F.addWidget(self.input_Fmo)
        layout_F.addWidget(self.label_Fmr)
        layout_F.addWidget(self.input_Fmr)
        layout_F.addWidget(self.label_Fco)
        layout_F.addWidget(self.input_Fco)
        layout_F.addWidget(self.label_Fcr)
        layout_F.addWidget(self.input_Fcr)
        layout_F.addWidget(self.label_FEo)
        layout_F.addWidget(self.input_FEo)
        layout_F.addWidget(self.label_Fma)
        layout_F.addWidget(self.input_Fma)
        layout_F.addWidget(self.label_Fca)
        layout_F.addWidget(self.input_Fca)
        layout_F.addWidget(self.label_Fcy)
        layout_F.addWidget(self.input_Fcy)
        layout_F.addWidget(self.label_Fq)
        layout_F.addWidget(self.input_Fq)
        layout_F.addWidget(self.label_Fu)
        layout_F.addWidget(self.input_Fu)

        spacerF = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_F.addItem(spacerF)

        self.tab_F.setLayout(layout_F)

        # Crear el widget para la gráfica
        self.graph_widget = QWidget(self)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumWidth(500)
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

        self.input_Dn.textChanged.connect(self.check_inputs)
        self.input_DArea.textChanged.connect(self.check_inputs)
        self.input_Dmo.textChanged.connect(self.check_inputs)
        self.input_Dmr.textChanged.connect(self.check_inputs)
        self.input_Dco.textChanged.connect(self.check_inputs)
        self.input_Dcr.textChanged.connect(self.check_inputs)
        self.input_DEo.textChanged.connect(self.check_inputs)

        self.input_En.textChanged.connect(self.check_inputs)
        self.input_EArea.textChanged.connect(self.check_inputs)
        self.input_Emo.textChanged.connect(self.check_inputs)
        self.input_Emr.textChanged.connect(self.check_inputs)
        self.input_Eco.textChanged.connect(self.check_inputs)
        self.input_Ecr.textChanged.connect(self.check_inputs)
        self.input_EEo.textChanged.connect(self.check_inputs)
        self.input_Ema.textChanged.connect(self.check_inputs)
        self.input_Eca.textChanged.connect(self.check_inputs)
        self.input_Ecy.textChanged.connect(self.check_inputs)
        self.input_Eq.textChanged.connect(self.check_inputs)

        self.input_Fn.textChanged.connect(self.check_inputs)
        self.input_FArea.textChanged.connect(self.check_inputs)
        self.input_Fmo.textChanged.connect(self.check_inputs)
        self.input_Fmr.textChanged.connect(self.check_inputs)
        self.input_Fco.textChanged.connect(self.check_inputs)
        self.input_Fcr.textChanged.connect(self.check_inputs)
        self.input_FEo.textChanged.connect(self.check_inputs)
        self.input_Fma.textChanged.connect(self.check_inputs)
        self.input_Fca.textChanged.connect(self.check_inputs)
        self.input_Fcy.textChanged.connect(self.check_inputs)
        self.input_Fq.textChanged.connect(self.check_inputs)
        self.input_Fu.textChanged.connect(self.check_inputs)

        # Menú de idioma
        self._build_language_menu()

        # Aplicar el idioma guardado a textos estáticos
        self.apply_language(self.lang)

    def _build_language_menu(self):
        menubar = self.menuBar()
        menu = menubar.addMenu("Idioma / Language")

        # Acciones exclusivas
        from PyQt5.QtWidgets import QAction, QActionGroup

        group = QActionGroup(self)
        group.setExclusive(True)

        act_es = QAction("Español", self, checkable=True)
        act_en = QAction("English", self, checkable=True)
        group.addAction(act_es)
        group.addAction(act_en)
        menu.addAction(act_es)
        menu.addAction(act_en)

        # Check inicial según preferencia
        if (self.lang or "es") == "es":
            act_es.setChecked(True)
        else:
            act_en.setChecked(True)

        # Conectar cambios
        act_es.triggered.connect(lambda: self.on_change_language("es"))
        act_en.triggered.connect(lambda: self.on_change_language("en"))

    def on_change_language(self, lang: str):
        if lang not in ("es", "en"):
            return
        self.lang = lang
        self.settings.setValue("lang", lang)  # Persistir
        self.apply_language(lang)

    def _translation_tables(self):
        # Mapeo literal ES -> EN para etiquetas/títulos estáticos
        ES_TO_EN = {
            "Gráficadora de reacciones electroquímicas": "Electrochemical Reaction Grapher",
            # Títulos de pestañas
            "Caso A": "Case A",
            "Caso B": "Case B",
            "Caso C": "Case C",
            "Caso D": "Case D",
            "Caso E": "Case E",
            "Caso F": "Case F",
            # Descripciones
            "Descripción:\n\nR está ausente, pero O está presente.\n": "Description:\n\nR is absent, O is present.\n",
            "Descripción:\n\nO y R están presentes desde el inicio.\n": "Description:\n\nBoth O and R are present initially.\n",
            "Descripción:\n\nR está presente, pero está O ausente.\n": "Description:\n\nR is present, but O is absent.\n",
            "Descripción:\n\nR es insoluble.\n": "Description:\n\nR is insoluble.\n",
            "Descripción:\n\nHay un agente acomplejante (Y) que afecta a la especie O (reacciones reversibles).\n": "Description:\n\nA complexing agent (Y) affects species O (reversible reactions).\n",
            "Descripción:\n\n El agente Y facilita la reacción (reacciones irreversibles).\n": "Description:\n\nAgent Y facilitates the reaction (irreversible reactions).\n",
            # Campos comunes
            "Electrones(n):": "Electrons (n):",
            "Área (cm²):": "Area (cm²):",
            "Coef. de transferencia de masa 0:": "Mass transfer coeff. O:",
            "Coef. de transferencia de masa R:": "Mass transfer coeff. R:",
            "Concentración O*:": "Concentration O*:",
            "Concentración R* (No aplica):": "Concentration R* (N/A):",
            "Concentración R*:": "Concentration R*:",
            "Concentración O* (no aplica):": "Concentration O* (N/A):",
            "Concentración R* (no aplica):": "Concentration R* (N/A):",
            "E°':": "E°':",
            # Caso E/F adicionales
            "Coef. de transferencia de masa A:": "Mass transfer coeff. A:",
            "Concentración de A*:": "Concentration A*:",
            "Concentración de Y*:": "Concentration Y*:",
            "Coeficiente estequiométrico q para Y*:": "Stoichiometric coefficient q for Y*:",
            "Espesor de capa de reacción (µm):": "Reaction layer thickness (µm):",
            # Ejes y títulos de gráfica (estáticos)
            "Corriente contra Potencial": "Current vs Potential",
            "E (V)": "E (V)",
            "I (mA)": "I (mA)",
            # Leyendas comunes (texto exacto sin valores numéricos)
            "0 A": "0 A",
        }

        # Construye EN->ES automáticamente
        EN_TO_ES = {v: k for k, v in ES_TO_EN.items()}
        return ES_TO_EN, EN_TO_ES

    def apply_language(self, lang: str):
        ES_TO_EN, EN_TO_ES = self._translation_tables()

        # 1) Título de la ventana
        if lang == "en":
            title = ES_TO_EN.get(self.windowTitle(), None)
            if title:
                self.setWindowTitle(title)
        else:
            title = EN_TO_ES.get(self.windowTitle(), None)
            if title:
                self.setWindowTitle(title)

        # 2) Títulos de pestañas (índices 0..5)
        tab_titles_es = ["Caso A", "Caso B", "Caso C", "Caso D", "Caso E", "Caso F"]
        for idx, es_title in enumerate(tab_titles_es):
            current = self.tabs.tabText(idx)
            if lang == "en":
                new = ES_TO_EN.get(current, ES_TO_EN.get(es_title, current))
            else:
                # Si ya está en inglés o no coincide, intenta revertir
                new = EN_TO_ES.get(
                    current, EN_TO_ES.get(ES_TO_EN.get(es_title, ""), current)
                )
            self.tabs.setTabText(idx, new)

        # 3) Todos los QLabel del formulario (traducción literal si hay clave)
        for lbl in self.findChildren(QLabel):
            txt = lbl.text()
            if lang == "en":
                if txt in ES_TO_EN:
                    lbl.setText(ES_TO_EN[txt])
            else:
                if txt in EN_TO_ES:
                    lbl.setText(EN_TO_ES[txt])

        # NOTA: Títulos/leyendas generados dentro de plot_* pueden seguir en ES.
        # Abajo dejo un TODO para internacionalizar también las gráficas.

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

        # Si la pestaña activa es la tercera, generar gráfica
        elif current_tab == 3:
            try:
                Dn = float(self.input_Dn.text())
                DArea = float(self.input_DArea.text())
                Dmo = float(self.input_Dmo.text())
                Dmr = float(self.input_Dmr.text())
                Dco = float(self.input_Dco.text())
                Dcr = float(self.input_Dcr.text())
                DEo = float(self.input_DEo.text())
                print("Variables D correctas")
                self.plot_graph_D(Dn, DArea, Dmo, Dmr, Dco, Dcr, DEo)
            except ValueError:
                print("Error de valor")
                return

        # Si la pestaña activa es la quinta, generar gráfica
        elif current_tab == 4:
            try:
                En = float(self.input_En.text())
                EArea = float(self.input_EArea.text())
                Emo = float(self.input_Emo.text())
                Emr = float(self.input_Emr.text())
                Eco = float(self.input_Eco.text())
                Ecr = float(self.input_Ecr.text())
                EEo = float(self.input_EEo.text())
                Ema = float(self.input_Ema.text())
                Eca = float(self.input_Eca.text())
                Ecy = float(self.input_Ecy.text())
                Eq = float(self.input_Eq.text())
                print("Variables E correctas")
                self.plot_graph_E(En, EArea, Emo, Emr, Eco, Ecr, EEo, Ema, Eca, Ecy, Eq)
            except ValueError:
                print("Error de valor")
                return

        # Si la pestaña activa es la sexta, generar gráfica
        elif current_tab == 5:
            try:
                Fn = float(self.input_Fn.text())
                FArea = float(self.input_FArea.text())
                Fmo = float(self.input_Fmo.text())
                Fmr = float(self.input_Fmr.text())
                Fco = float(self.input_Fco.text())
                Fcr = float(self.input_Fcr.text())
                FEo = float(self.input_FEo.text())
                Fma = float(self.input_Fma.text())
                Fca = float(self.input_Fca.text())
                Fcy = float(self.input_Fcy.text())
                Fq = float(self.input_Fq.text())
                Fu = float(self.input_Fu.text())
                print("Variables F correctas")
                self.plot_graph_F(
                    Fn, FArea, Fmo, Fmr, Fco, Fcr, FEo, Fma, Fca, Fcy, Fq, Fu
                )
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
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

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
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

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
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

        print("completadooooooooooo")
        # Dibujar gŕafica
        self.canvas.draw()

    def plot_graph_D(self, Dn, DArea, Dmo, Dmr, Dco, Dcr, DEo):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LC = Dmo * Dn * F * DArea * 0.0001 * Dco
        I = np.linspace(0, 0.95 * I_LC, 400)
        try:
            E_eq = DEo - R * T * np.log(1 / Dco) / Dn / F
            # exponencial = np.exp((Dn * F) * (DEo - E) / (R * T))
            # I = I_LC - I_LC / (Dco * exponencial)
            E = E_eq - R * T * np.log(I_LC / (I_LC - I)) / Dn / F
            # sobrepotencial = R * T * np.log((I_LC - I) / I_LC) / Dn / F
            # print(E)
        except:
            print("Ignorando división por cero")
            return
        # print("I:", I)
        print("I_LC:", I_LC)
        print("E_eq:", E_eq)
        # print("sobrepotencial:", sobrepotencial)

        # recta_ilcx = np.array([np.min(E), np.max(E)])
        # recta_ilcy = np.array([I_LA, I_LA])
        recta_ilax = np.array([np.min(E), np.max(E)])
        recta_ilay = np.array([I_LC, I_LC])
        Vx = np.array([E_eq, E_eq])
        Vy = np.array([np.min(I), np.max(I)])
        ax.plot(
            Vx,
            Vy,
            linestyle="--",
            linewidth=2,
            color="#F72226",
            label="$E_{eq}$" + f" = {E_eq:.6f} V",
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
            recta_ilax,
            np.array([0, 0]),
            linestyle="--",
            linewidth=2,
            color="#861491",
            label=f"0 A",
        )
        # ax.plot(
        # recta_ilcx,
        # recta_ilcy,
        # linestyle="--",
        # linewidth=2,
        # color="#168491",
        # label="$I_{LA}$" + f" = {I_LA:.6f} mA",
        # )
        # ax.set_xticks(np.linspace(-2, 2, 11))  # divisions on the x-axis
        ax.plot(E, I, linewidth=3, color="#101030")
        ax.grid(True)
        ax.legend()
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

        # Dibujar gŕafica
        self.canvas.draw()

    def plot_graph_E(self, En, EArea, Emo, Emr, Eco, Ecr, EEo, Ema, Eca, Ecy, Eq):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LC = Ema * En * F * EArea * 0.0001 * Eca
        try:
            k = Eco * Ecy**Eq / Eca
            E_central = (
                EEo
                + R * T * np.log(k) / En / F
                + R * T * np.log(Emr / Ema) / En / F
                - R * T * Eq * np.log(Ecy) / En / F
            )
            exponencial = (
                (Eca / Eco) * (Ema / Emr) * np.exp((En * F) * (E - EEo) / (R * T))
            )
            I = I_LC / (1 + exponencial)
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
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

        # Dibujar la nueva gráfica
        self.canvas.draw()

    def plot_graph_F(self, Fn, FArea, Fmo, Fmr, Fco, Fcr, FEo, Fma, Fca, Fcy, Fq, Fu):
        # Limpiar la gráfica anterior
        self.figure.clear()

        # Crear el eje para la nueva gráfica
        ax = self.figure.add_subplot(111)

        E = np.linspace(-2, 2, 300)
        I_LC = Fma * Fn * F * FArea * 0.0001 * Fca
        try:
            k = Fco * Fcy**Fq / Fca
            E_central = FEo - R * T * np.log((Fmr + Fu * k) / Fmo) / Fn / F
            exponencial = ((Fmr + Fu * k) / Fmo) * np.exp(
                (Fn * F) * (E - FEo) / (R * T)
            )
            I = I_LC / (1 + exponencial)
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
        ax.set_title(self._("Corriente contra Potencial"))
        ax.set_xlabel(self._("E (V)"))
        ax.set_ylabel(self._("I (mA)"))

        # Dibujar la nueva gráfica
        self.canvas.draw()

    def _(self, s: str) -> str:
        ES_TO_EN, EN_TO_ES = self._translation_tables()
        if self.lang == "en":
            return ES_TO_EN.get(s, s)
        return EN_TO_ES.get(s, s) if s in EN_TO_ES else s


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    window.check_inputs()
    sys.exit(app.exec_())
