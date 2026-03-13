# Shipay Back-End Engineer Challenge (Versão .NET 8)

***Nota: Utilizaremos os seguintes critérios para a avaliação: Desempenho, Testes, Manutenabilidade e boas práticas de engenharia de software (especialmente padrões C#/.NET).***

1.- Sua squad irá desenvolver uma nova funcionalidade que irá prover um serviço de validação de cadastro de clientes. Ao informar o CNPJ e o CEP do endereço do cliente, iremos consultar duas APIs de terceiros: a primeira retornará informações da empresa de acordo com o CNPJ e a segunda API retornará detalhes de um endereço a partir de um CEP. Com os resultados das duas APIs, iremos comparar o endereço do cadastro da empresa obtido pelo CNPJ com o endereço obtido através da consulta do CEP e verificar se as informações de unidade federativa, cidade e logradouro coincidem. Caso coincidam, retornaremos HTTP 200, caso contrário, um HTTP 404.
Como este novo serviço deverá ser resiliente e essencial para os nossos cadastros, a solução proposta deverá permitir retentativas automáticas em casos de falhas e o chaveamento entre dois provedores de resolução do endereço pelo CEP (fallback), ou seja, usaremos a API de um provedor como padrão e caso o serviço esteja fora do ar, o serviço proposto deverá chamar o segundo provedor automaticamente após "N" tentativas.
Apesar de depender do consumo de múltiplas APIs de terceiros, a resposta do serviço desenvolvido deverá ser síncrona.
Você pode verificar exemplos das APIs utilizadas em [requests_e_responses_apis_questao_1.json](requests_e_responses_apis_questao_1.json).
Implemente o referido serviço em .NET 8.

BOA SORTE!