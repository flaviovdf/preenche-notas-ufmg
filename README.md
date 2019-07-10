# Preenche notas Minha-UFMG

Script que preenche as notas automagicamente. Precisa de Selenium + GeckoDriver para funcionar.

Como: 1) sou péssimo em manter consistência; e, 2) às vezes tenho turmas quebradas; com o script preciso apenas criar uma planilha e "importar" no sistema depois.

## Instalando o Selenium

```bash
pip install selenium
```

## Instalando o GeckoDriver

Execute as linhas abaixo como root. Caso prefira, mude os comandos para instalar em um outro local.

```bash
LATEST=`wget -O - https://github.com/mozilla/geckodriver/releases/latest 2>&1 | grep "Location:" | grep --only-match -e "v[0-9\.]\+"`
wget "https://github.com/mozilla/geckodriver/releases/download/${LATEST}/geckodriver-${LATEST}-linux64.tar.gz"
tar -x geckodriver -zf geckodriver-${LATEST}-linux64.tar.gz -O > /usr/local/bin/geckodriver
chmod +x /usr/local/bin/geckodriver
```

## Formato

Como entrada, basta passar um csv que contenha no cabeçalho. Qualquer coluna que não seja `AV#` ou `EE` será ignorada.

**A ideia aqui é que o: excell, google-sheets, \*-office, todos permitem salvar planilhas como csv**

```
Matricula,AV1,AV2,AV3,AV4,EE
```

## Executando

Sempre mantenha um terminal aberto. O mesmo vai perguntar para você qual é a turma, veja o vídeo abaixo.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Z7yhH-4r8YI/0.jpg)](https://www.youtube.com/watch?v=Z7yhH-4r8YI)
