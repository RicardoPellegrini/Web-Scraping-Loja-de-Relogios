import requests
from bs4 import BeautifulSoup


# Página inicial do catálogo de relógios
url = 'https://mrjoias.com.br/loja/12-relogios?p=1'

# Fazendo parsing da página html
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Descobrindo o número total de itens para inserir nos query params
contagem = soup.find('span', class_="heading-counter").text.split()
max_items = [int(palavra) for palavra in contagem if palavra.isdigit()]

# Padronização das marcas, já que não há um campo específico de marca nas tags
marcas = {
  'BAUME': 'BAUME ET MERCIER',
  'MERCEDES': 'MERCEDES-BENZ',
  'JAEGER': 'JAEGER LECOULTRE',
  'VACHERON': 'VACHERON CONSTANTIN',
  'RALF': 'RALF TECH',
  'BELL': 'BELL & ROSS',
  'PORSCHE': 'PORSCHE DESIGN',
  'FREDERIQUE': 'FREDERIQUE CONSTANT',
  'LOUIS': 'LOUIS VUITTON',
  'GIRARD': 'GIRARD PERREGAUX',
  'PATEK': 'PATEK PHILIPPE',
  'TAG': 'TAG HEUER'
  }

# Criação do arquivo csv para preenchimento dos dados obtidos
filename = "watches.csv"
file = open(filename, 'w')
headers = 'marca,modelo,preço,disponibilidade\n'
file.write(headers)

# Percorrer a página 'mostrar todos'
updated_url = f'https://mrjoias.com.br/loja/12-relogios?id_category=12&n={max_items[0]}'
response = requests.get(updated_url)
soup = BeautifulSoup(response.content, 'html.parser')
relogios = soup.find_all('div', class_="product-container")

# Percorrer todos os relógios disponíveis na página
for relogio in relogios:
  # Marca
  marca = relogio.find('a', class_="product-name")['title'].strip().split(' ')[0]
  # Normalizando a marca através do dicionário
  if marca in marcas.keys():
    marca = marcas[marca]

  # Modelo
  modelo = relogio.find('a', class_="product-name")['title'].strip()

  # Preço
  preco = relogio.find('span', class_="price product-price").text.strip().split(',')[0]

  # Disponibilidade
  disponibilidade = relogio.find('span', class_="availability").span.text.strip()

  # Escreve os dados encontrados na linha do arquivo
  file.write(marca + ',' + modelo + ',' + preco + ',' + disponibilidade + '\n')

# Fecha o arquivo csv
file.close()

