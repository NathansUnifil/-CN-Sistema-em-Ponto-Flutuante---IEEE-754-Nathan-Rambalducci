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

    print("\nComparação usando as operações da linguagem normal")
    print(f"{valorFloat1} + {valorFloat2}: {valorFloat1 + valorFloat2}")
    print(f"{ieee32Um} + {ieee32Dois}: {int(bitSinal1) + int(bitSinal2)}|{int(bitExpoente1) + int(bitExpoente2)}|{int(bitMantisa1) + int(bitMantisa2)}")

    simOuNao1 = input("Quer saber porque os resultados são diferentes? (Y/N) ")

    if (simOuNao1 == "Y" or simOuNao1 == "y") :
        print("\nRazão do resultado diferente de Ieee 754 e da linguagem normal:"),
        print("\nNumeros no Ieee 754 podem ser representados com precisão em binário, enquanto números decimais em uma linguagem de programação tem problema com isso."),
        print("\nIeee 754 permite diferentes modos de arredondamentos enquanto linguagens de programação usam seus proprio modos distintos, que altera o resultado final por varios motivos, um deles podendo ser a limitação de bits."),
        print("\nO corportamento de execeções em linguagens normais faz com que aperação valores invalidos ou denormalizados invês do Ieee 754.")

        simOuNao2 = input("Quer ouvir mais? (Y/N) ")

        if (simOuNao2 == "Y" or simOuNao2 == "y") :
            print("\nO Resultado obtido pela calculadora foi exatamente o mesmo da operação normal? \nNão, foi muito diferente, que como explicado anteriormente, foi por causa de erro de arredodamento representados pela falta de precisão no binário por parte da operação normal, e o corportamento de execeções em linguagens normais"),
            print("\nHouve diferença no valor binário do resultado? \nHouve sim, porque somou diretamente os valores dos dois resultados, porque a linguagem natural não reconhece os numeros como binario e com isso, não faz o calculo corretamente"),
            print("\nComo o arredondamento e a limitação de bits influenciam os cálculos? \nO problema principal é que computadores tem memoria finita e não consegue representar todos os numeros na matématica, que caso tenha muitos numeros negativos ou postivos ou um grande numero fracionario, teriamos underflow ou overflow, então, é preciso ter uma limitação nos bits do computador para isso não acontecer, mais mesmo assim temos problemas de precisão, aonde o comprimento da mantissa, também limitado pela memoria finita, não consegue representar todos os possiveis numeros, então, arrendondamos pro numero mais proximo caso não for conseguido ser exibido nela, dando pequenos erros no resultado final por causa deste problema de memoria.")

            simOuNao3 = input("Quer ouvir mais? (Y/N) ")

            if (simOuNao3 == "Y" or simOuNao3 == "y") :
                print("\nPor que numeros como 0.1 ou 0.2 não são representados exatamente no formato IEEE 754?\n Isso é porque eles não são compativeis entre as bases decimais e binárias, e como dito anteriormente, com sua memoria infinita, não conseguem representar esses numeros complentos sem ter overflow, então, seu valor é arrendado para o mais proximo."),
                print("\nQue tipo de erro numérico esse fenômeno representa? \n Esse fenomeno representa principalmente o de cancelamento catastrofico e erro relativo. Erro relativo, por aproximar um valor para arrendondar-lo pro seu valor de referencia mais exato, e cancelamento catastrófico, porque já estamos subtraindo dois numeros já aproximados por erro relativo, se cancelando e aumentando o erro relativo da equação final entre esses dois numeros, maior que antes da conta.")


