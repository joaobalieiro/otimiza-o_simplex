import time
from auxiliares import SimplexFuncoes
from fracionar import NumeroFracionario


"""
classe responsavel pela criacao e execucao do metodo simplex,
encapsulando a logica do tableau e do fluxo de execucao
"""


class SimplexExecutor:
    """
    inicializa o executor e cria uma instancia do simplex
    """

    def __init__(self, funcao_objetivo, restricoes):

        # cria a instancia do Simplex com os parametros fornecidos
        self.simplex = SimplexFuncoes(funcao_objetivo, restricoes)
        # inicializa o contador de iteracoes
        self.iteracao = 0

    """
    identifica as variaveis atualmente na base, com base no tableau atual
    a logica utilizada verifica se cada coluna e uma coluna canonica, ou seja, 
    possui exatamente um elemento igual a 1 e todos os demais iguais a 0
    """

    @property
    def variavel_basica(self):

        # lista para armazenar os índices das variaveis na base
        dentro_base = []

        # itera sobre todas as colunas exceto a coluna de Z e o termo independente
        for c in range(1, len(self.simplex.linha_funcao_objetivo) - 1):
            # extrai os valores da coluna correspondente
            valores_coluna = [linha[c] for linha in self.simplex.linhas_restricoes]

            # conta quantos elementos da coluna sao iguais a 0 e quantos sao iguais a 1
            numero_de_zeros = valores_coluna.count(NumeroFracionario(0))
            numero_de_ums = valores_coluna.count(NumeroFracionario(1))

            # verifica se a coluna forma um vetor canonico
            # - deve conter exatamente um '1' e o restante '0'
            if numero_de_ums == 1 and numero_de_zeros == len(self.simplex.linhas_restricoes) - 1:
                # adiciona o indice da coluna como variavel na base
                dentro_base.append(c)

        # retorna a lista de indices das variaveis na base
        return dentro_base

    """
    identifica as variaveis que estao fora da base 
    as variaveis fora da base são aquelas que nao aparecem como variaveis canonicas
    no tableau atual, ou seja, nao estao associadas a colunas da identidade
    """

    @property
    def variavel_nao_basica(self):

        # constroi uma lista de indices das variaveis ignorando Z e o termo independente
        fora_base = [
            # itera pelos indices das variaveis
            i for i in range(1, len(self.simplex.linha_funcao_objetivo) - 1)
            # inclui apenas aquelas que nao estao na base
            if i not in self.variavel_basica
        ]

        return fora_base

    """
    calcula a solucao otima do problema de otimizacao, verifica quais variaveis estao dentro ou
    fora da base e calcula seus valores correspondentes
    """

    @property
    def solucao_otima(self):

        # recupera as variaveis que estao dentro e fora da base
        dentro = self.variavel_basica
        fora = self.variavel_nao_basica

        solucao = []

        # para cada variavel na base, busca seu valor no tableau
        for val in dentro:
            for linha in self.simplex.linhas_restricoes:
                # identifica a linha correspondente na base
                if linha[val] == NumeroFracionario(1):
                    # adiciona o valor da variável (índice, valor)
                    solucao.append((val, linha[-1]))
                    break

        # para as variaveis fora da base, seus valores sao automaticamente zero
        solucao += [(val, NumeroFracionario(0)) for val in fora]

        # converte os valores fracionarios para float para maior legibilidade no resultado
        return [(t[0], float(t[1])) for t in solucao]

    """
    executa o metodo simplex iterativamente ate que a solucao otima seja encontrada
    e mede o tempo total de execucao
    """

    def executar(self):

        # inicia o cronometro
        tempo_inicial = time.time()

        # imprime o tableau inicial
        self.simplex.printar_tableau()

        # executa o metodo simplex iterativamente ate todos os coeficientes na linha objetivo forem positivos
        while not all(coeficientes >= 0 for coeficientes in self.simplex.linha_funcao_objetivo[1:-1]):
            self.iteracao += 1
            coluna_pivo = self.simplex.encontra_entrada()
            linha_pivo = self.simplex.encontra_sai(coluna_pivo)
            self.simplex.pivoteamento(linha_pivo, coluna_pivo)

            print(f'\nIteração {self.iteracao}:')
            print(f'Coluna do pivô: {coluna_pivo + 1}, Linha do pivô: {linha_pivo + 1}')
            self.simplex.printar_tableau()

        # para o cronometro
        tempo_final = time.time()
        tempo_total = tempo_final - tempo_inicial

        print(f"\nTempo total de execucao: {tempo_total:.4f} segundos.")
        print(f"Total de iterações: {self.iteracao}.")
        # o valor otimo da função objetivo esta no ultimo elemento da linha da função objetivo (Z)
        print(f"Valor otimo: {float(self.simplex.linha_funcao_objetivo[-1])}.")
        print(f"Solucao otima: {[(f'x{t[0]}', t[1]) for t in self.solucao_otima]}.")
        print(f"Variaveis Basicas: {[f'x{i}' for i in self.variavel_basica]}.")
        print(f"Variaveis Nao Basicas: {[f'x{i}' for i in self.variavel_nao_basica]}.")
