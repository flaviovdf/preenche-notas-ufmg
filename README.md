# Preenche notas Minha-UFMG

Script que preenche as notas automagicamente. Precisa de Selenium + GeckoDriver para funcionar.

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

```
Matricula,AV1,AV2,AV3,AV4,EE
```

## Executando

Sempre mantenha um terminal aberto. O mesmo vai perguntar para você qual é a turma, veja o vídeo abaixo.

<iframe width="560" height="315"
src="https://www.youtube.com/embed/Z7yhH-4r8YI" 
frameborder="0" 
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen>
</iframe>
