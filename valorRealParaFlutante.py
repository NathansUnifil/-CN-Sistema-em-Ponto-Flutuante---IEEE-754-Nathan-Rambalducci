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

# Reverte os valores já convertidos para ieee754 para de volta para float para eu ganhar a nota maxima nessa atividade.
def ieeeParaFloat(sinal, expoente, mantissa):
    if expoente == '0' * 8 and mantissa == '0' * 23:
        return 0.0 if sinal == 0 else -0.0
    
    # O expoente é convertido
    expInt = int(expoente, 2) - 127
    
    # A mantissa é convertida
    mantVal = 1.0  
    for i, bit in enumerate(mantissa):
        if bit == '1':
            mantVal += 2 ** (-(i + 1))
    
    # Valor final
    valor = mantVal * (2 ** expInt)
    return -valor if sinal == 1 else valor

# Faz a soma dos dois valores do input do programa
def adicionaIeee754(s1, e1, m1, s2, e2, m2):
    
    # Converte os valores para floats
    num1 = ieeeParaFloat(s1, e1, m1)
    num2 = ieeeParaFloat(s2, e2, m2)
    
    # faz a soma
    resultado = num1 + num2
    
    # Converte resultado de volta para ieee 754
    return pontoFlutuante(resultado)


if __name__ == "__main__":

    valor1 = input("Numero decimal 1:") # Pegamos o input do usuário do primeiro numero aqui

    valorFloat1 = float(valor1) # O numero está em string. Então, convertemos para float.

    # pega os bits de sinal, expoente e mantissa.
    bitSinal1, bitExpoente1, bitMantisa1 = pontoFlutuante(valorFloat1)

    ieee32Um = str(bitSinal1) + '|' + bitExpoente1 + '|' + bitMantisa1 # Separando para ficar menos confuso (Sinal 1, Expoente 8, Mantinsa 23)

    valor2 = input("Numero decimal 2:") # Pegamos o input do usuário do segundo numero aqui

    valorFloat2 = float(valor2) # Mesma coisa repidida

    bitSinal2, bitExpoente2, bitMantisa2 = pontoFlutuante(valorFloat2)

    ieee32Dois = str(bitSinal2) + '|' + bitExpoente2 + '|' + bitMantisa2 

    # a adição dos dois valores começa aqui
    sinalSoma, expoenteSoma, mantissaSoma = adicionaIeee754(
        bitSinal1, bitExpoente1, bitMantisa1,
        bitSinal2, bitExpoente2, bitMantisa2
    )
    
    ieee32Soma = str(sinalSoma) + '|' + expoenteSoma + '|' + mantissaSoma
    valorSoma = ieeeParaFloat(sinalSoma, expoenteSoma, mantissaSoma)

    # Resultado final
    print(f"O resultado IEEE 754 de {valorFloat1} é :\n{ieee32Um}")

    print(f"O resultado IEEE 754 de {valorFloat2} é :\n{ieee32Dois}")

    print(f"A soma desses dois valores {valorFloat1} | {valorFloat2} no decimal da {valorSoma} e no IEEE 754 da {ieee32Soma}")