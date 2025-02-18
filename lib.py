import os, csv
import numpy as np
from gdown import download

# Definir a função download_from_drive
def download_dataset(link,filename):
    # Criar a pasta para download
    foldername = filename.split('/')[0]
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    else:
        print(f'A pasta {foldername} já existe!')

    # Extrair o ID do arquivo a partir do link do Google Drive
    file_id = link.split('/')[5]
    # Criar a URL de download usando o ID do arquivo
    url = f'https://drive.google.com/uc?id={file_id}'
    download(url, filename, quiet = False)

    return None

#-------------------------------------------------------------------

def preencher_matriz_contratos(nome_arquivo: str):

    # Abrir o arquivo em modo de leitura
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        # << DEBUG >> Exibir as linhas uma por uma no console
        #for linha in linhas:
        #    print(linha.strip())  # `strip()` remove espaços em branco nas extremidades da linha

    # Le a primeira linha e armazenar as variáveis
    primeira_linha = linhas[0]
    # << DEBUG >> print(primeira_linha)

    # Remover a primeira linha (não será usada para a matriz)
    linhas_restantes = linhas[1:]

    #Cria as matrizes
    Fornecedor_cleaned = []
    Max_Month = []
    Month = []
    
    #Código para definir quantos fornecedores diferentes existem no dataSet
    for linha in linhas_restantes:
    # Separar os valores da linha, convertendo para inteiros e float
        dados = linha.strip().split()
        Fornecedor = int(dados[0])
        Fornecedor_cleaned.append(Fornecedor)

    #Realiza a verficação do maior valor do mês final
        month_list= int(dados[2])
        Month.append(month_list)


    Max_Month = np.max(Month) #pega o maior valor do mês
    # << DEBUG >> print(f"Número Máximo de Mês Final: {Max_Month}")
    

    #verifica quantos fornecedores distintos o dataset possui
    Fornecedor_cleaned = np.array(list(set(Fornecedor_cleaned))) #Remove os IDs dos fornecedores repetidos
    Numero_de_fornecedores = Fornecedor_cleaned.size
    # << DEBUG >> print(f"Número de fornecedores: {Numero_de_fornecedores}")

    # Inicializar a matriz de contratos
    matriz_Fornecedor = []
    matriz_Inicio_Contrato = []
    matriz_Termino_Contrato = []
    #Baseado na quantidade de fornecedores, e mês final é definido o tamanho da matriz
    matriz = np.full((Numero_de_fornecedores, Max_Month+1, Max_Month+1), float('inf'))
    # << DEBUG >> print(matriz)

    # << DEBUG >> print(f"Número de dimensões {matriz.ndim}")
    # << DEBUG >> print(f"Formato da Matriz {matriz.shape}")
    # << DEBUG >> print(f"Tamanho da matriz {matriz.size}")

    Matriz_Modificada = []
    
    # Ler os dados restantes e armazenar os valores de contrato
    for linha in linhas_restantes:
        dados = linha.strip().split()
        
        Fornecedor = int(dados[0]) #Identifica o fornecedor atual
        Fornecedor = Fornecedor - 1 #subtrai 1 do índice do fornecedor ao preencher a matriz para manter a indexação correta em zero
        Inicio_Contrato = int(dados[1]) #Identifica o mês de inicio
        Termino_Contrato = int(dados[2]) #Identifica o mês final
        Valor_contrato = float(dados[3]) #identifica o valor do contrato

        #Atribui os valores na Matriz 
        matriz[Fornecedor, Inicio_Contrato, Termino_Contrato] = Valor_contrato

    m = Inicio_Contrato
    t = Termino_Contrato
    n = Fornecedor + 1
    
    return m, n, t, matriz     

def imprimir_matriz(matriz, k=None):

    print(matriz)

    return None





def exportar_csv(nome_arquivo, matriz):

    # Função para exportar a matriz de contratos
    import csv
    output_file = nome_arquivo

    with open(output_file, 'w', newline='') as csvfile: #Abre o Arquivo de saída
        
        csv_writer = csv.writer(csvfile, delimiter=',') #Cria um objeto de escrita

        for row in matriz: #loops through rows of matrix
            csv_writer.writerow(row) #writes row to csv file

    print(f"Arquivo salvo como:  {output_file}")

    return None