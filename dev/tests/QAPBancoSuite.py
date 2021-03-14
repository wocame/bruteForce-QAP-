# -*- coding: utf-8 -*-

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class QAPBancoSuite:

    def __init__(self, testes=None, alg=None):

        # Valores padrão
        self.__alg = None
        self.__testes = None
        self.__testes_executados = None

        if alg is not None:
            self.definir_algoritmo(alg)

        if testes is not None:
            self.definir_testes(testes)

    def definir_testes(self, testes):
        self.__testes = testes
        self.__testes_executados = None

    def resgatar_testes(self):
        return self.__testes

    def definir_algoritmo(self, alg):
        self.__alg = alg
        self.__testes_executados = None

    def resgatar_algoritmo(self):
        return self.__alg

    def rodar_testes(self):
        for teste in self.__testes:
            teste.resolver_problema_com(self.__alg)
        self.__testes_executados = self.__testes

    def testes_executados(self):
        return self.__testes_executados

    def dados_tempo_execucao(self):

        # Garante que foi executado
        if self.__testes_executados is None:
            return None

        # Define valores de 'n' testados
        valores_n = []
        teste_n = {}
        for teste in self.__testes_executados:
            n = teste.num_dependencias_problema()
            if n not in teste_n:
                teste_n[n] = [teste]
                valores_n.append(n)
            else:
                teste_n[n].append(teste)
        valores_n.sort()

        # Obter info de tempo de execucao
        media = []
        stdev = []
        for n in valores_n:
            media_n = 0
            stdev_n = 0
            for teste in teste_n[n]:
                media_n += teste.tempo_medio()
                stdev_n += teste.tempo_desvio()
            media.append(media_n / len(teste_n[n]))
            stdev.append(stdev_n / len(teste_n[n]))

        # Retornar dataframe
        return pd.DataFrame({'n': valores_n, 'media': media, 'desvio': stdev})

    def grafico_tempo_execucao(self):

        # Garante que foi executado
        if self.__testes_executados is None:
            return None

        df = self.dados_tempo_execucao()
        ax = plt.subplot()
        ax.plot(df['n'], df['media'], 'b', label="media")
        ax.errorbar(df['n'], df['media'], df['desvio'], linestyle='None', ecolor='r', label="desvio padrão")
        ax.legend(loc='upper left')
        ax.title.set_text("Tempo de execução: "+self.__alg.__name__)
        return ax

    # Métodos privados ########################################

    def __str__(self):
        string = f"QAPBancoSuite com {len(self.__testes)} testes\n"
        if self.__testes_executados is None:
            string += "<Não executado>"
        else:
            for teste in self.__testes_executados:
                string += str(teste) + '\n'
        return string
