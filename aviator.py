#GEILOC
def get_url():
  api_key = "1737636254"
  api_pass = "cf334dde-eb8c-11ee-8b18-0050569ac2e1"
  icao_code = input("Informe o código ICAO desejado: ")

  url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=met&icaoCode={icao_code}"

  return url

def make_request(url):
  response = requests.get(url)

  return response

def xml_to_dict(resposta):
  resposta_json = xmltodict.parse(resposta)

  return resposta_json

def resultado(resposta_json):

  total_aeroportos = int(resposta_json.get('aisweb').get('rotaer').get('@total'))

  if total_aeroportos == 1:
    cidade = resposta_json.get('aisweb').get('rotaer').get('item').get('city')

    aeroporto = resposta_json.get('aisweb').get('rotaer').get('item')

    print(f"\n\nA cidade de {cidade} tem os seguinte aeroporto:\n")

    print(f"Aerodromo 1\nNome: {aeroporto.get('name')}\nCódigo ICAO: {aeroporto.get('AeroCode')}\n")

  else:

    cidade = resposta_json.get('aisweb').get('rotaer').get('item')[0].get('city')

    lista_aeroportos = resposta_json.get('aisweb').get('rotaer').get('item')

    numero = 1

    print(f"\n\nA cidade de {cidade} tem os seguintes aeroportos:\n")

    for aeroporto in lista_aeroportos:
      print(f"Aerodromo {numero}\nNome: {aeroporto.get('name')}\nCódigo ICAO: {aeroporto.get('AeroCode')}\n")
      numero +=1

def geiloc():
  resposta = requisicao()
  resposta_json = xml_to_dict(resposta)
  resultado(resposta_json)

#METAR
def metar_to_list_metar(resposta_json):
  metar = resposta_json.get('aisweb').get('met').get('metar')

  lista_metar = metar.split()

  return lista_metar

def icao_code_metar(resposta_json):
  codigo_icao = resposta_json.get('aisweb').get('met').get('loc')

  return codigo_icao

def get_horario_metar(lista_metar):
  horario_observacao = f"{int(lista_metar[2][2:4])-3}:{lista_metar[2][4:6]}"

  return horario_observacao

def get_vento_metar(lista_metar):
 vento = int(lista_metar[3][0:3])
 velocidade_do_vento = lista_metar[3][3:5]


 if vento >=316 or vento <=45:
   direcao_vento = "Norte"
 elif vento >=46 and vento <= 135:
   direcao_vento = "Leste"
 elif vento >=136 and vento <=225:
   direcao_vento = "Sul"
 elif vento >=226 and vento <=315:
   direcao_vento = "Oeste"


 result = f"Vento de {direcao_vento} com {velocidade_do_vento} nós"


 return result
 return vento

def get_temperatura_metar(lista_metar):
  temperatura = f"{lista_metar[-2][0:2]}º C"

  return temperatura

def get_pressao_metar(lista_metar):
  pressao = f"{lista_metar[-1][1:5]} hPa"

  return pressao

def resultado_metar(resposta_json, lista_metar):
  codigo_icao = icao_code_metar(resposta_json)
  horario_observacao = get_horario_metar(lista_metar)
  vento = get_vento_metar(lista_metar)
  temperatura = get_temperatura_metar(lista_metar)
  pressao = get_pressao_metar(lista_metar)
  print(f"\nCódigo ICAO: {codigo_icao}\nHorário da Observação: {horario_observacao}\nVento: {vento}\nTemperatura:{temperatura}\nPressão:{pressao}")

def metar():
  resposta = requisicao()
  resposta_json = xml_to_dict(resposta)
  lista_metar = metar_to_list_metar(resposta_json)
  resultado_metar(resposta_json, lista_metar)

