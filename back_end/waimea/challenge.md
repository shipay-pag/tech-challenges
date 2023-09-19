# Shipay Back-End Engineer Challenge

***Nota: Utilizaremos os seguintes critérios para a avaliação: Desempenho, Testes, Manutenabilidade e boas práticas de engenharia de software.***

1.- Sua squad irá desenvolver uma nova funcionalidade que irá prover um serviço de validação de cadastro de clientes, ao informar o CNPJ e o CEP do endereço do cliente iremos consultar duas APIs de terceiros, a primeira irá retornar informações da empresa de acordo com o CNPJ e a segunda API irá retornar detalhes de um endereço a partir de um CEP. Com os resultados das duas APIs iremos comparar o endereço do cadastro da empresa obtido pelo CNPJ com o endereço obtido através da consulta do CEP e verificar se as informações de unidade federativa, cidade e logradouro coincidem, e caso o endereço de uma consulta seja encontrada na outra retornaremos HTTP 200 e na negativa um HTTP 404.
Como este novo serviço deverá ser resiliente e essencial para os nossos cadastros, a solução proposta deverá permitir retentativas automáticas em casos de falhas e o chaveamento entre dois provedores de resolução do endereço pelo CEP, ou seja usaremos a API de um provedor como padrão e caso o serviço esteja fora do ar o serviço proposto deverá chamar o segundo provedor automaticamente após "N" tentativas.
Apesar de depender diretamente do consumo de múltiplas APIs de terceiros a resposta do serviço desenvolvido deverá ser síncrono.
Você pode verificar exemplos das APIs utilizadas em [requests_e_responses_apis_questao_1.json](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/requests_e_responses_apis_questao_1.json).
Descreva e detalhe como você implementaria o referido serviço? Não é necessário desenvolver o código a menos que você julgue necessário. Sinta-se a vontade para utilizar diagramas, desenhos, descrição textual, arquitetura, design patterns, etc.

2.- Foi nos solicitado a criação de um relatório que mostre a utilização do serviço de lançamentos de foguetes separados por cada um dos nossos clientes em um intervalo de 30 dias. A nossa proposta para o desenvolvimento deste relatório é o de tentar evitar ao máximo algum impacto no fluxo de execução deste endpoint/api (de lançamento de foguetes), uma vez que este é o principal produto da empresa. 
Com essas premissas em mente, o time propôs a utilização apenas das solicitações/requests em comum com o atual serviço e armazenar os dados necessários para o relatório utilizando uma base de dados paralela à base de dados do serviço de lançamentos.
Como você atenderia essa demanda? Lembre-se, caso o novo workflow proposto para o armazenamento dos dados dos relatórios falhe, ele não deve impactar no serviço de lançamentos. 
Descreva em detalhes como você implementaria a solução. Sinta-se a vontade para utilizar diagramas, desenhos, descrição textual, arquitetura, design patterns, etc.

```python
# Linguagem: Python

from uuid import uuid4
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from shipay_auth_async.interfaces import AuthAdapter
from shipay.infrastructure.containers import Container
from shipay.endpoints.schemas import LaunchRequestBody
from shipay.launch.rules import RulesEngine
from shipay.services import LaunchService

router = APIRouter()
auth_client = shipay_auth_async.client()

@router.post('/v1/rocket/launch', tags=['rocket'])
@inject
@auth_client.required_authenticator([AuthAdapter(Container.claims_service(),
                                                 route='/v1/rocket/launch/post',
                                                 type_filter='resource'),
                                     AuthAdapter(Container.jwt_service())])
async def launch(request: Request, schema: LaunchRequestBody = None,
                 service: LaunchService = Depends(Provide[Container.launch_service])):
    try:
        trace_id = request.headers.get('trace_id', str(uuid4()))
        if not schema:
            raise HTTPException(status_code=400, detail='where is the request payload?')
        
        if not RulesEngine.is_launch_approved(schema):
            raise HTTPException(status_code=405, detail='your launch is not allowed.')
            
        pre_flight = await service.pre_flight_check()
        
        if not RulesEngine.is_pre_flight_status_equals_ok(pre_flight.status):
            raise HTTPException(status_code=500, detail='your launch is compromised, please abort.')
        
        countdown_status = service.countdown()

        return await service.launch(trace_id=trace_id,
                                    customer_id=schema.customer_id,
                                    countdown_status=countdown_status,
                                    pre_flight=pre_flight)

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error during launch...{exception.args[0]}')
```

