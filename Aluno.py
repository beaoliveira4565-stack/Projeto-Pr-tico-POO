
import tkinter as tk
from tkinter import ttk, messagebox
import os

class Aluno:
    def __init__(self, Matricula, Nome, CPF, Email, Codigo_curso):
        self._Matricula = Matricula
        self._Nome = Nome
        self._CPF = CPF
        self._Email = Email
        self._Codigo_curso = Codigo_curso

    @property
    def Matricula(self):
        return self._Matricula

    @property
    def Nome(self):
        return self._Nome

    @Nome.setter
    def Nome(self, novo_nome):
        self._Nome = novo_nome

    @property
    def CPF(self):
        return self._CPF

    @CPF.setter
    def CPF(self, novo_CPF):
        self._CPF = novo_CPF

    @property
    def Email(self):
        return self._Email

    @Email.setter
    def Email(self, novo_Email):
        self._Email = novo_Email

    @property
    def Codigo_curso(self):
        return self._Codigo_curso

    @Codigo_curso.setter
    def Codigo_curso(self, novo_codigo):
        self._Codigo_curso = novo_codigo

    # EXIBIR DADOS DO ALUNO
    def __str__(self):
        return f"{self.Matricula} - {self.Nome} - {self.Email}"

    # CONVERTER DADOS PARA ARQUIVO TXT
    def para_txt(self):
        return (
            f"{self.Matricula};{self.Nome};{self.CPF};"
            f"{self.Email};{self.Codigo_curso}"
        )

           

