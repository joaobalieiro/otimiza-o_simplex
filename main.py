from metodo import SimplexExecutor

""" exemplo dado por (KAGAN N. ET AL, 2009): "Um produtor independente dispõe de 2 unidades de geração, que podem ser 
conectadas ao sistema elétrico em pontos distintos, para a venda do excedente de energia elétrica que são capazes de 
produzir. Tanto os custos de produção quanto as tarifas negociadas para a venda de energia são distintos para os 2 
geradores. O produtor deseja vender o máximo possível de energia seguindo, entretanto, seu plano de negócios, 
que não permite gastar acima de um valor pré-estabelecido para a produção de energia." 

Funcao objetivo:  max z = 90x + 120y         
s.a.     
                     x <= 5000
                     y <= 7000
            50x + 100y <= 800000
                   x,y >= 0
"""

coeficientes_funcao_objetivo = [90, 120]

coeficientes_restricoes = [([1, 0], "<=", 5000), ([0, 1], "<=", 7000), ([50, 100], "<=", 800000)]

simplex = SimplexExecutor(coeficientes_funcao_objetivo, coeficientes_restricoes)
simplex.executar()
