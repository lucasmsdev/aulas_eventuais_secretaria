import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import firebase_admin
from firebase_admin import credentials, db

# Inicializar Firebase
cred = credentials.Certificate('aulaseventuais-966ef-firebase-adminsdk-swryz-f9bcd4c14a.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aulaseventuais-966ef-default-rtdb.firebaseio.com/'
})

# Referências ao banco de dados
eventuais_ref = db.reference('eventuais')
efetivos_ref = db.reference('efetivos')
aulas_eventuais_ref = db.reference('aulas_eventuais')

class CadastroApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Cadastro")

        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Botões para ações
        self.btn_eventuais = QtWidgets.QPushButton('Cadastro de Eventuais')
        self.btn_eventuais.clicked.connect(self.cadastro_eventuais)
        layout.addWidget(self.btn_eventuais)

        self.btn_efetivos = QtWidgets.QPushButton('Cadastro de Professores Efetivos')
        self.btn_efetivos.clicked.connect(self.cadastro_efetivos)
        layout.addWidget(self.btn_efetivos)

        self.btn_aulas_eventuais = QtWidgets.QPushButton('Cadastro de Aulas Eventuais')
        self.btn_aulas_eventuais.clicked.connect(self.cadastro_aulas_eventuais)
        layout.addWidget(self.btn_aulas_eventuais)

        self.btn_listar_eventuais = QtWidgets.QPushButton('Listar Professores Eventuais')
        self.btn_listar_eventuais.clicked.connect(self.listar_eventuais)
        layout.addWidget(self.btn_listar_eventuais)

        self.btn_listar_efetivos = QtWidgets.QPushButton('Listar Professores Efetivos')
        self.btn_listar_efetivos.clicked.connect(self.listar_efetivos)
        layout.addWidget(self.btn_listar_efetivos)

        self.btn_listar_aulas = QtWidgets.QPushButton('Listar Aulas Eventuais')
        self.btn_listar_aulas.clicked.connect(self.listar_aulas_eventuais)
        layout.addWidget(self.btn_listar_aulas)

        self.btn_sair = QtWidgets.QPushButton('Sair')
        self.btn_sair.clicked.connect(self.close)
        layout.addWidget(self.btn_sair)

        self.setLayout(layout)

    def cadastro_eventuais(self):
        self.window_eventuais = QtWidgets.QDialog()
        self.window_eventuais.setWindowTitle("Cadastro de Eventuais")

        layout = QtWidgets.QVBoxLayout()
        self.entry_nome_eventuais = QtWidgets.QLineEdit()
        self.entry_cpf_eventuais = QtWidgets.QLineEdit()
        self.entry_conta_eventuais = QtWidgets.QLineEdit()
        self.entry_agencia_eventuais = QtWidgets.QLineEdit()
        self.entry_banco_eventuais = QtWidgets.QLineEdit()

        layout.addWidget(QtWidgets.QLabel('Nome'))
        layout.addWidget(self.entry_nome_eventuais)
        layout.addWidget(QtWidgets.QLabel('CPF'))
        layout.addWidget(self.entry_cpf_eventuais)
        layout.addWidget(QtWidgets.QLabel('Conta'))
        layout.addWidget(self.entry_conta_eventuais)
        layout.addWidget(QtWidgets.QLabel('Agência'))
        layout.addWidget(self.entry_agencia_eventuais)
        layout.addWidget(QtWidgets.QLabel('Banco'))
        layout.addWidget(self.entry_banco_eventuais)

        btn_salvar = QtWidgets.QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvar_eventuais)
        layout.addWidget(btn_salvar)

        self.window_eventuais.setLayout(layout)
        self.window_eventuais.exec_()

    def salvar_eventuais(self):
        nome = self.entry_nome_eventuais.text()
        cpf = self.entry_cpf_eventuais.text()
        conta = self.entry_conta_eventuais.text()
        agencia = self.entry_agencia_eventuais.text()
        banco = self.entry_banco_eventuais.text()

        eventuais_ref.push({
            'nome': nome,
            'cpf': cpf,
            'conta': conta,
            'agencia': agencia,
            'banco': banco
        })
        QtWidgets.QMessageBox.information(self, 'Sucesso', 'Cadastro salvo com sucesso!')
        self.window_eventuais.close()

    def cadastro_efetivos(self):
        self.window_efetivos = QtWidgets.QDialog()
        self.window_efetivos.setWindowTitle("Cadastro de Professores Efetivos")

        layout = QtWidgets.QVBoxLayout()
        self.entry_nome_efetivos = QtWidgets.QLineEdit()
        self.entry_cpf_efetivos = QtWidgets.QLineEdit()
        self.entry_nif_efetivos = QtWidgets.QLineEdit()
        self.entry_especialidade_efetivos = QtWidgets.QLineEdit()

        layout.addWidget(QtWidgets.QLabel('Nome'))
        layout.addWidget(self.entry_nome_efetivos)
        layout.addWidget(QtWidgets.QLabel('CPF'))
        layout.addWidget(self.entry_cpf_efetivos)
        layout.addWidget(QtWidgets.QLabel('NIF'))
        layout.addWidget(self.entry_nif_efetivos)
        layout.addWidget(QtWidgets.QLabel('Especialidade'))
        layout.addWidget(self.entry_especialidade_efetivos)

        btn_salvar = QtWidgets.QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvar_efetivos)
        layout.addWidget(btn_salvar)

        self.window_efetivos.setLayout(layout)
        self.window_efetivos.exec_()

    def salvar_efetivos(self):
        nome = self.entry_nome_efetivos.text()
        cpf = self.entry_cpf_efetivos.text()
        nif = self.entry_nif_efetivos.text()
        especialidade = self.entry_especialidade_efetivos.text()

        efetivos_ref.push({
            'nome': nome,
            'cpf': cpf,
            'nif': nif,
            'especialidade': especialidade
        })
        QtWidgets.QMessageBox.information(self, 'Sucesso', 'Cadastro salvo com sucesso!')
        self.window_efetivos.close()

    def cadastro_aulas_eventuais(self):
        self.window_aulas_eventuais = QtWidgets.QDialog()
        self.window_aulas_eventuais.setWindowTitle("Cadastro de Aulas Eventuais")

        layout = QtWidgets.QVBoxLayout()

        # ComboBox para professores eventuais
        self.combo_prof_eventual = QtWidgets.QComboBox()
        self.combo_prof_eventual.addItems(self.carregar_eventuais())
        layout.addWidget(QtWidgets.QLabel('Professor Eventual'))
        layout.addWidget(self.combo_prof_eventual)

        # ComboBox para professores efetivos
        self.combo_prof_efetivo = QtWidgets.QComboBox()
        self.combo_prof_efetivo.addItems(self.carregar_efetivos())
        layout.addWidget(QtWidgets.QLabel('Professor Efetivo'))
        layout.addWidget(self.combo_prof_efetivo)

        self.entry_dia_aula = QtWidgets.QLineEdit()  # Novo campo para o dia da aula
        self.entry_horario_entrada = QtWidgets.QLineEdit()
        self.entry_horario_saida = QtWidgets.QLineEdit()
        self.entry_qtd_aulas = QtWidgets.QLineEdit()
        self.entry_observacoes = QtWidgets.QLineEdit()

        layout.addWidget(QtWidgets.QLabel('Dia da Aula'))  # Label para o dia da aula
        layout.addWidget(self.entry_dia_aula)  # Campo para o dia da aula
        layout.addWidget(QtWidgets.QLabel('Horário de Entrada'))
        layout.addWidget(self.entry_horario_entrada)
        layout.addWidget(QtWidgets.QLabel('Horário de Saída'))
        layout.addWidget(self.entry_horario_saida)
        layout.addWidget(QtWidgets.QLabel('Quantidade de Aulas'))
        layout.addWidget(self.entry_qtd_aulas)
        layout.addWidget(QtWidgets.QLabel('Observações'))
        layout.addWidget(self.entry_observacoes)

        btn_salvar = QtWidgets.QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvar_aulas_eventuais)
        layout.addWidget(btn_salvar)

        self.window_aulas_eventuais.setLayout(layout)
        self.window_aulas_eventuais.exec_()

    def carregar_eventuais(self):
        """Carregar os nomes dos professores eventuais do Firebase."""
        eventuais = eventuais_ref.get()
        if isinstance(eventuais, dict):
            return [event['nome'] for event in eventuais.values()]
        return []

    def carregar_efetivos(self):
        """Carregar os nomes dos professores efetivos do Firebase."""
        efetivos = efetivos_ref.get()
        if isinstance(efetivos, dict):
            return [efetivo['nome'] for efetivo in efetivos.values()]
        return []

    def salvar_aulas_eventuais(self):
        prof_eventual = self.combo_prof_eventual.currentText()
        prof_efetivo = self.combo_prof_efetivo.currentText()
        dia_aula = self.entry_dia_aula.text()  # Novo campo dia da aula
        horario_entrada = self.entry_horario_entrada.text()
        horario_saida = self.entry_horario_saida.text()
        qtd_aulas = self.entry_qtd_aulas.text()
        observacoes = self.entry_observacoes.text()

        aulas_eventuais_ref.push({
            'prof_eventual': prof_eventual,
            'prof_efetivo': prof_efetivo,
            'dia_aula': dia_aula,  # Salvar o dia da aula
            'horario_entrada': horario_entrada,
            'horario_saida': horario_saida,
            'qtd_aulas': qtd_aulas,
            'observacoes': observacoes
        })
        QtWidgets.QMessageBox.information(self, 'Sucesso', 'Cadastro de aula eventual salvo com sucesso!')
        self.window_aulas_eventuais.close()

    def listar_eventuais(self):
        self.window_listar_eventuais = QtWidgets.QDialog()
        self.window_listar_eventuais.setWindowTitle("Listagem de Professores Eventuais")
        self.window_listar_eventuais.setMinimumSize(800, 600)  # Tamanho mínimo
        self.window_listar_eventuais.setWindowState(Qt.WindowMaximized)  # Iniciar maximizado

        layout = QtWidgets.QVBoxLayout()
        self.table_eventuais = QtWidgets.QTableWidget()
        self.table_eventuais.setColumnCount(5)
        self.table_eventuais.setHorizontalHeaderLabels(['Nome', 'CPF', 'Conta', 'Agência', 'Banco'])
        layout.addWidget(self.table_eventuais)

        eventuais = eventuais_ref.get()  # Pega todos os eventuais do Firebase
        self.table_eventuais.setRowCount(0)

        if isinstance(eventuais, dict):
            for key, event in eventuais.items():
                row_position = self.table_eventuais.rowCount()
                self.table_eventuais.insertRow(row_position)
                nome = event.get('nome', 'Nome não disponível')
                cpf = event.get('cpf', 'CPF não disponível')
                conta = event.get('conta', 'Conta não disponível')
                agencia = event.get('agencia', 'Agência não disponível')
                banco = event.get('banco', 'Banco não disponível')

                self.table_eventuais.setItem(row_position, 0, QtWidgets.QTableWidgetItem(nome))
                self.table_eventuais.setItem(row_position, 1, QtWidgets.QTableWidgetItem(cpf))
                self.table_eventuais.setItem(row_position, 2, QtWidgets.QTableWidgetItem(conta))
                self.table_eventuais.setItem(row_position, 3, QtWidgets.QTableWidgetItem(agencia))
                self.table_eventuais.setItem(row_position, 4, QtWidgets.QTableWidgetItem(banco))
        else:
            QtWidgets.QMessageBox.information(self, 'Info', "Nenhum registro encontrado.")

        btn_fechar = QtWidgets.QPushButton('Fechar')
        btn_fechar.clicked.connect(self.window_listar_eventuais.close)
        layout.addWidget(btn_fechar)

        self.window_listar_eventuais.setLayout(layout)
        self.window_listar_eventuais.exec_()

    def listar_efetivos(self):
        self.window_listar_efetivos = QtWidgets.QDialog()
        self.window_listar_efetivos.setWindowTitle("Listagem de Professores Efetivos")
        self.window_listar_efetivos.setMinimumSize(800, 600)  # Tamanho mínimo
        self.window_listar_efetivos.setWindowState(Qt.WindowMaximized)  # Iniciar maximizado

        layout = QtWidgets.QVBoxLayout()
        self.table_efetivos = QtWidgets.QTableWidget()
        self.table_efetivos.setColumnCount(4)
        self.table_efetivos.setHorizontalHeaderLabels(['Nome', 'NIF', 'CPF', 'Especialidade'])
        layout.addWidget(self.table_efetivos)

        efetivos = efetivos_ref.get()  # Pega todos os efetivos do Firebase
        self.table_efetivos.setRowCount(0)

        if isinstance(efetivos, dict):
            for key, efetivo in efetivos.items():
                row_position = self.table_efetivos.rowCount()
                self.table_efetivos.insertRow(row_position)
                nome = efetivo.get('nome', 'Nome não disponível')
                cpf = efetivo.get('cpf', 'CPF não disponível')
                nif = efetivo.get('nif', 'NIF não disponível')
                especialidade = efetivo.get('especialidade', 'Especialidade não disponível')

                self.table_efetivos.setItem(row_position, 0, QtWidgets.QTableWidgetItem(nome))
                self.table_efetivos.setItem(row_position, 1, QtWidgets.QTableWidgetItem(nif))  # Incluindo NIF
                self.table_efetivos.setItem(row_position, 2, QtWidgets.QTableWidgetItem(cpf))
                self.table_efetivos.setItem(row_position, 3, QtWidgets.QTableWidgetItem(especialidade))
        else:
            QtWidgets.QMessageBox.information(self, 'Info', "Nenhum registro encontrado.")

        btn_fechar = QtWidgets.QPushButton('Fechar')
        btn_fechar.clicked.connect(self.window_listar_efetivos.close)
        layout.addWidget(btn_fechar)

        self.window_listar_efetivos.setLayout(layout)
        self.window_listar_efetivos.exec_()

    def listar_aulas_eventuais(self):
        self.window_listar_aulas = QtWidgets.QDialog()
        self.window_listar_aulas.setWindowTitle("Listagem de Aulas Eventuais")
        self.window_listar_aulas.setMinimumSize(800, 600)  # Tamanho mínimo
        self.window_listar_aulas.setWindowState(Qt.WindowMaximized)  # Iniciar maximizado

        layout = QtWidgets.QVBoxLayout()
        self.table_aulas = QtWidgets.QTableWidget()
        self.table_aulas.setColumnCount(7)  # Adicionar coluna para o NIF
        self.table_aulas.setHorizontalHeaderLabels(['Professor Eventual', 'NIF Efetivo', 'Professor Efetivo', 'Dia da Aula', 'Horário Entrada', 'Horário Saída', 'Observações'])
        layout.addWidget(self.table_aulas)

        aulas = aulas_eventuais_ref.get()  # Pega todas as aulas eventuais do Firebase
        self.table_aulas.setRowCount(0)

        if isinstance(aulas, dict):
            for key, aula in aulas.items():
                row_position = self.table_aulas.rowCount()
                self.table_aulas.insertRow(row_position)
                prof_eventual = aula.get('prof_eventual', 'Professor eventual não disponível')
                prof_efetivo = aula.get('prof_efetivo', 'Professor efetivo não disponível')
                dia_aula = aula.get('dia_aula', 'Dia da aula não disponível')
                horario_entrada = aula.get('horario_entrada', 'Horário de entrada não disponível')
                horario_saida = aula.get('horario_saida', 'Horário de saída não disponível')
                qtd_aulas = aula.get('qtd_aulas', 'Quantidade não disponível')
                observacoes = aula.get('observacoes', 'Observações não disponíveis')

                # Obter o NIF do professor efetivo
                nif_efetivo = self.get_nif_professor_efetivo(prof_efetivo)

                self.table_aulas.setItem(row_position, 0, QtWidgets.QTableWidgetItem(prof_eventual))
                self.table_aulas.setItem(row_position, 1, QtWidgets.QTableWidgetItem(nif_efetivo))  # Exibir NIF
                self.table_aulas.setItem(row_position, 2, QtWidgets.QTableWidgetItem(prof_efetivo))
                self.table_aulas.setItem(row_position, 3, QtWidgets.QTableWidgetItem(dia_aula))
                self.table_aulas.setItem(row_position, 4, QtWidgets.QTableWidgetItem(horario_entrada))
                self.table_aulas.setItem(row_position, 5, QtWidgets.QTableWidgetItem(horario_saida))
                self.table_aulas.setItem(row_position, 6, QtWidgets.QTableWidgetItem(observacoes))
        else:
            QtWidgets.QMessageBox.information(self, 'Info', "Nenhum registro encontrado.")

        btn_fechar = QtWidgets.QPushButton('Fechar')
        btn_fechar.clicked.connect(self.window_listar_aulas.close)
        layout.addWidget(btn_fechar)

        self.window_listar_aulas.setLayout(layout)
        self.window_listar_aulas.exec_()

    def get_nif_professor_efetivo(self, nome_prof_efetivo):
        """Retorna o NIF do professor efetivo dado seu nome."""
        efetivos = efetivos_ref.get()
        if isinstance(efetivos, dict):
            for efetivo in efetivos.values():
                if efetivo['nome'] == nome_prof_efetivo:
                    return efetivo.get('nif', 'NIF não disponível')
        return 'NIF não encontrado'

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CadastroApp()
    window.show()
    sys.exit(app.exec_())
