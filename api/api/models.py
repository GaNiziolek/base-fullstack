from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.dialects.postgresql import CIDR
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import FLOAT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from .utils.custom_types import BoolSN

# Registra todos os Models com um schema do colander
# atraves do atributo __colanderalchemy__
#from sqlalchemy import event
#from sqlalchemy.orm import mapper
#from colanderalchemy import setup_schema
#event.listen(mapper, 'mapper_configured', setup_schema)

Base = declarative_base()

class IO(Base):
    __tablename__ = 'tio_cad'
    __table_args__ = {'schema': 'inusitta'}

    id_io              = Column('id_uio', INTEGER, primary_key=True)
    descricao_io       = Column('des_io', TEXT)
    endereco_ip        = Column('end_ip', CIDR) 
    id_recurso         = Column('id_rec', INTEGER)
    io_inativa         = Column('ina_io', BoolSN)
    data_atualizacao   = Column('datatt', TIMESTAMP)
    io_ligada          = Column('io_lig', BoolSN)
    fila_imagens       = Column('filimg', INTEGER)
    temperatura_camera = Column('tmpcam', FLOAT)
    erros_io           = Column('io_err', JSON)
    max_tempo_inativo  = Column('tmpina', INTEGER)

    def __repr__(self):
        return f'IO(id_io={self.id_io!r}, descricao_io={self.descricao_io!r})'

class Leituras(Base):
    __tablename__ = 'tio_lei'
    __table_args__ = {'schema': 'inusitta'}

    id_leitura            = Column('id_lei', INTEGER, primary_key=True)
    id_io                 = Column('id_uio', INTEGER)
    data_leitura          = Column('datlei', TIMESTAMP)
    codigo_leitura        = Column('leicod', TEXT)
    qtd_leitura           = Column('qtdlei', INTEGER)
    data_processamento    = Column('datpro', TIMESTAMP)
    log_processamento     = Column('logpro', TEXT)
    sucesso_processamento = Column('sucpro', BoolSN)
    tempo_processamento   = Column('tempro', JSON)
    info_leitura          = Column('infcod', JSON)
    info_data             = Column('datinf', TIMESTAMP)
    sequencia_leitura     = Column('seqlei', INTEGER)
    sequencia_peca        = Column('seqpec', INTEGER)
    retrabalho_vinculado  = Column('retvin', BoolSN)
    id_retrabalho         = Column('id_ret', INTEGER)
    leitura_manual        = Column('leiman', BoolSN)

    def __repr__(self):
        return f'Leitura(id_leitura={self.id_leitura!r})'
