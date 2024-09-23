!pip install xmltodict

import pprint
import json
import requests
import xmltodict

#--------------
#FUNÇÕES COMUNS
#--------------

def get_url(area):
  api_key = "1737636254"
  api_pass = "cf334dde-eb8c-11ee-8b18-0050569ac2e1"
  tipo = "AD"

  if area == "met":
    icao_code = input("Informe o código ICAO desejado: ")
    url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=met&icaoCode={icao_code}"
  elif area == "rotaer":
    icao_code = input("Informe o código ICAO desejado: ")
    url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=rotaer&icaoCode={icao_code}"
  elif area == "geiloc":
    cidade = input("Informe a cidade desejada: ")
    url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=rotaer&city={cidade}&type={tipo}"
  elif area == "sol":
    icao_code = input("Informe o código ICAO desejado: ")
    url = f"http://aisweb.decea.gov.br/api/?apiKey={api_key}&apiPass={api_pass}&area=sol&icaoCode={icao_code}"

  return url

def make_request(url):
  response = requests.get(url)

  return response

def xml_to_dict(response):
  json_response = xmltodict.parse(response.content)

  return json_response

#------
#GEILOC
#------

def get_data_geiloc(json_response):

  total_aeroportos = int(json_response.get('aisweb').get('rotaer').get('@total'))

  if total_aeroportos == 1:
    cidade = json_response.get('aisweb').get('rotaer').get('item').get('city')
    aeroporto = json_response.get('aisweb').get('rotaer').get('item')
    print(f"\n\nA cidade de {cidade} tem os seguinte aeroporto:\n")
    print(f"Aerodromo 1\nNome: {aeroporto.get('name')}\nCódigo ICAO: {aeroporto.get('AeroCode')}\n")

  else:
    cidade = json_response.get('aisweb').get('rotaer').get('item')[0].get('city')
    lista_aeroportos = json_response.get('aisweb').get('rotaer').get('item')
    numero = 1
    print(f"\n\nA cidade de {cidade} tem os seguintes aeroportos:\n")

    for aeroporto in lista_aeroportos:
      print(f"Aerodromo {numero}\nNome: {aeroporto.get('name')}\nCódigo ICAO: {aeroporto.get('AeroCode')}\n")
      numero +=1

def geiloc():
  area = "geiloc"
  url = get_url(area)
  response = make_request(url)
  json_response = xml_to_dict(response)
  get_data_geiloc(json_response)

#-----
#METAR
#-----

def get_data_metar(json_response):
  metar = json_response.get('aisweb').get('met').get('metar')

  data = metar.split()

  return data

def get_icao_code_metar(json_response):
  icao_code = json_response.get('aisweb').get('met').get('loc')

  return icao_code

def get_time_metar(data):
  obs_time = f"{int(data[2][2:4])-3}:{data[2][4:6]}"

  return obs_time

def get_wind_metar(data):
  wind = int(data[3][0:3])
  wind_speed = data[3][3:5]

  if wind >=316 or wind <=45:
    wind_dir = "Norte"
  elif wind >=46 and wind <= 135:
    wind_dir = "Leste"
  elif wind >=136 and wind <=225:
    wind_dir = "Sul"
  elif wind >=226 and wind <=315:
    wind_dir = "Oeste"

  result = f"Vento de {wind_dir} com {wind_speed} nós"

  return result

def get_temperature_metar(data):
  temperature = f"{data[-2][0:2]}º C"

  return temperature

def get_pressure_metar(data):
  pressure = f"{data[-1][1:5]} hPa"

  return pressure

def get_result_metar(json_response, data):
  codigo_icao = get_icao_code_metar(json_response)
  horario_observacao = get_time_metar(data)
  vento = get_wind_metar(data)
  temperatura = get_temperature_metar(data)
  pressao = get_pressure_metar(data)
  print(f"\nCódigo ICAO: {codigo_icao}\nHorário da Observação: {horario_observacao}\nVento: {vento}\nTemperatura: {temperatura}\nPressão:{pressao}")

def metar():
  area = "met"
  url = get_url(area)
  response = make_request(url)
  json_response = xml_to_dict(response)
  data = get_data_metar(json_response)
  get_result_metar(json_response, data)

#------
#ROTAER
#------

def get_data_rotaer(json_response):
  data = json_response.get('aisweb')

  return data

def get_name_rotaer(data):
  nome = data.get('name')

  return nome

def get_icao_code_rotaer(data):
  codigo_icao = data.get('AeroCode')

  return codigo_icao

def get_city_rotaer(data):
  cidade = data.get('city')

  return cidade

def get_aero_type_rotaer(data):
  tipo_aerodromo = data.get('org').get('military').title()

  return tipo_aerodromo

def get_alt_ft_rotaer(data):
  alt_ft = data.get('altFt')

  formated_alt_ft = f"{alt_ft}ft"

  return formated_alt_ft

def get_alt_mt_rotaer(data):
  alt_mt = data.get('altM')

  formated_alt_mt = f"{alt_mt} mts"

  return formated_alt_mt

def get_fir_rotaer(data):
  fir = data.get('fir')

  if fir == "SBCW":
    formated_fir = "SBCW - Centro Curitiba"
  elif fir == "SBBS":
    formated_fir = "SBBS - Centro Brasília"
  elif fir == "SBRE":
    formated_fir = "SBRE - Centro Recife"
  else:
    formated_fir = "SBAZ - Centro Amazônico"

  return formated_fir

