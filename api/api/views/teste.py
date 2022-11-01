from cornice import Service

teste = Service(
    name='teste',
    path='/teste'
)

@teste.get()
def get_teste(request):
    return {'teste': True}