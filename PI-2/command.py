import os
def help():
    string = "Sou o QIsso! Um bot de reconhecimento de imagens de satélite trabalhando com as seguintes classificações:"
    for label in os.listdir(f"{os.getcwd()}/classificador/train"):
        string += f"\n\t\t**- {label}**"
    
    string += "\n\n***Comandos***\n\n**!help**: exibe as classificações que o modelo de predição utiliza e os comandos disponíveis.\n**!predict**(img):recebe uma imagem como parâmetro e devolve a classificação dela."

    return string