# -*- coding: utf8


from selenium import webdriver

import click
import pandas as pd


def parse_turmas(form):
    turmas = {}
    for option in form.find_elements_by_tag_name('option'):
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
NOTAS = URL + 'notaTurma/notaAvaliacao/solicitar/solicitarNota.do?acao=lancarAvaliacaoCompleta'


@click.command()
@click.option('--usuario', prompt='Digite seu login')
@click.option('--senha', prompt='Digite sua senha',
              confirmation_prompt=True, hide_input=True)
@click.argument('arquivo_notas')
def main(usuario, senha, arquivo_notas):

    # Pouco de programacao defensiva
    print('Lendo o arquivo')
    try:
        # Lendo como string, mais seguro
        df = pd.read_csv(arquivo_notas, header=0, index_col=-1, dtype=str)
        df['Matricula'] = pd.to_numeric(df['Matricula'])
        df = df.set_index('Matricula').fillna('0')
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
    username = driver.find_element_by_id('j_username')
    password = driver.find_element_by_id('j_password')

    username.send_keys(usuario)
    password.send_keys(senha)
    driver.find_element_by_name('submit').click()

    # Form de turmas
    form_turma = driver.find_element_by_name('turma')
    turmas = parse_turmas(form_turma)
    escolha_turma = pega_turma(turmas)
    escolha_turma.click()

    # Vamos para as notas
    driver.get(NOTAS)

    # Desliga as notificacoes do minha ufmg
    print('Destivando e-mails')
    notificacoes = "//input[@type='checkbox' and @checked='checked']"
    for checkbox in driver.find_elements_by_xpath(notificacoes):
        checkbox.click()

    # Pega os nomes das provas
    avaliacoes_header = driver.find_element_by_xpath("//div[@id='notasHead']")
    avaliacoes = []
    for avaliacao in avaliacoes_header.find_elements_by_tag_name('a'):
        avaliacoes.append(avaliacao.text)

    print('As avaliacoes sao:')
    for i in range(len(avaliacoes)):
        print(avaliacoes[i])

    # YOLO
    print('Caso as colunas existam no csv, here we go...')
    cells = '//input[@class="nota centralizado widthAval"]'
    for cell in driver.find_elements_by_xpath(cells):
        cell.click()
        id_ = cell.get_attribute('id')[1:]
        matricula, idx_aval = map(int, id_.split('_'))
        nota = df.loc[matricula][avaliacoes[idx_aval]]
        cell.send_keys(nota.replace('.', ','))

    driver.close()


if __name__ == '__main__':
    main()
