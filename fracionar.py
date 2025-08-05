from abc import ABC
from math import isinf, isnan


def _converter_para_numero_fracionario(outro):
    """
    converte um valor para a classe NumeroFracionario, se necessario e
    lida com infinito e NaN diretamente
    """
    if isinstance(outro, NumeroFracionario):
        return outro
    if isinf(outro):
        return NumeroFracionario(float('inf') if outro > 0 else float('-inf'), 0)
    if isnan(outro):
        raise ValueError("valor NaN nao pode ser convertido para NumeroFracionario")
    return NumeroFracionario(outro)


class NumeroFracionario(ABC):
    """
    classe que representa um numero fracionario com suporte ao termo 'M grande'
    """

    def __init__(self, numerador, termo_m=0):
        # trata explicitamente numeros infinitos
        if isinf(numerador):
            self.numerador = float('inf') if numerador > 0 else float('-inf')
        else:
            self.numerador = numerador

        self.termo_m = termo_m

    def __repr__(self):
        """representacao da instancia"""
        if self.termo_m == 0:
            return f"{self.numerador}"
        return f"{self.numerador} + ({self.termo_m} * M)"

    def __str__(self):
        """converte a instancia para uma string legivel"""
        return self.__repr__()

    def __eq__(self, outro):
        """compara se duas instancias sao iguais"""
        outro = _converter_para_numero_fracionario(outro)
        return self.numerador == outro.numerador and self.termo_m == outro.termo_m

    def __add__(self, outro):
        """realiza a soma entre dois numeros fracionarios"""
        outro = _converter_para_numero_fracionario(outro)
        return NumeroFracionario(self.numerador + outro.numerador, self.termo_m + outro.termo_m)

    def __sub__(self, outro):
        """realiza a subtracao entre dois numeros fracionarios"""
        outro = _converter_para_numero_fracionario(outro)
        return NumeroFracionario(self.numerador - outro.numerador, self.termo_m - outro.termo_m)

    def __rsub__(self, outro):
        """permite subtracao reversa para tipos numericos padrao"""
        outro = _converter_para_numero_fracionario(outro)
        return outro - self

    def __mul__(self, outro):
        """realiza a multiplicacao entre dois numeros fracionarios."""
        if not isinstance(outro, NumeroFracionario):
            outro = NumeroFracionario(outro)
        return NumeroFracionario(
            self.numerador * outro.numerador,
            self.termo_m * outro.numerador + self.numerador * outro.termo_m,
        )

    def __rmul__(self, outro):
        """permite multiplicacao reversa para tipos numericos padrao"""
        return self.__mul__(outro)

    def __truediv__(self, outro):
        """realiza a divisao entre dois numeros fracionarios"""
        outro = _converter_para_numero_fracionario(outro)
        if outro.numerador == 0:
            raise ZeroDivisionError("Divisao por zero em NumeroFracionario.")
        return NumeroFracionario(self.numerador / outro.numerador, self.termo_m / outro.numerador)

    def __lt__(self, outro):
        """compara se uma instancia e menor que outra"""
        outro = _converter_para_numero_fracionario(outro)
        if self.termo_m == outro.termo_m:
            return self.numerador < outro.numerador
        return self.termo_m < outro.termo_m

    def __gt__(self, outro):
        """compara se uma instancia e maior que outra"""
        outro = _converter_para_numero_fracionario(outro)
        if self.termo_m == outro.termo_m:
            return self.numerador > outro.numerador
        return self.termo_m > outro.termo_m

    def __le__(self, outro):
        """compara se uma instancia e menor ou igual a outra"""
        outro = _converter_para_numero_fracionario(outro)
        return self < outro or self == outro

    def __ge__(self, outro):
        """compara se uma instancia e maior ou igual a outra"""
        outro = _converter_para_numero_fracionario(outro)
        return self > outro or self == outro

    def __float__(self):
        """
        define como converter um NumeroFracionario para um float
        """
        # Converte para float somando o numerador e o termo M ajustado
        return float(self.numerador) + float(self.termo_m) * 1e6  # Multiplica por um valor alto para simular "M grande"
