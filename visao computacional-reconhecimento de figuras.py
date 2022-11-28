# importando as bibliotecas
import cv2 # processa imagens
import pandas as pd # manipulação de dados
from easyocr import Reader # reconhecimento de textos em imagens

video = cv2.VideoCapture(1)


# variaveis dos textos que serão mostrados na tela
texto = ''
primeiro_nome = ''
ultimo_nome = ''
clube = ''
altura = ''
peso = ''
valor =''
idade = ''

# leitor ocr
redear = Reader(['en'])

#dados dos jogadores
df_fifa = pd.read_csv('FIFA23_official_data.csv')

# função que busca as estatisticas dos jogadores
def Busca_stats_jogador(primeiro_nome,ultimo_nome):
    nome_busca = f'{primeiro_nome[0]}. {ultimo_nome}'
    nome_busca = nome_busca.lower()

    linha_stats = df_fifa.loc[df_fifa['Name'].str.lower() == nome_busca,['Club','Height','Weight','Value','Age']]

    if len(linha_stats) == 0:
        nome_busca = f'{primeiro_nome} {ultimo_nome}'
        nome_busca = nome_busca.lower()
        linha_stats = df_fifa.loc[
            df_fifa['Name'].str.lower() == nome_busca, ['Club', 'Height', 'Weight', 'Value', 'Age']]

    estado_jogador = linha_stats.values[0]

    return estado_jogador

while True:
    ret, frame = video.read()

    # se pressionar 'd', realiza o OCR (reconhecimento de texto na imagem)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        resultados = redear.readtext(frame)
        texto = "TESTE"

        for resul in resultados:
            print(resul[1])
            if len(resul[1].split() == 2):
                primeiro_nome = resul[1].split()[0]
                ultimo_nome = resul[1].split()[1]

                texto = resul[1]

    # se pressionar 's', preenche os dados do jogador
    if cv2.waitKey(1) & 0xFF == ord('s'):
        try:
            print(f'nome {primeiro_nome} {ultimo_nome}')
            stats_str = Busca_stats_jogador(primeiro_nome,ultimo_nome)
            clube = f'CLUBE: {stats_str[0]}'
            altura = f'ALTURA: {stats_str[1]}'
            peso = f'PESO: {stats_str[2]}'
            valor = f'VALOR: {stats_str[3][1:]} DE EUROS'
            idade = f'IDADE: {stats_str[4]}'
        except Exception as e:
            print(e)

    # se pressionar 'a', apaga o nome e a estatistica dos jogadores
    if cv2.waitKey(1) & 0xFF == ord('a'):
        clube = ''
        altura = ''
        peso = ''
        valor = ''
        idade = ''

    # se pressionar 'q' sair do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.putText(frame,texto,(200,100),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.putText(frame,clube,(200,120),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.putText(frame,altura,(200,140),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.putText(frame,peso,(200,160),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.putText(frame,valor,(200,180),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.putText(frame,idade,(200,200),cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0),2)
    cv2.imshow('Frame',frame)



# fecha o objeto de video
video.release()

# fecha todas as janelas
cv2.destroyAllWindows()