def get_rwy_thr_rotaer(data):
  rwy_qty = int(data.get('runways').get('@count'))

  if rwy_qty == 1:
    rwy_thr = data.get('runways').get('runway').get('ident')

    return rwy_thr

  else:
    rwys = []

    for rwy in data.get('runways').get('runway'):
      rwy_thr = rwy.get('ident')
      rwys.append(rwy_thr)

    return rwys

def get_rwy_dimensions_rotaer(data):
  rwy_qty = int(data.get('runways').get('@count'))

  if rwy_qty == 1:
    rwy_width = f"{data.get('runways').get('runway').get('width').get('#text')}"
    rwy_length = f"{data.get('runways').get('runway').get('length').get('#text')}"

    rwy_dimension = f"{rwy_length} x {rwy_width} metros"

    return rwy_dimension

  else:
    rwy_widths = []
    rwy_lengths = []

    for rwy in data.get('runways').get('runway'):
      width = rwy.get('width').get('#text')
      rwy_widths.append(width)

    for rwy in data.get('runways').get('runway'):
      length = rwy.get('length').get('#text')
      rwy_lengths.append(length)

    rwy_dimensions = []

    index = 0

    for i in range(len(rwy_widths)):
      rwy_dimensions.append(f"{rwy_lengths[index]} x {rwy_widths[index]} metros")
      index += 1

    return rwy_dimensions

def get_result_rotaer(nome, codigo_icao, cidade, tipo_aerodromo, elevacao_ft, elevacao_mt, fir, pista, dimensoes_pista):

  print(f"\nNome: {nome}\nCódigo ICAO: {codigo_icao}\nCidade: {cidade}\nTipo de Aeródromo: {tipo_aerodromo}\nElevação: {elevacao_ft} ({elevacao_mt})\nFIR: {fir}")

  if type(pista) == list:
    print("Pistas: ")
    for rwy in pista:
      print(f"      - {rwy}")
  else:
    print(f"Pista:")
    print(f"      - {pista}")

  if type(dimensoes_pista) == list:
    print("Dimensões das pistas: ")
    for dimensao in dimensoes_pista:
      print(f"      - {dimensao}")
  else:
    print(f"Dimensões da pista: ")
    print(f"      - {dimensoes_pista}")

def rotaer():
  area = "rotaer"
  url = get_url(area)
  response = make_request(url)
  json_response = xml_to_dict(response)
  data = get_data_rotaer(json_response)
  nome = get_name_rotaer(data)
  codigo_icao = get_icao_code_rotaer(data)
  cidade = get_city_rotaer(data)
  tipo_aerodromo = get_aero_type_rotaer(data).title()
  elevacao_ft = get_alt_ft_rotaer(data)
  elevacao_mt = get_alt_mt_rotaer(data)
  fir = get_fir_rotaer(data)
  pista = get_rwy_thr_rotaer(data)
  dimensoes_pista = get_rwy_dimensions_rotaer(data)
  get_result_rotaer(nome, codigo_icao, cidade, tipo_aerodromo, elevacao_ft, elevacao_mt, fir, pista, dimensoes_pista)

#---
#SOL
#---

def get_icao_code_sol(json_response):
  icao_code = json_response.get('aisweb').get('day').get('aero')

  return icao_code

def get_date_sol(json_response):
  date = json_response.get('aisweb').get('day').get('date')

  data = date.split("-")
  day = data[2]
  month = data[1]
  year = data[0]

  formated_date = f"{day}/{month}/{year}"

  return formated_date

def get_sunrise_sol(json_response):
  sunrise = json_response.get('aisweb').get('day').get('sunrise')

  hour_sunrise = int(sunrise[0:2])-3

  sunrise_time = f"{hour_sunrise}:{sunrise[3:]}"

  return sunrise_time

def get_sunset_sol(json_response):
  sunset = json_response.get('aisweb').get('day').get('sunset')

  hour_sunset = int(sunset[0:2])-3

  sunset_time = f"{hour_sunset}:{sunset[3:]}"

  return sunset_time

def get_result_sol(icao_code, date, sunrise, sunset):
  print(f"\nPara {icao_code.upper()}, no dia {date}, o nascer do Sol acontecerá às {sunrise} e o pôr do Sol, às {sunset}.")

def sol():
  area = "sol"
  url = get_url(area)
  response = make_request(url)
  json_response = xml_to_dict(response)
  icao_code = get_icao_code_sol(json_response)
  data_observacao = get_date_sol(json_response)
  nascer_do_sol = get_sunrise_sol(json_response)
  por_do_sol = get_sunset_sol(json_response)
  get_result_sol(icao_code, data_observacao, nascer_do_sol, por_do_sol)

#----------------
#FUNÇÃO PRINCIPAL
#----------------

def main():

  print("===========================")
  print("Bem vindo ao Aviators Atlas")
  print("===========================\n")

  while True:
    print("\n========== MENU ===========\n")
    print("1 - GEILOC")
    print("2 - METAR")
    print("3 - ROTAER")
    print("4 - SOL")
    print("5 - SAIR")

    opcao = int(input("\nSua opção: \n"))

    if opcao == 1:
      geiloc()
    elif opcao == 2:
      metar()
    elif opcao == 3:
      rotaer()
    elif opcao == 4:
      sol()
    elif opcao == 5:
      print("\nAté mais!")
      break

#--------------------------------------------------------------------------------------------------------
main()
