from fracionar import NumeroFracionario


def converte_para_fracionar(lista):
    return [NumeroFracionario(e) for e in lista]


"""
classe com as funcoes necessarias para o metodo simplex
"""


class SimplexFuncoes(object):

    def __init__(self, funcao_objetivo, restricoes=None):
        # inicializa o contador de iteracao
        self.iteracao = 0

        # preenche as linhas do tableau das restricoes
        self.linhas_restricoes = []

        total_variaveis_adicionais = len(restricoes) + sum(1 for _, t, _ in restricoes if t != '<=')

        # preenche a linha da funcao objetivo
        coeficiente_z = [1]

        # ajusta os coeficientes da funcao objetivo (invertendo o sinal)
        coeficiente_objetivo = [-c for c in funcao_objetivo]

        # adiciona os coeficientes das variaveis extras (zero)
        coeficiente_variaveis_extras = [0] * total_variaveis_adicionais

        # adiciona o coeficiente do lado direito
        coeficiente_b = [0]

        # concatena todos os coeficientes
        self.linha_funcao_objetivo = coeficiente_z + coeficiente_objetivo + coeficiente_variaveis_extras + coeficiente_b

        # itera sobre as restricoes para construir as linhas do tableau
        for i, (coeficientes, tipo, termo) in enumerate(restricoes):
            # Inicializa os coeficientes das variaveis extras com zeros
            coeficientes_variaveis_adicionais = [0] * total_variaveis_adicionais

            # verifica o tipo da restricao para ajustar os coeficientes das variaveis extras
            if tipo == '<=':
                # variavel de folga adicionada positivamente
                coeficientes_variaveis_adicionais[i] = 1

            elif tipo == '=':
                # variavel de igualdade adicionada positivamente
                coeficientes_variaveis_adicionais[i] = 1
                # ajusta a linha da funcao objetivo para lidar com o termo "M grande"
                index = 1 + len(coeficientes) + i
                self.linha_funcao_objetivo[index] = NumeroFracionario(0, NumeroFracionario(1))

            elif tipo == '>=':
                # variavel de excesso subtraida e variavel artificial adicionada
                coeficientes_variaveis_adicionais[i] = -1
                coeficientes_variaveis_adicionais[i + 1] = 1
                # ajusta a linha da funcao objetivo para lidar com o termo "M grande"
                index = 1 + len(coeficientes) + i + 1
                self.linha_funcao_objetivo[index] = NumeroFracionario(0, NumeroFracionario(1))

            # constroi a linha completa para a restricao e converte para o formato `NumeroFracionario`
            linha_completa = [0] + coeficientes + coeficientes_variaveis_adicionais + [termo]
            self.linhas_restricoes.append(converte_para_fracionar(linha_completa))

    """
     imprime o tableau no formato de matriz.
     o tableau é composta pela linha da funcao objetivo e as linhas das restricoes.
     Cada elemento é convertido em uma string para exibição.
     """

    def printar_tableau(self):
        # combina a funcao objetivo e as restricoes em um unico tableau
        tableau = [self.linha_funcao_objetivo] + self.linhas_restricoes

        # exibe o tableau no formato de matriz, convertendo os elementos para string
        print(f"\nTableau")
        for linha in tableau:
            print(" | ".join(map(str, linha)))

    '''
     encontra a coluna corresponte a variavel que entra da base e retorna seu indice 
     '''

    def encontra_entrada(self):
        # inicializa o menor coeficiente como positivo infinito e o indice como None
        menor_coeficiente = float('inf')
        indice_entra = None

        # itera sobre os coeficientes da funcao objetivo, ignorando a primeira coluna (z)
        # e a última (termo independente)
        for i, coef in enumerate(self.linha_funcao_objetivo[1:-1], start=1):
            if coef < menor_coeficiente:
                menor_coeficiente = coef
                indice_entra = i

        # se o menor coeficiente for nao-negativo, a solução e otima; caso contrario, retorna o indice
        return indice_entra if menor_coeficiente < 0 else None

    '''
     encontra a linha corresponte a variavel que sai da base e retorna seu indice 
     '''

    def encontra_sai(self, coluna_pivo):
        # inicializa o menor valor como infinito
        menor_razao = float('inf')
        # inicializa o indice da linha a ser retornado como None
        indice_sai = None

        # itera sobre as restricoes para calcular a razao b_i / a_ij
        for i, linha in enumerate(self.linhas_restricoes):
            # termo independente (b_i)
            termo = linha[-1]
            # coeficiente da coluna do pivô (a_ij)
            coeficiente_pivo = linha[coluna_pivo]

            if coeficiente_pivo > 0:
                # Calcula a razão b_i / a_ij
                razao = termo / coeficiente_pivo

                # atualiza o menor valor e o indice, se necessario
                if razao < menor_razao:
                    menor_razao = razao
                    indice_sai = i

        # verifica se encontrou um indice valido (nenhuma razao positiva indica problema ilimitado)
        if indice_sai is None:
            raise ValueError("O problema é ilimitado. Nenhuma variavel pode sair da base.")

        return indice_sai

    '''
     faz o pivoteamento, tendo como elemento pivo o elemento pi,pj da matrix de restricoes
     '''

    def pivoteamento(self, linha_pivo, coluna_pivo):
        # obtem o elemento pivo
        elemento_pivo = self.linhas_restricoes[linha_pivo][coluna_pivo]

        # normaliza a linha do pivo, dividindo todos os elementos pelo pivo
        self.linhas_restricoes[linha_pivo] = [
            valor / elemento_pivo for valor in self.linhas_restricoes[linha_pivo]
        ]

        # atualiza a funcao objetivo (fo)
        # ajusta a linha da fo usando a linha pivo e o coeficiente da fo na coluna do pivo
        coeficiente_coluna_pivo = self.linha_funcao_objetivo[coluna_pivo]
        self.linha_funcao_objetivo = [
            valor_fo - coeficiente_coluna_pivo * valor_pivo
            for valor_fo, valor_pivo in zip(
                self.linha_funcao_objetivo, self.linhas_restricoes[linha_pivo]
            )
        ]

        # atualiza as demais linhas do tableau (restricoes)
        for idx, linha in enumerate(self.linhas_restricoes):
            # ignora a linha do pivo
            if idx != linha_pivo:
                coeficiente_coluna = linha[coluna_pivo]
                self.linhas_restricoes[idx] = [
                    valor - coeficiente_coluna * valor_pivo
                    for valor, valor_pivo in zip(linha, self.linhas_restricoes[linha_pivo])
                ]
