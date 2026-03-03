# Shipay Back-End Engineer Challenge (Versão Java)

***Nota: Utilizaremos os seguintes critérios para a avaliação: Desempenho, Testes, Manutenabilidade e boas práticas de engenharia de software (especialmente padrões Java/Spring).***

1.- Sua squad irá desenvolver uma nova funcionalidade que irá prover um serviço de validação de cadastro de clientes. Ao informar o CNPJ e o CEP do endereço do cliente, iremos consultar duas APIs de terceiros: a primeira retornará informações da empresa de acordo com o CNPJ e a segunda API retornará detalhes de um endereço a partir de um CEP. Com os resultados das duas APIs, iremos comparar o endereço do cadastro da empresa obtido pelo CNPJ com o endereço obtido através da consulta do CEP e verificar se as informações de unidade federativa, cidade e logradouro coincidem. Caso coincidam, retornaremos HTTP 200, caso contrário, um HTTP 404.
Como este novo serviço deverá ser resiliente e essencial para os nossos cadastros, a solução proposta deverá permitir retentativas automáticas em casos de falhas e o chaveamento entre dois provedores de resolução do endereço pelo CEP (fallback), ou seja, usaremos a API de um provedor como padrão e caso o serviço esteja fora do ar, o serviço proposto deverá chamar o segundo provedor automaticamente após "N" tentativas.
Apesar de depender do consumo de múltiplas APIs de terceiros, a resposta do serviço desenvolvido deverá ser síncrona.
Você pode verificar exemplos das APIs utilizadas em [requests_e_responses_apis_questao_1.json](requests_e_responses_apis_questao_1.json).
Descreva e detalhe como você implementaria o referido serviço em Java/Spring Boot? Não é necessário desenvolver o código, a menos que você julgue necessário. Sinta-se à vontade para utilizar diagramas, descrição textual, arquitetura, design patterns (ex: Circuit Breaker, Strategy, etc.), etc.

2.- Foi-nos solicitado a criação de um relatório que mostre a utilização do serviço de lançamentos de foguetes separado por cada um dos nossos clientes em um intervalo de 30 dias. A nossa proposta é tentar evitar ao máximo impacto no fluxo de execução deste endpoint/api, uma vez que este é o principal produto da empresa. 
Com essas premissas em mente, o time propôs a utilização apenas das solicitações em comum com o atual serviço e armazenar os dados necessários para o relatório utilizando uma base de dados paralela à base de dados do serviço de lançamentos.
Como você atenderia essa demanda em Java? Lembre-se, caso o novo workflow proposto para o armazenamento dos dados falhe, ele não deve impactar no serviço de lançamentos. 

```java
// Linguagem: Java (Spring Boot)

@RestController
@RequestMapping("/v1/rocket")
public class LaunchController {

    private final LaunchService service;
    private final RulesEngine rulesEngine;

    public LaunchController(LaunchService service, RulesEngine rulesEngine) {
        this.service = service;
        this.rulesEngine = rulesEngine;
    }

    @PostMapping("/launch")
    @PreAuthorize("@authService.hasPermission('resource', '/v1/rocket/launch/post')")
    public ResponseEntity<?> launch(
            @RequestHeader(value = "trace_id", required = false) String traceId,
            @RequestBody LaunchRequestBody schema) {
        
        try {
            if (traceId == null) {
                traceId = UUID.randomUUID().toString();
            }

            if (schema == null) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "where is the request payload?");
            }

            if (!rulesEngine.isLaunchApproved(schema)) {
                throw new ResponseStatusException(HttpStatus.METHOD_NOT_ALLOWED, "your launch is not allowed.");
            }

            PreFlightStatus preFlight = service.preFlightCheck();

            if (!rulesEngine.isPreFlightStatusOk(preFlight.getStatus())) {
                throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "your launch is compromised, please abort.");
            }

            CountdownStatus countdownStatus = service.countdown();

            LaunchResponse response = service.launch(
                    traceId,
                    schema.getCustomerId(),
                    countdownStatus,
                    preFlight
            );

            return ResponseEntity.ok(response);

        } catch (ResponseStatusException e) {
            throw e;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Error during launch... " + e.getMessage());
        }
    }
}
```

3.- Para evitar sobrecargas em serviços de terceiros, nossa squad decidiu implementar um agendador de eventos para ser utilizado durante a verificação do status de execução de uma operação de renderização de vídeos em um dos nossos workflows orquestrados utilizando kafka. Como o kafka não permite o agendamento de eventos, a squad desenvolveu um agendador próprio que armazena o evento temporariamente em um banco de dados in-memory (Redis), bem como um processo que executa consultas por eventos enfileirados que estão com o agendamento para vencer. Ao encontrar um, esse agendamento é transformado em um novo evento em um tópico do kafka e removido do Redis.
Como o referido workflow deverá ser resiliente, a squad gostaria de garantir que o serviço suporte 1.000 requisições por segundo com P99 de 30ms. Conforme ilustrado no diagrama [event_scheduler.png](event_scheduler.png), descreva detalhadamente quais testes você desenvolveria e executaria para garantir as premissas em um ambiente Java?

```java
// Linguagem: Java (Spring Boot)

@RestController
@RequestMapping("/v1/render")
public class SchedulerController {

    private final JobScheduler jobScheduler;

    public SchedulerController(JobScheduler jobScheduler) {
        this.jobScheduler = jobScheduler;
    }

    @PostMapping("/scheduler")
    @PreAuthorize("@authService.hasPermission('resource', '/v1/render/scheduler/post')")
    public ResponseEntity<?> scheduler(@RequestBody SchedulerRequest schema) {
        try {
            if (schema == null) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "where is the request payload?");
            }

            // Exemplo simplificado de agendamento usando uma abstração de fila baseada em Redis
            String jobId = jobScheduler.enqueueAt(
                schema.getSchedulerDatetime(), 
                "publish_event", 
                schema.getEventContent()
            );

            return ResponseEntity.ok(Collections.singletonMap("job_id", jobId));

        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Error during scheduler event... " + e.getMessage());
        }
    }
}
```

4.- Você ficou responsável por mentorar um novo membro do time (nível Júnior). Ele está finalizando um novo microsserviço em Java/Spring Boot e está com dúvidas quanto a possíveis "anti-patterns". Quantos anti-patterns você consegue identificar no código dele disponibilizado na pasta `anti_patterns` e por quais motivos?

5.- Tomando como base a estrutura do banco de dados fornecida (conforme diagrama [ER_diagram.png](ER_diagram.png) e/ou script DDL [1_create_database_ddl.sql](1_create_database_ddl.sql)) construa uma API REST em Java (Spring Boot) que irá criar um usuário. Os campos obrigatórios serão nome, e-mail e papel do usuário. A senha será um campo opcional; caso o usuário não informe uma senha, o serviço deverá gerar essa senha automaticamente. Siga as melhores práticas de pacotes (Controller, Service, Repository, DTO).

6.- Ajude-nos fazendo o ‘Code Review’ do código Java de um robô/rotina que exporta os dados da tabela “users” de tempos em tempos. O código foi disponibilizado na pasta `bot`. ***ATENÇÃO: Não é necessário implementar as revisões, basta apenas anotá-las em um arquivo texto ou em forma de comentários no código.***

7.- Qual ou quais Padrões de Projeto/Design Patterns você utilizaria em Java para normalizar serviços de terceiros (ex: disparos de e-mails ou SMS de múltiplos provedores)? Justifique sua escolha.

BOA SORTE!
