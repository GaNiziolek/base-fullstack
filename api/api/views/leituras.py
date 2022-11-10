from pyramid import request
from cornice import Service
from cornice.validators import colander_body_validator
import colander
import datetime

from .. import Session

from ..models import Leituras
from ..models import IO

leituras = Service(
    name='leituras',
    path='/leituras'
)

@leituras.get()
def leituras_get(request):

    retorno = []

    with Session() as session:

        ID_LEITURA            = request.params.get('id_leitura')
        ID_IO                 = request.params.get('id_io')
        CODIGO_LEITURA        = request.params.get('codigo_leitura')
        SUCESSO_PROCESSAMENTO = request.params.get('sucesso_processamento')
        RETRABALHO_VINCULADO  = request.params.get('retrabalho_vinculado')
        LEITURA_MANUAL        = request.params.get('leitura_manual')

        conditions = []

        if ID_LEITURA:
            conditions.append(Leituras.id_leitura == ID_LEITURA)

        if ID_IO:
            conditions.append(Leituras.id_io == ID_IO)

        if CODIGO_LEITURA:
            conditions.append(Leituras.codigo_leitura == CODIGO_LEITURA)
        
        if SUCESSO_PROCESSAMENTO:
            conditions.append(Leituras.sucesso_processamento == SUCESSO_PROCESSAMENTO)

        if RETRABALHO_VINCULADO:
            conditions.append(Leituras.retrabalho_vinculado == RETRABALHO_VINCULADO)

        if LEITURA_MANUAL:
            conditions.append(Leituras.leitura_manual == LEITURA_MANUAL)

        results = session.query(Leituras).where(*conditions)

        for res in results:

            leitura = {
                'id_leitura':            res.id_leitura,
                'id_io':                 res.id_io,
                'data_leitura':          res.data_leitura,
                'codigo_leitura':        res.codigo_leitura,
                'qtd_leitura':           res.qtd_leitura,
                'data_processamento':    res.data_processamento,
                'log_processamento':     res.log_processamento,
                'sucesso_processamento': res.sucesso_processamento,
                'tempo_processamento':   res.tempo_processamento,
                'info_leitura':          res.info_leitura,
                'info_data':             res.info_data,
                'sequencia_leitura':     res.sequencia_leitura,
                'sequencia_peca':        res.sequencia_peca,
                'retrabalho_vinculado':  res.retrabalho_vinculado,
                'id_retrabalho':         res.id_retrabalho,
                'leitura_manual':        res.leitura_manual
            }
            retorno.append(leitura)
    
    return retorno

class leituras_post_schema(colander.MappingSchema):

    codigo_leitura     = colander.SchemaNode(colander.String())
    data_leitura       = colander.SchemaNode(colander.DateTime())
    id_recurso         = colander.SchemaNode(colander.Integer(), validator=colander.Range(1), missing=colander.drop)
    id_io              = colander.SchemaNode(colander.Integer(), validator=colander.Range(1), missing=colander.drop)
    qtd_leitura        = colander.SchemaNode(colander.Integer())
    leitura_manual     = colander.SchemaNode(colander.Boolean())

@leituras.post(schema=leituras_post_schema(), validators=(colander_body_validator,))
def leituras_post(request):

    with Session() as session:

        body = leituras_post_schema().deserialize(request.json_body)

        print(body)

        exit()
        
        if body['id_io'] == 0:
            if not 'id_recurso' in body or body.get('id_recurso') == 0: 
                return colander.Invalid(leituras_post_schema, "Quando 'id_io' não for especificado (ou igual a zero), é necessário especificar 'id_recurso'").asdict()

            body['id_io'] = (session.query(IO.id_io)
                                    .where(IO.io_inativa == 'N')
                                    .where(IO.id_recurso == body['id_recurso'])
                            )
                            
        io = Leituras(
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
