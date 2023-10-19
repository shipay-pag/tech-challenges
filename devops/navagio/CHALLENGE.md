# Shipay DevOps Challenge 


## Observações: 

O teste foi desenvolvido para entender como o candidato pensa em diferentes situações. Não é um teste objetivo e existem várias soluções corretas para os problemas propostos. Queremos saber como é o seu modo de trabalho. 


## Dicas:

* use mensagens de commit consistentes.
* aplique boas praticas que já trabalhou ou leu em documentações.
* faça as mudanças que achar necessário na estrutura de repositório. 
* não se atenha a esse repositório, caso prefira, separe em dois ou mais.
* mantenha a calma que vai dar bom. 


## Introdução

Nesse repositório está presente o código fonte de duas aplicações, ambas em Python e utilizando poetry como gerenciador de dependências. O serviço `api_rest` prove uma API que responde a um GET na porta 8000 e o serviço `async_worker` envia e processa eventos em um canal do Kafka(o Kafka É uma dependência externa dessa aplicação).


## Instalando dependências

```
# change dir to service dir
poetry shell
poetry install
```


## Desafios:

1. Containerização: crie uma imagem de Docker base, e extenda sua imagem para cada aplicação. Instale uma cadeia de certificados publica qualquer na base padrão ex: Comodo SSL, DigiCert, Entrust Datacard, GoDaddy, etc.. Nas imagens extendidas, instale as dependências, e configure a imagem para utilizar o comando `ENTRYPOINT` para iniciar as aplicações. Documente o processo de build e run nos devidos arquivos, e.g. `README.md`.

    Bônus: Dependências externas da aplicação podem subir a parte com um `docker-compose.yaml`.

2. Empacotamento: baseado no repositório apresentado, crie um Helm chart contendo todos os componentes necessários para essa aplicação rodar em um cluster de Kubernetes local (kind, minikube, Kubernetes Docker Desktop). Você pode utilizar Kustomize caso se sentir a vontade. A aplicação `api_rest` precisa estar acessível por um `Service` do Kubernetes (ClusterIP) na porta 443. A aplicação `async_worker` não precisa de um `Service` do Kubernetes. 

    Bônus: A instancia da aplicação `api_rest` performa bem em ec2 com a label `shipay.com.br/capacity-type = spot` enquanto a aplicação `async_worker` só pode rodar em ec2 com a label `shipay.com.br/capacity-type = ondemand`. Configure Affinity's para garantir melhor distribuição dos workloads.

3. Pipeline: o candidato pode optar por uma entre duas opções para o desafio de pipeline. Uma pipeline de build ou uma pipeline de deploy. Nessa parte do desafio, não é importante se ater a tecnologia. Utilize o que se sentir confortável: GitlabCI, Jenkis, TravisCI, CircleCI, Github Actions, Tekton, DroneCI, JenkinsX, Spinnaker, Codefresh, ArgoCD, etc.. É preferível utilizar ferramentas aderentes ao fluxo de versionamento gitflow, mas não é mandatário. É imprescindível a necessidade de versionamento da pipeline como código. Para builds, escreva uma pipeline para buildar as imagens de docker e enviar para o dockerhub público. Apesar de o repositório ter a estrutura de `monorepo`, não é necessário que os builds das aplicações sejam trigados individualmente e.g. cada trigger handler pode buildar as 3 imagens e enviar para as 3 imagens o repositório de imagens. Para deploy, utilize a estratégia de empacotamento utilizada no passo anterior para implantar as aplicações e suas dependências externas.  

    Bônus: Implemente ambas as pipelines.

4. Responda as questões abaixo em um arquivo chamado ANSWERS.md
* a) O que é uma sub-rede e por que é usada em uma VPC?
* b) Descreva o conceito de balanceamento de carga e porque ele é importante em uma arquitetura de nuvem.
* c) Como um servidor proxy funciona para intermediar as solicitações entre os clientes e os servidores de destino?
* d) O que é NAT e qual é o seu propósito em uma rede?
* e) Explique nas suas palavras, o que acontece quando você acessa um site no seu browser por baixo dos panos?

    obs: Não responder todas as questões não é impeditivo, essa etapa consiste em avaliar o conhecimento em infraestrutura do candidato. 

5. Considere um diretório com diversos arquivos que são adicionados diariamente;
    ```
    $ ls 
    $ ARQUIVOS  ARQUIVOS_PROCESSADOS
    $ ls ARQUIVOS/
    $ log_para_processamento_1.log  log_para_processamento_2.log  log_para_processamento_3.log  log_para_processamento_4.log
    ```

    Faça um script que movas os arquivos para um diretório de arquivos processados e renomeie todos os arquivos movidos incluindo o dia e horário sem pontos no nome. Log no terminal todas as etapas do processo.

6. Agende a execução periódica desse script para uma vez ao dia e nos mande o processo de configuração.


Boa Sorte.