from pyramid import request
from cornice import Service
from cornice.validators import colander_body_validator
import colander
import datetime

from .. import Session

from ..models import IO

ios = Service(
    name='ios',
    path='/ios'
)

@ios.get()
def ios_get(request):

    retorno = []

    with Session() as session:

        _id_io      = request.params.get('id_io')
        _id_recurso = request.params.get('id_recurso')

        conditions = []

        if _id_io:
            conditions.append(IO.id_io == _id_io)

        if _id_recurso:
            conditions.append(IO.id_recurso == _id_recurso)

        results = session.query(IO).where(*conditions)

        for res in results:

            io = {
                'id_io':              res.id_io,
                'descricao_io':       res.descricao_io,
                'endereco_ip':        res.endereco_ip,
                'id_recurso':         res.id_recurso,
                'io_inativa':         res.io_inativa,
                'data_atualizacao':   res.data_atualizacao,
                'io_ligada':          res.io_ligada,
                'fila_imagens':       res.fila_imagens,
                'temperatura_camera': res.temperatura_camera,
                'erros_io':           res.erros_io,
                'max_tempo_inativo':  res.max_tempo_inativo
            }
        
            retorno.append(io)
    
    return retorno


class ios_put_schema(colander.MappingSchema):

    id_io              = colander.SchemaNode(colander.Integer())
    fila_imagens    = colander.SchemaNode(colander.Integer())
    temperatura_camera = colander.SchemaNode(colander.Float())
    data_atualizacao   = colander.SchemaNode(colander.DateTime())

    @colander.instantiate()
    class erros_io(colander.SequenceSchema):
        @colander.instantiate(missing=())
        class erro(colander.MappingSchema):
            processo_fonte = colander.SchemaNode(colander.String())
            vi_fonte       = colander.SchemaNode(colander.String())
            codigo_erro    = colander.SchemaNode(colander.Integer())
            descricao_erro = colander.SchemaNode(colander.String())
            data_erro      = colander.SchemaNode(colander.DateTime())

@ios.put(schema=ios_put_schema(), validators=(colander_body_validator,))
def ios_put(request):

    with Session() as session:

        body = request.json_body

        io = session.get(IO, body['id_io'])

        io.io_ligada          = 'S'
        io.fila_imagens       = body['fila_imagens']
        io.temperatura_camera = body['temperatura_camera']
        io.data_atualizacao   = body['data_atualizacao']
        io.erros_io           = body['erros_io']

        session.commit()


class ios_post_schema(colander.MappingSchema):

    descricao_io       = colander.SchemaNode(colander.String())
    endereco_ip        = colander.SchemaNode(colander.String())
    id_recurso         = colander.SchemaNode(colander.Integer())
    max_tempo_inativo  = colander.SchemaNode(colander.Integer())
    temperatura_camera = colander.SchemaNode(colander.Float())

@ios.post(schema=ios_post_schema(), validators=(colander_body_validator,))
def ios_post(request):

    with Session() as session:

        body = request.json_body

        io = IO(
            descricao_io       = body['descricao_io'],
            endereco_ip        = body['endereco_ip'],
            id_recurso         = body['id_recurso'],
            max_tempo_inativo  = body['max_tempo_inativo'],
            temperatura_camera = body['temperatura_camera'],
            io_ligada          = 'N',
            io_inativa         = 'N',
            data_atualizacao   = datetime.datetime.now().isoformat()
        )

        session.add(io)

        session.commit()