3.- Para evitar sobrecargas em serviços de terceiros, nossa squad decidiu implementar um agendador de eventos para ser utilizado durante a verificação do status de execução de uma operação de reenderização de vídeos em um dos nossos workflows orquestrados utilizando kafka. Como o kafka não permite o agendamento de eventos, a squad acabou por desenvolver um agendador próprio que armazena o evento temporariamente em um banco de dados do tipo chave/valor em memória, bem como um processo executará consultas (em looping) por eventos enfileirados no banco chave/valor que estão com o agendamento para vencer. Ao encontrar um, este agendamento é transformado em um novo evento em um tópico do kafka para dar continuidade ao workflow temporariamente paralizado pelo agendamento e finalmente removido do banco de agendamentos. Confome ilustrado no diagrama [event_scheduler.png](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/event_scheduler.png).
Como o referido workflow deverá ser resiliente e essencial para o nosso produto, a squad gostaria de garantir que o serviço conseguirá suportar 1.000 requesições por segundo com o P99 de 30ms de latencia nas requisições. Descreva detalhadamente quais testes você desenvolveria e executaria para garantir as premissas? Como você faria/executaria os testes propostos?

```python
# Linguagem: Python

from rq import Queue
from redis import Redis
from functions import publish_event

from fastapi import APIRouter, HTTPException, Request
from shipay_auth_async.interfaces import AuthAdapter
from shipay.infrastructure.containers import Container
from shipay.endpoints.schemas import RequestBody


router = APIRouter()
auth_client = shipay_auth_async.client()

@router.post('/v1/render/scheduler', tags=['render'])
@auth_client.required_authenticator([AuthAdapter(Container.claims_service(),
                                                 route='/v1/render/scheduler/post',
                                                 type_filter='resource'),
                                     AuthAdapter(Container.jwt_service())])
async def scheduler(request: Request, schema: RequestBody = None):
    try:

        if not schema:
            raise HTTPException(status_code=400, detail='where is the request payload?')
            
        queue = Queue(name='default', connection=Redis())

        return await queue.enqueue_at(schema.scheduler_datetime, publish_event, schema.event_content)

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error during scheduler event...{exception.args[0]}')
```

4.- Você ficou responsável por mentorar um novo membro do time que além de novo na empresa possui o perfil de nível junior. Ele está finalizando o desenvolvimento de um novo microserviço e está com dúvidas quanto a possíveis implementações de "anti-patterns" em seu código e gostaria da sua avaliação... Quantos anti-patterns você consegue identificar no código dele (se é que existe algum), e caso tenha encontrado por qual motivo você categorizou a implementação como sendo um anti-pattern? *** O código a ser avaliado está disponibilizado no diretório [anti_patterns](https://github.com/shipay-pag/tech-challenges/tree/master/back_end/waimea/anti_patterns).

5.- ATENÇÃO: Caso você tenha escrito o código para responder a questão 1, por favor desconsiderar a questão 5 e nos encaminhe o código da questão 1 no lugar.
 Tomando como base a estrutura do banco de dados fornecida (conforme diagrama [ER_diagram.png](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/ER_diagram.png) e/ou script DDL [1_create_database_ddl.sql](https://github.com/shipay-pag/tech-challenges/blob/master/back_end/waimea/1_create_database_ddl.sql), disponibilizados no repositório do github) construa uma API REST em Python que irá criar um usuário. Os campos obrigatórios serão nome, e-mail e papel do usuário. A senha será um campo opcional, caso o usuário não informe uma senha o serviço da API deverá gerar essa senha automaticamente.

6.- Ajude-nos fazendo o ‘Code Review’ do código de um robô/rotina que exporta os dados da tabela “users” de tempos em tempos. O código foi disponibilizado no mesmo repositório do git hub dentro da pasta [bot](https://github.com/shipay-pag/tech-challenges/tree/master/back_end/waimea/bot). ***ATENÇÃO: Não é necessário implementar as revisões, basta apenas anota-las em um arquivo texto ou em forma de comentários no código.***

7.- Qual ou quais Padrões de Projeto/Design Patterns você utilizaria para normalizar serviços de terceiros (tornar múltiplas interfaces de diferentes fornecedores uniforme), por exemplo serviços de disparos de e-mails, ou então disparos de SMS. ***ATENÇÃO: Não é necessário implementar o Design Pattern, basta descrever qual você utilizaria e por quais motivos optou pelo mesmo.***

BOA SORTE!
