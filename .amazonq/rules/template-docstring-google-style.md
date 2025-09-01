# Template de Documentação Inline - Google Style

<div align="center">

**Padrão Google Style para Docstrings e Type Hints**

[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)
[![Style](https://img.shields.io/badge/style-google-green)](https://google.github.io/styleguide/pyguide.html)
[![Type Hints](https://img.shields.io/badge/type--hints-PEP484-orange)](https://pep8.org)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Estrutura Básica](#-estrutura-básica)
- [Classes](#-classes)
- [Métodos e Funções](#-métodos-e-funções)
- [Type Hints](#-type-hints)
- [Exemplos Práticos](#-exemplos-práticos)
- [Ferramentas](#-ferramentas)
- [Referências](#-referências)

---

## 🎯 Visão Geral

### Padrão Google Style

O Google Style é um padrão de documentação inline que utiliza docstrings estruturadas para documentar código Python de forma clara e consistente.

### Benefícios

- ✅ **Legibilidade**: Formato claro e estruturado
- ✅ **Automação**: Compatível com ferramentas de documentação
- ✅ **Padronização**: Consistência em todo o projeto
- ✅ **Type Safety**: Integração com type hints

---

## 🏗️ Estrutura Básica

### Template Geral

```python
def funcao_exemplo(parametro1: tipo, parametro2: tipo = valor_padrao) -> tipo_retorno:
    """Descrição breve da função em uma linha.

    Descrição mais detalhada da função, explicando seu propósito,
    comportamento e contexto de uso. Pode ocupar múltiplas linhas.

    Args:
        parametro1 (tipo): Descrição do primeiro parâmetro.
        parametro2 (tipo, optional): Descrição do segundo parâmetro.
            Defaults to valor_padrao.

    Returns:
        tipo_retorno: Descrição do valor retornado.

    Raises:
        TipoExcecao: Descrição de quando esta exceção é lançada.
        OutraExcecao: Descrição de outra exceção possível.

    Example:
        Exemplo básico de uso:

        >>> resultado = funcao_exemplo("valor1", parametro2="valor2")
        >>> print(resultado)
        'resultado_esperado'

    Note:
        Informações adicionais importantes sobre a função.

    Todo:
        * Melhorias futuras planejadas
        * Funcionalidades a serem implementadas
    """
    pass
```

---

## 🏛️ Classes

### Template de Classe

```python
from typing import Optional, List, Dict, Any
from datetime import datetime

class ExemploClasse:
    """Descrição breve da classe.

    Descrição detalhada da classe, seu propósito no sistema,
    responsabilidades e como deve ser utilizada.

    Attributes:
        atributo_publico (str): Descrição do atributo público.
        _atributo_protegido (int): Descrição do atributo protegido.
        CONSTANTE_CLASSE (str): Descrição da constante da classe.

    Example:
        Uso básico da classe:

        >>> instancia = ExemploClasse("valor_inicial")
        >>> resultado = instancia.metodo_principal()
        >>> print(resultado)
        'resultado_esperado'
    """

    CONSTANTE_CLASSE: str = "valor_constante"

    def __init__(
        self, 
        parametro_obrigatorio: str,
        parametro_opcional: Optional[int] = None,
        configuracoes: Optional[Dict[str, Any]] = None
    ) -> None:
        """Inicializa uma nova instância da classe.

        Args:
            parametro_obrigatorio (str): Parâmetro obrigatório para inicialização.
            parametro_opcional (int, optional): Parâmetro opcional.
                Defaults to None.
            configuracoes (Dict[str, Any], optional): Dicionário de configurações.
                Defaults to None.

        Raises:
            ValueError: Se parametro_obrigatorio for vazio.
            TypeError: Se configuracoes não for um dicionário.

        Example:
            >>> instancia = ExemploClasse("valor", parametro_opcional=42)
            >>> print(instancia.atributo_publico)
            'valor'
        """
        if not parametro_obrigatorio:
            raise ValueError("parametro_obrigatorio não pode ser vazio")
        
        self.atributo_publico = parametro_obrigatorio
        self._atributo_protegido = parametro_opcional or 0
        self._configuracoes = configuracoes or {}

    @property
    def propriedade_exemplo(self) -> str:
        """str: Propriedade de exemplo com getter e setter.

        Esta propriedade demonstra como documentar properties.
        O tipo é especificado no início da docstring.

        Returns:
            str: Valor atual da propriedade.

        Example:
            >>> instancia.propriedade_exemplo = "novo_valor"
            >>> print(instancia.propriedade_exemplo)
            'novo_valor'
        """
        return self._valor_interno

    @propriedade_exemplo.setter
    def propriedade_exemplo(self, valor: str) -> None:
        """Define o valor da propriedade.

        Args:
            valor (str): Novo valor para a propriedade.

        Raises:
            ValueError: Se valor for None ou vazio.
        """
        if not valor:
            raise ValueError("Valor não pode ser None ou vazio")
        self._valor_interno = valor
```

---

## 🔧 Métodos e Funções

### Método Simples

```python
def metodo_simples(self, entrada: str) -> bool:
    """Verifica se a entrada é válida.

    Args:
        entrada (str): String a ser validada.

    Returns:
        bool: True se válida, False caso contrário.
    """
    return len(entrada) > 0
```

### Método Complexo

```python
def processar_dados(
    self,
    dados: List[Dict[str, Any]],
    filtros: Optional[Dict[str, Any]] = None,
    ordenar_por: Optional[str] = None,
    reverso: bool = False
) -> List[Dict[str, Any]]:
    """Processa uma lista de dados aplicando filtros e ordenação.

    Este método recebe uma lista de dicionários, aplica filtros opcionais
    e retorna os dados processados e ordenados conforme especificado.

    Args:
        dados (List[Dict[str, Any]]): Lista de dicionários para processar.
        filtros (Dict[str, Any], optional): Filtros a serem aplicados.
            Chaves devem corresponder a campos nos dados.
            Defaults to None.
        ordenar_por (str, optional): Campo para ordenação.
            Defaults to None.
        reverso (bool, optional): Se True, ordena em ordem decrescente.
            Defaults to False.

    Returns:
        List[Dict[str, Any]]: Lista processada e ordenada.

    Raises:
        ValueError: Se dados estiver vazio.
        KeyError: Se ordenar_por não existir nos dados.
        TypeError: Se dados não for uma lista de dicionários.

    Example:
        Processamento básico:

        >>> dados = [{"nome": "João", "idade": 30}, {"nome": "Maria", "idade": 25}]
        >>> filtros = {"idade": lambda x: x > 25}
        >>> resultado = instancia.processar_dados(dados, filtros, "nome")
        >>> print(resultado)
        [{"nome": "João", "idade": 30}]

    Note:
        O método modifica a lista original. Use copy() se precisar preservar
        os dados originais.

    Todo:
        * Adicionar suporte para filtros mais complexos
        * Implementar cache para melhor performance
    """
    if not dados:
        raise ValueError("Lista de dados não pode estar vazia")
    
    # Implementação do método...
    pass
```

### Função com *args e **kwargs

```python
def funcao_flexivel(
    parametro_obrigatorio: str,
    *args: Any,
    **kwargs: Any
) -> Dict[str, Any]:
    """Função que aceita argumentos variáveis.

    Args:
        parametro_obrigatorio (str): Parâmetro sempre necessário.
        *args: Argumentos posicionais variáveis.
        **kwargs: Argumentos nomeados variáveis.
            Opções suportadas:
            - debug (bool): Ativa modo debug. Defaults to False.
            - timeout (int): Timeout em segundos. Defaults to 30.

    Returns:
        Dict[str, Any]: Dicionário com resultados processados.
            Contém as chaves:
            - 'status': Status da operação ('success' ou 'error')
            - 'data': Dados processados
            - 'metadata': Informações adicionais

    Example:
        >>> resultado = funcao_flexivel("teste", "arg1", "arg2", debug=True)
        >>> print(resultado['status'])
        'success'
    """
    pass
```

---

## 🏷️ Type Hints

### Tipos Básicos

```python
from typing import (
    Any, Optional, Union, List, Dict, Tuple, Set,
    Callable, Iterator, Generator, TypeVar, Generic
)

def exemplos_tipos_basicos(
    string_param: str,
    int_param: int,
    float_param: float,
    bool_param: bool,
    optional_param: Optional[str] = None,
    union_param: Union[str, int] = "default"
) -> None:
    """Demonstra tipos básicos.

    Args:
        string_param (str): Parâmetro string.
        int_param (int): Parâmetro inteiro.
        float_param (float): Parâmetro float.
        bool_param (bool): Parâmetro booleano.
        optional_param (str, optional): Parâmetro opcional.
        union_param (Union[str, int], optional): Aceita string ou int.
    """
    pass
```

### Tipos Compostos

```python
def exemplos_tipos_compostos(
    lista_strings: List[str],
    dict_config: Dict[str, Any],
    tupla_coordenadas: Tuple[float, float],
    set_ids: Set[int],
    callback: Callable[[str], bool]
) -> Dict[str, List[Any]]:
    """Demonstra tipos compostos.

    Args:
        lista_strings (List[str]): Lista de strings.
        dict_config (Dict[str, Any]): Dicionário de configuração.
        tupla_coordenadas (Tuple[float, float]): Coordenadas (x, y).
        set_ids (Set[int]): Conjunto de IDs únicos.
        callback (Callable[[str], bool]): Função de callback.

    Returns:
        Dict[str, List[Any]]: Resultado processado.
    """
    pass
```

### Tipos Genéricos

```python
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Container(Generic[T]):
    """Container genérico para qualquer tipo.

    Type Parameters:
        T: Tipo dos elementos armazenados no container.

    Attributes:
        items (List[T]): Lista de itens do tipo T.
    """

    def __init__(self) -> None:
        """Inicializa container vazio."""
        self.items: List[T] = []

    def adicionar(self, item: T) -> None:
        """Adiciona item ao container.

        Args:
            item (T): Item a ser adicionado.
        """
        self.items.append(item)

    def obter_primeiro(self) -> Optional[T]:
        """Obtém o primeiro item do container.

        Returns:
            Optional[T]: Primeiro item ou None se vazio.
        """
        return self.items[0] if self.items else None
```

---

## 💡 Exemplos Práticos

### Classe de Serviço

```python
from typing import Protocol, runtime_checkable
from datetime import datetime
import logging

@runtime_checkable
class DatabaseProtocol(Protocol):
    """Protocol para operações de banco de dados."""
    
    def conectar(self) -> None:
        """Estabelece conexão com o banco."""
        ...
    
    def executar_query(self, query: str) -> List[Dict[str, Any]]:
        """Executa query e retorna resultados."""
        ...

class UsuarioService:
    """Serviço para gerenciamento de usuários.

    Esta classe fornece operações CRUD para usuários,
    incluindo validação, autenticação e logging.

    Attributes:
        db (DatabaseProtocol): Instância do banco de dados.
        logger (logging.Logger): Logger para auditoria.

    Example:
        >>> db = PostgreSQLDatabase()
        >>> service = UsuarioService(db)
        >>> usuario = service.criar_usuario("joão", "joao@email.com")
        >>> print(usuario.id)
        1
    """

    def __init__(self, database: DatabaseProtocol) -> None:
        """Inicializa o serviço de usuários.

        Args:
            database (DatabaseProtocol): Implementação do banco de dados.

        Raises:
            TypeError: Se database não implementa DatabaseProtocol.
        """
        if not isinstance(database, DatabaseProtocol):
            raise TypeError("database deve implementar DatabaseProtocol")
        
        self.db = database
        self.logger = logging.getLogger(__name__)

    def criar_usuario(
        self,
        nome: str,
        email: str,
        senha: str,
        ativo: bool = True,
        metadados: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Cria um novo usuário no sistema.

        Valida os dados de entrada, criptografa a senha e
        persiste o usuário no banco de dados.

        Args:
            nome (str): Nome completo do usuário.
            email (str): Email único do usuário.
            senha (str): Senha em texto plano (será criptografada).
            ativo (bool, optional): Status ativo do usuário.
                Defaults to True.
            metadados (Dict[str, Any], optional): Dados adicionais.
                Defaults to None.

        Returns:
            Dict[str, Any]: Dados do usuário criado.
                Contém as chaves:
                - 'id': ID único do usuário
                - 'nome': Nome do usuário
                - 'email': Email do usuário
                - 'ativo': Status ativo
                - 'criado_em': Timestamp de criação

        Raises:
            ValueError: Se nome ou email estiverem vazios.
            ValueError: Se senha for muito fraca.
            IntegrityError: Se email já existir no sistema.

        Example:
            Criação básica:

            >>> usuario = service.criar_usuario(
            ...     "João Silva",
            ...     "joao@exemplo.com",
            ...     "senha123"
            ... )
            >>> print(usuario['id'])
            1

            Com metadados:

            >>> metadados = {"departamento": "TI", "cargo": "Desenvolvedor"}
            >>> usuario = service.criar_usuario(
            ...     "Maria Santos",
            ...     "maria@exemplo.com",
            ...     "senha456",
            ...     metadados=metadados
            ... )

        Note:
            A senha é automaticamente criptografada usando bcrypt
            antes de ser armazenada no banco de dados.

        Todo:
            * Adicionar validação de força da senha
            * Implementar verificação de email
            * Adicionar suporte para avatars
        """
        # Validações
        if not nome or not nome.strip():
            raise ValueError("Nome não pode estar vazio")
        
        if not email or "@" not in email:
            raise ValueError("Email inválido")
        
        if len(senha) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")

        # Log da operação
        self.logger.info(f"Criando usuário: {email}")

        # Implementação...
        usuario_data = {
            "id": 1,
            "nome": nome,
            "email": email,
            "ativo": ativo,
            "criado_em": datetime.now()
        }

        return usuario_data
```

### Função Utilitária

```python
def validar_cpf(cpf: str) -> bool:
    """Valida um número de CPF brasileiro.

    Verifica se o CPF possui formato válido e dígitos verificadores corretos,
    seguindo o algoritmo oficial da Receita Federal.

    Args:
        cpf (str): CPF a ser validado. Pode conter pontos e hífen.

    Returns:
        bool: True se CPF for válido, False caso contrário.

    Example:
        CPF válido:

        >>> validar_cpf("123.456.789-09")
        True

        CPF inválido:

        >>> validar_cpf("111.111.111-11")
        False

        Apenas números:

        >>> validar_cpf("12345678909")
        True

    Note:
        A função remove automaticamente pontos e hífens antes da validação.
        CPFs com todos os dígitos iguais são considerados inválidos.
    """
    # Remove formatação
    cpf_numeros = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf_numeros) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf_numeros == cpf_numeros[0] * 11:
        return False
    
    # Implementação do algoritmo de validação...
    return True
```

---

## 🛠️ Ferramentas

### Sphinx

```python
"""
Configuração para Sphinx (conf.py):

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Suporte ao Google Style
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx'
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
"""
```

### Pydocstyle

```ini
# setup.cfg
[pydocstyle]
convention = google
add-ignore = D100,D104
```

### MyPy

```ini
# mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/pydocstyle
    rev: 6.1.1
    hooks:
      - id: pydocstyle
        args: [--convention=google]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.910
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 📚 Referências

### Documentação Oficial

- **[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)** - Guia oficial do Google
- **[PEP 257](https://www.python.org/dev/peps/pep-0257/)** - Docstring Conventions
- **[PEP 484](https://www.python.org/dev/peps/pep-0484/)** - Type Hints
- **[PEP 526](https://www.python.org/dev/peps/pep-0526/)** - Variable Annotations

### Ferramentas

- **[Sphinx](https://www.sphinx-doc.org/)** - Gerador de documentação
- **[Napoleon](https://sphinxcontrib-napoleon.readthedocs.io/)** - Extensão Sphinx para Google Style
- **[Pydocstyle](http://www.pydocstyle.org/)** - Linter para docstrings
- **[MyPy](http://mypy-lang.org/)** - Type checker estático

### Exemplos e Tutoriais

- **[Real Python - Documenting Python Code](https://realpython.com/documenting-python-code/)**
- **[Sphinx Tutorial](https://sphinx-tutorial.readthedocs.io/)**
- **[Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)**

---

<div align="center">

**Mantido por**: Equipe de Desenvolvimento Datametria  
**Última Atualização**: [DD/MM/AAAA]  
**Versão**: 1.0.0

---

**Para dúvidas sobre documentação**: [email-dev]

</div>