#ROTAER
def obter_informacoes_aerodromo(api_key, api_pass, rotaer_icao_code):
    url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=rotaer&icaoCode={rotaer_icao_code}"

    resposta = requests.get(url)
    resposta_dict = xmltodict.parse(resposta.content)

    nome = resposta_dict.get('aisweb').get('name')
    print(f"Nome do aerodromo: {nome}")

    codigo_icao = resposta_dict.get('aisweb').get('AeroCode')
    print(f"Codigo ICAO: {codigo_icao}")

    local = resposta_dict.get('aisweb').get('city')
    print(f"Cidade do aerodromo: {local}")

    tipo_de_aerodromo = resposta_dict.get('aisweb').get('org').get('military')
    if tipo_de_aerodromo != 'CIVIL':
      print(f"Tipo de aerodromo: {tipo_de_aerodromo}")
    else:
      print(f"Não existe tipo.")

    elevacao = resposta_dict.get('aisweb').get('altFt')
    print(f"Elevação em pés: {elevacao} pés")

    fir = resposta_dict.get('aisweb').get('fir')
    print(f"Codigo ICAO da FIR: {fir}")

    pista = resposta_dict.get('aisweb').get('runways').get('runway').get('ident')
    print(f"Designativo das cabeceiras da pista: {pista}")

    dimensoes_da_pista_metros = resposta_dict.get('aisweb').get('runways').get('runway').get('length').get('#text')
    dimensoes_da_pista_largura = resposta_dict.get('aisweb').get('runways').get('runway').get('width').get('#text')
    print(f"A pista possui o comprimento de {dimensoes_da_pista_metros} metros e {dimensoes_da_pista_largura} de largura.")

def rotaer():
    api_key = "1737636254"
    api_pass = "cf334dde-eb8c-11ee-8b18-0050569ac2e1"

    while True:
        rotaer_icao_code = input("\nDigite o código ICAO da localidade do aeródromo que deseja: ")
        obter_informacoes_aerodromo(api_key, api_pass, rotaer_icao_code)

        repetir = input("\nDeseja fazer outra requisição? (s/n): ").strip().lower()
        if repetir != 's':
            print("Obrigado por usar o sistema. Até logo!")
            break

#SOL
def json_response(resposta):
  json_response = xmltodict.parse(resposta.content)

  return json_response

def get_icao_code(json_response):
  icao_code = json_response.get('aisweb').get('day').get('aero')

  return icao_code

def get_date(json_response):
  date = json_response.get('aisweb').get('day').get('date')

  data = date.split("-")
  day = data[2]
  month = data[1]
  year = data[0]

  formated_date = f"{day}/{month}/{year}"
  return formated_date

def get_sunrise(json_response):
  sunrise = json_response.get('aisweb').get('day').get('sunrise')

  hour_sunrise = int(sunrise[0:2])-3

  sunrise_time = f"{hour_sunrise}.{sunrise[3:]}"

  return sunrise_time

def get_sunset(json_response):
  sunset = json_response.get('aisweb').get('day').get('sunset')

  hour_sunset = int(sunset[0:2])-3

  sunset_time = f"{hour_sunset}.{sunset[3:]}"

  return sunset_time

def get_result(icao_code, date, sunrise, sunset):
  print(f"\nPara {icao_code.upper()}, no dia {date}, o nascer do Sol acontecerá ás {sunrise} e o pôr do sol, ás {sunset}.")

def sol():
  dados = make_request()
  dados_json = json_response(dados)
  icao_code = get_icao_code(dados_json)
  data_observacao = get_date(dados_json)
  nascer_do_sol = get_sunrise(dados_json)
  por_do_sol = get_sunset(dados_json)
  get_result(icao_code, data_observacao, nascer_do_sol, por_do_sol)

def main():

  print("===========================================")
  print("=======BEM VINDO AO Aviators Atlas=========")
  print("===========================================\n\n")
  print("==================MENU=====================")
  print("1 - GEILOC")
  print("2 - METAR")
  print("3 - ROTAER")
  print("4 - SOL")
  print("5 - SAIR")

  opcao = int(input("Sua opção: "))

  if opcao == 1:
    geiloc()
  elif opcap == 2:
    metar()
  elif opcao == 3:
    rotaer()
  elif opcao == 4:
    sol()


