# Shipay DevOps Challenge 


## Observações: 

O teste foi desenvolvido para entender como o candidato pensa em diferentes situações. Não é um teste objetivo e existem várias soluções corretas para os problemas propostos. Queremos saber como é o seu modo de trabalho. 


## Dicas:

* aplique boas praticas que já trabalhou ou leu em documentações.
* não se atenha a esse repositório, caso prefira, separe em dois ou mais.
* mantenha a calma que vai dar bom. 


## Introdução

Dentro do repositório tem uma aplicação Flask bem simples, é uma API que responde "pong" à rota api/ping.


#### Para executar a aplicação é necessário python 3.11 e rodar os seguintes comandos:
    ```
    # change dir to service dir
    $ pip install pipenv
    $ pipenv install
    $ pipenv run python start.py runserver
    ```

#### Para executar os testes da aplicação rode o comando:
    ```
    # change dir to service dir
    $ BASE_API_ENV=test pipenv run pytest
    ```


## Desafios:

1. Você deverá Dockerizar a aplicação garantindo que o Dockerfile esteja otimizado e com boas praticas de segurança.

    Bônus: A partir do Dockerfile criado, faça o build e envie a imagem para o Dockerhub, crie um deployment utilizando essa imagem e descreva o processo para aplicar o yaml em um cluster de Kubernetes.

2. Agora, imagine que você está assumindo a responsabilidade pela infraestrutura de uma empresa que possui ambientes de produção e desenvolvimento em um Cloud Provider (Escolha AWS ou GCP). Sua tarefa é desenhar a arquitetura de rede, garantindo a segurança e isolamento adequado entre os ambientes. Além disso, é necessário criar um diagrama de rede que represente essa estrutura.
    
    ##### Máquinas:
    * Ambiente de Produção: 300 máquinas
    * Ambiente de Desenvolvimento: 150 máquinas

    ##### Isolamento de Ambientes:
    * Ambos os ambientes devem compartilhar a mesma VPC (Virtual Private Cloud).
    * Garanta que não haja comunicação direta não autorizada entre as máquinas dos ambientes de produção e desenvolvimento.
  
    ##### Diagrama de Rede:
    * Crie um diagrama de redes que represente a infraestrutura proposta.
    * Destaque claramente as VPCs, sub-redes, e máquinas em cada ambiente.
    * Destaque qual o range de IP utilizado em ambos os ambientes.
    * Inclua detalhes sobre gateways, firewalls, e quaisquer outros componentes relevantes.

    ##### Segurança:
    * Implemente medidas de segurança apropriadas para proteger a rede.
    * Considere o uso de grupos de segurança, listas de controle de acesso (ACLs), e outras práticas recomendadas.

3. Considere um diretório com diversos arquivos que são adicionados diariamente;
    ```
    $ ls 
    $ ARQUIVOS  ARQUIVOS_PROCESSADOS
    $ ls ARQUIVOS/
    $ log_para_processamento_1.log  log_para_processamento_2.log  log_para_processamento_3.log  log_para_processamento_4.log
    ```

    Faça um script que movas os arquivos para um diretório de arquivos processados e renomeie todos os arquivos movidos incluindo o dia e horário sem pontos no nome. Log no terminal todas as etapas do processo.

4. Agende a execução periódica desse script para uma vez ao dia e nos mande o processo de configuração.


Boa Sorte.