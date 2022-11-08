import sqlalchemy.types as types

# Help: https://docs.sqlalchemy.org/en/14/core/custom_types.html#types-typedecorator

class BoolSN(types.TypeDecorator):
    """
        Converte os valores 'S' ou 'N' da Tabela para valores True ou False do python
    """

    cache_ok = True

    impl = types.String

    def process_bind_param(self, value, dialect) -> None:

        if str(value).strip().upper() == 'TRUE':
            return 'S'
        else:
            return 'N'

    def process_result_value(self, value, dialect) -> None:

        if str(value).strip().upper() == 'S':
            return True
        elif str(value).strip().upper() == 'N':
            return False
        else:
            return None