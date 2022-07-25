# -*- coding: utf8


from selenium import webdriver
from selenium.webdriver.common.by import By

import click
import pandas as pd


def parse_turmas(form):
    turmas = {}
    for option in form.find_elements(By.TAG_NAME, 'option'):
        if 'Selecione' in option.text:
            continue
        turmas[option.text] = option
    return turmas


def pega_turma(turmas):
    while True:
        print()
        escolha_idx = print('Escolha uma turma:')
        escolhas = {}
        for i, turma in enumerate(sorted(turmas)):
            escolhas[str(i)] = turma
            print(i, ':', turma, sep='\t')

        escolha_idx = input()
        if escolha_idx not in escolhas:
            print('Turma inválida!')
        else:
            break

    nome_turma = escolhas[escolha_idx]
    valor_form = turmas[nome_turma]
    return valor_form


URL = 'https://sistemas.ufmg.br/diario/'
NOTAS = URL +\
    'notaTurma/notaAvaliacao/solicitar/solicitarNota.do' +\
    '?acao=lancarAvaliacaoCompleta'


@click.command()
@click.option('--usuario', prompt='Digite seu login')
@click.option('--senha', prompt='Digite sua senha',
              hide_input=True)
@click.argument('arquivo_notas')
def main(usuario, senha, arquivo_notas):

    # Pouco de programacao defensiva
    print('Lendo o arquivo')
    try:
        # Lendo como string, mais seguro
        df = pd.read_csv(
            arquivo_notas,
            header=0, index_col=None, dtype=str
        )
        df['Matricula'] = pd.to_numeric(df['Matricula'])
        df = df.set_index('Matricula')
        df = df.sort_index()
        df = df.fillna('0')
    except Exception as e:
        print('Arquivo no formato errado.')
        print('Preciso de csv com uma coluna Matricula')
        print('Além de uma coluna por avaliacao estilo minha ufmg AV1,AV2,EE')
        raise e

    # Inicia selenium
    print('Iniciando selenium')
    driver = webdriver.Firefox()
    driver.get(URL)

    # Logando
    username = driver.find_element(By.ID, 'j_username')
    password = driver.find_element(By.ID, 'j_password')

    username.send_keys(usuario)
    password.send_keys(senha)
    driver.find_element(By.NAME, 'submit').click()

    # Form de turmas
    form_turma = driver.find_element(By.NAME, 'turma')
    turmas = parse_turmas(form_turma)
    escolha_turma = pega_turma(turmas)
    escolha_turma.click()

    # Vamos para as notas
    driver.get(NOTAS)

    # Desliga as notificacoes do minha ufmg
    print('Destivando e-mails')
    notificacoes = "//input[@type='checkbox' and @checked='checked']"
    for checkbox in driver.find_elements(By.XPATH,
                                         notificacoes):
        checkbox.click()

    # Pega os nomes das provas
    avaliacoes_header = driver.find_element(By.XPATH,
                                            "//div[@id='notasHead']")
    avaliacoes = []
    for avaliacao in avaliacoes_header.find_elements(By.TAG_NAME, 'a'):
        avaliacoes.append(avaliacao.text)

    print('As avaliacoes sao:')
    for i in range(len(avaliacoes)):
        print(avaliacoes[i])

    # YOLO
    print('Caso as colunas existam no csv, here we go...')
    cells = '//input[@class="nota centralizado widthAval"]'
    cols = set(df.columns)
    idx_aval = 0
    for cell in driver.find_elements(By.XPATH, cells):
        cell.click()
        id_ = cell.get_attribute('id')[1:]
        matricula, _ = map(int, id_.split('_'))
        if avaliacoes[idx_aval] in cols and matricula in df.index:
            nota = df.loc[matricula][avaliacoes[idx_aval]]
            cell.send_keys(nota.replace('.', ','))
        idx_aval = (idx_aval + 1) % len(avaliacoes)

    print('Antes de fechar o script, ', end='')
    print('verifique tudo e salve as notas no browser.')
    print('Depois, digite qq coisa aqui para terminar')
    input()
    try:
        driver.close()
    except Exception:
        pass


if __name__ == '__main__':
    main()
