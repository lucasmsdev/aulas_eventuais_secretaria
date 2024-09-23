import sys
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QFormLayout, QComboBox, QDateTimeEdit, QTextEdit, QSpinBox,
    QGroupBox, QTableWidget, QTableWidgetItem, QLabel, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDateTime, QDate

# Configuração do Firebase
cred = credentials.Certificate('aulaseventuais-966ef-firebase-adminsdk-swryz-f9bcd4c14a.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aulaseventuais-966ef-default-rtdb.firebaseio.com/'
})

# Função para carregar os dados do Firebase
def load_from_firebase(path):
    ref = db.reference(path)
    data = ref.get()
    if data is None:
        return pd.DataFrame()
    
    # Verifica se os dados são uma lista
    if isinstance(data, list):
        # Converte a lista em DataFrame
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        # Converte o dicionário em DataFrame
        return pd.DataFrame.from_dict(data, orient='index')
    else:
        return pd.DataFrame()

# Função para salvar os dados no Firebase
def save_to_firebase(path, df):
    ref = db.reference(path)
    ref.set(df.to_dict(orient='index'))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Eventuais")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Botões de Cadastro
        self.add_button(layout, "Cadastro de Eventuais", self.cadastroEventuais)
        self.add_button(layout, "Cadastro de Professores Efetivos", self.cadastroEfetivos)
        self.add_button(layout, "Cadastro de Aulas Eventuais", self.cadastroAulasEventuais)

        # Botões de Listagem
        self.add_button(layout, "Listar Professores Eventuais", self.listarEventuais)
        self.add_button(layout, "Listar Professores Efetivos", self.listarEfetivos)
        self.add_button(layout, "Listar Aulas Eventuais", self.listarAulas)

        # Grupo para Relatórios e Gráficos
        groupbox = QGroupBox("Relatórios e Gráficos")
        groupbox_layout = QVBoxLayout()

        self.add_button(groupbox_layout, "Gerar Gráfico Mensal (EM BREVE)", self.gerarGraficoMensal)
        self.add_button(groupbox_layout, "Gerar Gráfico Anual (EM BREVE)", self.gerarGraficoAnual)
        self.add_button(groupbox_layout, "Gerar Relatório Diário (EM BREVE)", self.gerarRelatorioDiario)

        groupbox.setLayout(groupbox_layout)
        layout.addWidget(groupbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_button(self, layout, text, func):
        button = QPushButton(text)
        button.clicked.connect(func)
        layout.addWidget(button)

    def cadastroEventuais(self):
        self.formWindow = CadastroWindow("Cadastro de Eventuais", 'eventuais')
        self.formWindow.show()

    def cadastroEfetivos(self):
        self.formWindow = CadastroEfetivosWindow()
        self.formWindow.show()

    def cadastroAulasEventuais(self):
        self.formWindow = CadastroAulasEventuaisWindow()
        self.formWindow.show()

    def listarEventuais(self):
        self.listWindow = ListarProfessoresWindow("Listar Professores Eventuais", 'eventuais')
        self.listWindow.show()

    def listarEfetivos(self):
        self.listWindow = ListarProfessoresWindow("Listar Professores Efetivos", 'efetivos')
        self.listWindow.show()

    def listarAulas(self):
        self.listWindow = ListarAulasEventuaisWindow()
        self.listWindow.show()

    def gerarGraficoMensal(self):
        self.graficoMensalWindow = GraficoWindow('mensal')
        self.graficoMensalWindow.show()

    def gerarGraficoAnual(self):
        self.graficoAnualWindow = GraficoWindow('anual')
        self.graficoAnualWindow.show()

    def gerarRelatorioDiario(self):
        self.relatorioDiarioWindow = RelatorioDiarioWindow()
        self.relatorioDiarioWindow.show()

class CadastroWindow(QWidget):
    def __init__(self, title, path):
        super().__init__()
        self.setWindowTitle(title)
        self.path = path
        self.layout = QFormLayout()

        self.nome = QLineEdit()
        self.cpf = QLineEdit()
        self.conta = QLineEdit()
        self.agencia = QLineEdit()
        self.banco = QLineEdit()

        self.layout.addRow("Nome:", self.nome)
        self.layout.addRow("CPF:", self.cpf)
        self.layout.addRow("Conta:", self.conta)
        self.layout.addRow("Agência:", self.agencia)
        self.layout.addRow("Banco:", self.banco)

        self.btnSalvar = QPushButton("Salvar")
        self.btnSalvar.clicked.connect(self.salvar)
        self.layout.addRow("", self.btnSalvar)

        self.setLayout(self.layout)

    def salvar(self):
        try:
            nome = self.nome.text()
            cpf = self.cpf.text()
            conta = self.conta.text()
            agencia = self.agencia.text()
            banco = self.banco.text()

            # Carregar dados existentes
            df = load_from_firebase(self.path)

            # Adicionar nova entrada
            nova_linha = pd.DataFrame([{
                'Nome': nome,
                'CPF': cpf,
                'Conta': conta,
                'Agência': agencia,
                'Banco': banco
            }])

            df = pd.concat([df, nova_linha], ignore_index=True)

            # Salvar no Firebase
            save_to_firebase(self.path, df)
            self.close()
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

class CadastroEfetivosWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Professores Efetivos")
        self.layout = QFormLayout()

        self.nome = QLineEdit()
        self.cpf = QLineEdit()
        self.nif = QLineEdit()

        self.layout.addRow("Nome:", self.nome)
        self.layout.addRow("CPF:", self.cpf)
        self.layout.addRow("NIF:", self.nif)

        self.btnSalvar = QPushButton("Salvar")
        self.btnSalvar.clicked.connect(self.salvar)
        self.layout.addRow("", self.btnSalvar)

        self.setLayout(self.layout)

    def salvar(self):
        try:
            nome = self.nome.text()
            cpf = self.cpf.text()
            nif = self.nif.text()

            # Carregar dados existentes
            df = load_from_firebase('efetivos')

            # Adicionar nova entrada
            nova_linha = pd.DataFrame([{
                'Nome': nome,
                'CPF': cpf,
                'NIF': nif
            }])

            df = pd.concat([df, nova_linha], ignore_index=True)

            # Salvar no Firebase
            save_to_firebase('efetivos', df)
            self.close()
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

class ListarProfessoresWindow(QWidget):
    def __init__(self, title, path):
        super().__init__()
        self.setWindowTitle(title)
        self.path = path
        self.layout = QVBoxLayout()
        self.table = QTableWidget()

        self.layout.addWidget(self.table)
        
        # Botão para excluir o item selecionado
        self.btnExcluir = QPushButton("Excluir Selecionado")
        self.btnExcluir.clicked.connect(self.excluirSelecionado)
        self.layout.addWidget(self.btnExcluir)

        self.setLayout(self.layout)

        self.carregarDados()

    def carregarDados(self):
        try:
            df = load_from_firebase(self.path)
            self.table.setRowCount(df.shape[0])
            self.table.setColumnCount(df.shape[1])
            self.table.setHorizontalHeaderLabels(df.columns)

            for i, row in df.iterrows():
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")

    def excluirSelecionado(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row >= 0:
                df = load_from_firebase(self.path)
                df = df.drop(df.index[selected_row]).reset_index(drop=True)
                save_to_firebase(self.path, df)
                self.carregarDados()
        except Exception as e:
            print(f"Erro ao excluir os dados: {e}")

class CadastroAulasEventuaisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Aulas Eventuais")
        self.layout = QFormLayout()

        self.professor_eventual = QComboBox()
        self.professor_efetivo = QComboBox()

        self.data_aula = QDateEdit()
        self.data_aula.setDate(QDate.currentDate())

        self.layout.addRow("Professor Eventual:", self.professor_eventual)
        self.layout.addRow("Professor Efetivo:", self.professor_efetivo)
        self.layout.addRow("Data da Aula:", self.data_aula)

        self.btnSalvar = QPushButton("Salvar")
        self.btnSalvar.clicked.connect(self.salvar)
        self.layout.addRow("", self.btnSalvar)

        self.setLayout(self.layout)
        self.carregarProfessores()

    def carregarProfessores(self):
        # Carregar professores eventuais e efetivos para preencher o combo box
        eventuais_df = load_from_firebase('eventuais')
        efetivos_df = load_from_firebase('efetivos')

        self.professor_eventual.addItems(eventuais_df['Nome'].tolist())
        self.professor_efetivo.addItems(efetivos_df['Nome'].tolist())

    def salvar(self):
        try:
            eventual = self.professor_eventual.currentText()
            efetivo = self.professor_efetivo.currentText()
            data_aula = self.data_aula.date().toString("dd/MM/yyyy")

            aulas_df = load_from_firebase('aulas_eventuais')

            nova_linha = pd.DataFrame([{
                'Nome Professor Eventual': eventual,
                'Nome Professor Efetivo': efetivo,
                'Data da Aula': data_aula
            }])

            aulas_df = pd.concat([aulas_df, nova_linha], ignore_index=True)
            save_to_firebase('aulas_eventuais', aulas_df)
            self.close()

        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

class ListarAulasEventuaisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listar Aulas Eventuais")
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Campo de pesquisa e botão
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Pesquisar...")
        self.search_button = QPushButton("Pesquisar")
        self.search_button.clicked.connect(self.pesquisar)

        self.layout.addWidget(self.search_field)
        self.layout.addWidget(self.search_button)

        self.setLayout(self.layout)
        self.carregarDados()

    def carregarDados(self):
        try:
            # Carregar dados
            aulas_df = load_from_firebase('aulas_eventuais')
            eventuais_df = load_from_firebase('eventuais')
            efetivos_df = load_from_firebase('efetivos')

            # Mapeamento de CPF para Nome (professor eventual)
            eventuais_map = dict(zip(eventuais_df['CPF'], eventuais_df['Nome']))

            # Mapeamento de CPF para Nome e NIF (professor efetivo)
            efetivos_nome_map = dict(zip(efetivos_df['CPF'], efetivos_df['Nome']))
            efetivos_nif_map = dict(zip(efetivos_df['CPF'], efetivos_df['NIF']))

            # Adicionar colunas de nome e NIF dos professores ao DataFrame de aulas eventuais
            aulas_df['Nome Professor Eventual'] = aulas_df['CPF Professor Eventual'].map(eventuais_map)
            aulas_df['Nome Professor Efetivo'] = aulas_df['CPF Professor Efetivo'].map(efetivos_nome_map)
            aulas_df['NIF Professor Efetivo'] = aulas_df['CPF Professor Efetivo'].map(efetivos_nif_map)

            # Definir o número de linhas e colunas na tabela
            self.table.setRowCount(aulas_df.shape[0])
            self.table.setColumnCount(aulas_df.shape[1])
            self.table.setHorizontalHeaderLabels(aulas_df.columns)

            for i, row in aulas_df.iterrows():
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

        except Exception as e:
            print(f"Erro ao carregar os dados: {e}")

    def excluirSelecionado(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row >= 0:
                df = load_from_firebase('aulas_eventuais')
                df = df.drop(df.index[selected_row]).reset_index(drop=True)
                save_to_firebase('aulas_eventuais', df)
                self.carregarDados()
        except Exception as e:
            print(f"Erro ao excluir os dados: {e}")

    def pesquisar(self):
        query = self.search_field.text().strip()  # Remover espaços extras
        self.filtrarDados(query)

    def filtrarDados(self, query):
        try:
            # Carregar todos os dados
            aulas_df = load_from_firebase('aulas_eventuais')
            eventuais_df = load_from_firebase('eventuais')
            efetivos_df = load_from_firebase('efetivos')

            # Mapeamento de CPF para Nome (professor eventual)
            eventuais_df['Nome'] = eventuais_df['Nome'].str.strip()  # Remover espaços extras
            eventuais_map = dict(zip(eventuais_df['CPF'], eventuais_df['Nome']))

            # Mapeamento de CPF para Nome e NIF (professor efetivo)
            efetivos_df['Nome'] = efetivos_df['Nome'].str.strip()  # Remover espaços extras
            efetivos_df['NIF'] = efetivos_df['NIF'].str.strip()  # Remover espaços extras
            efetivos_nome_map = dict(zip(efetivos_df['CPF'], efetivos_df['Nome']))
            efetivos_nif_map = dict(zip(efetivos_df['CPF'], efetivos_df['NIF']))

            # Adicionar colunas de nome e NIF dos professores ao DataFrame de aulas eventuais
            aulas_df['Nome Professor Eventual'] = aulas_df['CPF Professor Eventual'].map(eventuais_map).str.strip()
            aulas_df['Nome Professor Efetivo'] = aulas_df['CPF Professor Efetivo'].map(efetivos_nome_map).str.strip()
            aulas_df['NIF Professor Efetivo'] = aulas_df['CPF Professor Efetivo'].map(efetivos_nif_map).str.strip()

            # Aplicar filtro baseado no campo de pesquisa com correspondência exata
            if query:
                query = query.strip().lower()  # Remover espaços extras e garantir que tudo esteja em minúsculas
                aulas_df = aulas_df[
                    (aulas_df['Nome Professor Eventual'].str.lower().str.contains(f'^{query}$')) |  # Comparação exata
                    (aulas_df['Nome Professor Efetivo'].str.lower().str.contains(f'^{query}$')) |  # Comparação exata
                    (aulas_df['Data da Aula'].str.contains(query, case=False))  # Permitir busca parcial na data
                ]

            # Atualizar a tabela com os dados filtrados
            self.table.setRowCount(aulas_df.shape[0])
            self.table.setColumnCount(aulas_df.shape[1])
            self.table.setHorizontalHeaderLabels(aulas_df.columns)

            for i, row in aulas_df.iterrows():
                for j, val in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))

        except Exception as e:
            print(f"Erro ao filtrar os dados: {e}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
