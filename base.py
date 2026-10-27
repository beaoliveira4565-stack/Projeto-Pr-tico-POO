"""Infraestrutura comum: classe Entidade e GerenciadorBase (persistência em .txt).

Formato dos arquivos: uma linha por registro, campos separados por ';'
Ex.: 202301;João Silva;123.456.789-00;joao@email.com;10
"""
import copy
import os


def texto_valido(valor, campo):
    """Remove espaços e garante que o valor não é vazio nem contém ';'."""
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"O campo '{campo}' não pode ficar vazio.")
    if ";" in valor:
        raise ValueError(f"O campo '{campo}' não pode conter ';'.")
    return valor


class Entidade:
    """Modelo de dados (sem lógica de persistência).

    O 1º item de CAMPOS é sempre o identificador. As regras de CRUD, leitura e
    escrita de arquivo ficam nas classes Gerenciadoras.
    """
    CAMPOS = []   # lista de (atributo, rótulo)
    OPCOES = {}   # atributo -> valores permitidos (usado na interface gráfica)

    @property
    def codigo(self):
        return getattr(self, self.CAMPOS[0][0])


class GerenciadorBase:
    """Concentra os requisitos funcionais (RF01-RF05, RF10-RF12):
    CRUD, conversão objeto <-> linha e persistência em arquivo .txt."""
    ARQUIVO = ""
    CLASSE = Entidade

    def __init__(self, pasta="dados"):
        self._caminho = os.path.join(pasta, self.ARQUIVO)
        self._itens = []
        self.dependentes = []  # [(gerenciador, atributo, descrição)] p/ integridade
        self.carregar()

    # ---------- conversão objeto <-> linha do .txt ----------
    def _para_linha(self, obj):
        return ";".join(str(getattr(obj, a)) for a, _ in self.CLASSE.CAMPOS)

    def _de_linha(self, linha):
        partes = linha.strip().split(";")
        if len(partes) != len(self.CLASSE.CAMPOS):
            raise ValueError(f"Linha inválida em {self.ARQUIVO}: '{linha}'")
        return self.CLASSE(*partes)

    # ---------- persistência ----------
    def carregar(self):
        """Lê o .txt e converte cada linha em objeto."""
        self._itens = []
        if not os.path.exists(self._caminho):
            return
        with open(self._caminho, encoding="utf-8") as f:
            for linha in f:
                if linha.strip():
                    self._itens.append(self._de_linha(linha))

    def salvar(self):
        """Reescreve o .txt com o estado atual da lista."""
        os.makedirs(os.path.dirname(self._caminho) or ".", exist_ok=True)
        with open(self._caminho, "w", encoding="utf-8") as f:
            for item in self._itens:
                f.write(self._para_linha(item) + "\n")

    # ---------- gancho para regras de integração ----------
    def validar(self, obj):
        """Sobrescrito pelas subclasses para checar chaves estrangeiras."""

    # ---------- CRUD ----------
    def cadastrar(self, obj):
        if self.buscar_por_codigo(obj.codigo):
            raise ValueError(f"Já existe registro com código '{obj.codigo}'.")
        self.validar(obj)
        self._itens.append(obj)
        self.salvar()

    def listar(self):
        return list(self._itens)

    def buscar_por_codigo(self, codigo):
        codigo = str(codigo).strip()
        return next((i for i in self._itens if str(i.codigo) == codigo), None)

    def alterar(self, codigo, **campos):
        obj = self.buscar_por_codigo(codigo)
        if obj is None:
            raise ValueError(f"Registro '{codigo}' não encontrado.")
        if self.CLASSE.CAMPOS[0][0] in campos:
            raise ValueError("O código/matrícula não pode ser alterado.")
        novo = copy.copy(obj)            # altera uma cópia: se falhar, nada muda
        for atributo, valor in campos.items():
            setattr(novo, atributo, valor)   # passa pelos setters (validação)
        self.validar(novo)
        self._itens[self._itens.index(obj)] = novo
        self.salvar()

    def excluir(self, codigo):
        obj = self.buscar_por_codigo(codigo)
        if obj is None:
            raise ValueError(f"Registro '{codigo}' não encontrado.")
        for ger, atributo, desc in self.dependentes:
            if any(str(getattr(i, atributo)) == str(obj.codigo) for i in ger.listar()):
                raise ValueError(f"Não é possível excluir: há {desc} vinculado(s).")
        self._itens.remove(obj)
        self.salvar()

    def pesquisar(self, termo):
        """Busca por código exato ou por parte do nome."""
        termo = str(termo).strip().lower()
        return [i for i in self._itens
                if termo == str(i.codigo).lower() or termo in i.nome.lower()]
