def boasVindas():
    print("Bem-vindo ao sistema de consumo de API e interpretação de dados de aeródromos!")
    print("""
       __|__    
--o--o--(_)--o--o--
    """)
    print("Estamos prontos para ajudar a encontrar as informações que você precisa.\n")

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

def main():
    api_key = "1737636254"
    api_pass = "cf334dde-eb8c-11ee-8b18-0050569ac2e1"
    boasVindas()

    while True:
        rotaer_icao_code = input("\nDigite o código ICAO da localidade do aeródromo que deseja: ")
        obter_informacoes_aerodromo(api_key, api_pass, rotaer_icao_code)

        repetir = input("\nDeseja fazer outra requisição? (s/n): ").strip().lower()
        if repetir != 's':
            print("Obrigado por usar o sistema. Até logo!")
            break
