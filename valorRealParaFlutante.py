# Feito por Nathan Gonçalves Rambalducci

# Essa função converte uma fração para binario
def binarioFracao(Fracao):

    binario = str()

    # Fazemos as multiplicações de 2 até chegamos em 0
    while (Fracao):
        
        Fracao *= 2

        # Pegamos os numeros 1 da fração e colocamos em uma variavel separada para não pifar o calculo.
        if (Fracao >= 1):
            partesInteiras = 1
            Fracao -= 1
        else:
            partesInteiras = 0
    
        # Colocamos essa variavel separada em na string binario para o valor final.
        binario += str(partesInteiras)
    
    return binario

# Função principal.
def pontoFlutuante(numeroInt):

    # Iniciando a variavel do bit de sinal
    bitSinal = 0

    # Se o numero for negativo, o bit sinal muda para representar que o numero é negativo 
    if(numeroInt < 0):
        bitSinal = 1

    # Convertendo o numero para seu valor absoluto já que temos o bit de sinal declarado.
    numeroInt = abs(numeroInt)

    # Convertendo a parte inteira de um numero para binaria.
    intStr = bin(int(numeroInt))[2 : ]

    # Chamamos a função anterior para converter a fração para binario.
    fracaoStr = binarioFracao(numeroInt - int(numeroInt))

    # Chamando esse index para casos aonde o bit é muito alto para representar o binario em um numero inteiro.
    ind = intStr.index('1')

    # Agora, declara o bit do expoente.
    bitExpoente = bin((len(intStr) - ind - 1) + 127)[2 : ]

    # e o da mantissa também
    bitMantisa = intStr[ind + 1 : ] + fracaoStr

    # Adicionando os zeros ausentes
    bitMantisa = bitMantisa + ('0' * (23 - len(bitMantisa)))

    return bitSinal, bitExpoente, bitMantisa

if __name__ == "__main__":

    valor = input("Numero decimal 1:") # Pegamos o input do usuário do primeiro numero aqui

    valorFloat1 = float(valor) # O numero está em string. Então, convertemos para float.

    # pega os bits de sinal, expoente e mantissa.
    bitSinal, bitExpoente, bitMantisa = pontoFlutuante(valorFloat1)

    ieee32Um = str(bitSinal) + '|' + bitExpoente + '|' + bitMantisa # Separando para ficar menos confuso (Sinal 1, Expoente 8, Mantinsa 23)

    valor = input("Numero decimal 2:") # Pegamos o input do usuário do segundo numero aqui

    valorFloat2 = float(valor) # Mesma coisa repidida

    bitSinal, bitExpoente, bitMantisa = pontoFlutuante(valorFloat2)

    ieee32Dois = str(bitSinal) + '|' + bitExpoente + '|' + bitMantisa 

    # Resultado final
    print(f"O resultado IEEE 754 de {valorFloat1} é :\n{ieee32Um}")

    print(f"O resultado IEEE 754 de {valorFloat2} é :\n{ieee32Dois}")