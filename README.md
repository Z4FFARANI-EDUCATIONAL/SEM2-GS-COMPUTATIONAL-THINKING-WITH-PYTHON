![banner](./assets/banner.png)

# INTEGRANTES:
- **[Guilherme Santos Nunes](https://github.com/sannunez)**
- **[Kaique Zaffarani](https://github.com/Z4ffarani)**

## LINKS
- **[VÍDEO EXPLICATIVO](https://youtu.be/5BdzgsT5DlY)**

<br>

# PROJETO
Com o objetivo de contribuir para a sustentabilidade e a redução das emissões de CO2, a empresa fictícia Econy desenvolveu uma plataforma que integra o comércio de créditos de carbono e certificações de auditoria por meio de smart contracts (contratos inteligentes) e blockchains (tecnologia de registro distribuído e descentralizado) que utilizam o algoritmo de consenso PoS (Proof-of-Stake).

Este projeto tem como foco a criação de um sistema que simula transações de créditos de carbono, onde as empresas podem registrar suas ações e obter validações de suas práticas ambientais. As transações, registradas em blocos criptografados, podem ser validadas por participantes da rede, ganhando stakes (poder de participação para validações de Blocos) e garantindo a segurança e o rastreamento de cada movimentação. Além disso, a plataforma oferece uma interface interativa para empresas monitorarem suas ações e manterem conformidade com o mercado de carbono.

O programa é composto por três sistemas principais:

- **Comercialização de créditos de carbono** | Permite que empresas comprem, vendam ou cambiem créditos de carbono com o governo dos blocos econômicos a que pertencem.
- **Certificações de sustentabilidade** | Oferece uma solução para a validação de ações ambientais das empresas por meio de auditorias terceirizadas. As certificações obtidas podem ser usadas pelas empresas para comprovar suas práticas sustentáveis.
- **Blockchains** | A base de segurança e descentralização do sistema, onde tipos de transação de créditos de carbono e certificações de sustentabilidade das empresas são registradas em arquivos binários.

<br>

# INSTRUÇÕES
1. Em um terminal, clonar o repositório:
```bash
git clone https://github.com/Z4FFARANI-EDUCATIONAL/SEM2-GS-COMPUTATIONAL-THINKING-WITH-PYTHON.git
```

2. No terminal, navegar até a pasta do projeto:
```bash
cd SEM2-GS-COMPUTATIONAL-THINKING-WITH-PYTHON
```

3. No terminal, executar o arquivo `main.py` exibirá um menu interativo perguntando informações sobre o nome e setor de atuação da empresa a registrar. Depois, ela poderá escolher entre comprar, vender, cambiar créditos de carbono, obter certificações, consultar blockchains ou entender mais sobre a proposta da plataforma.
   
4. Após as opções de comercialização de créditos de carbono, a empresa registrada escolhe o bloco econômico em que participa e depois informa a quantidade de créditos de carbono. O sistema converte a quantidade para dólares a partir da cotação do bloco econômico escolhido.

5. Dependendo do tipo de transação, a empresa informa o vendedor ou o comprador de créditos de carbono.

6. Quando uma transação ou certificação é finalizada, baseada no conceito de smart contracts, ela é armazenada como um bloco (objeto de dados) que contém um hash (identificador criptográfico que permite "acorrentar" os blocos) em um arquivo binário dedicado ao tipo de transação, com todas as informações relacionadas. Caso o arquivo binário ainda não exista, cria-se um novo, consolidando um genesis block (primeiro bloco de uma blockchain).

<br>

# FUNÇÕES
`main.py`:
- **Block** | Classe que define um bloco na blockchain, contendo índice, timestamp, dados transacionais, hash atual e anterior, além do validador.
- **calculate_hash** | Função que gera um hash único para cada bloco utilizando o algoritmo SHA-256.
- **Validator** | Classe que representa participantes no processo de validação de blockchains, incluindo empresas e um centro de dados governamental.
- **initialize_validators** | Função que inicializa os validadores das blockchains (de acordo com a quantidade de stakes), incluindo a empresa principal e outros participantes.
- **Blockchain** | Classe que representa a estrutura principal da cadeia de blocos, armazenando principais informações sobre transações e garantindo a validade dos dados.
- **load_chain / save_chain** | Funções que carregam e salvam o estado da blockchain localmente em arquivos binários, garantindo persistência de dados.
- **select_validator** | Função que seleciona validadores para adicionar blocos à blockchain, com base na quantidade de stakes dos participantes.
- **add_block** | Função que adiciona novos blocos às blockchains, associando-os ao hash do bloco anterior e salvando os dados transacionais.
- **is_valid** | Função que valida a integridade da blockchain definida, verificando se os hashes de cada bloco correspondem e se a cadeia dela está intacta.
- **debug_chain** | Função que exibe detalhes da blockchain, incluindo índice, timestamp, dados e hashes, para depuração.
- **execute_transaction** | Função que gerencia transações de créditos de carbono, incluindo compra, venda, troca e obtenção de certificações, gerando e adicionando blocos com os dados.
- **main** | Função que gerencia o fluxo principal do sistema, incluindo menus interativos para consulta de saldo, transações de créditos de carbono e consulta de blockchains.

<br>

# OBSERVAÇÕES
- Este projeto não tem relação direta com algum mercado de carbono oficial, nem com as empresas, ou quaisquer auditorias e certificações que compõem.
- Alguns valores dispostos no sistema não condizem com a realidade e apenas servem para fins educativos.
- Bibliotecas essenciais foram instaladas para criação de hashes, registro de tempo, manipulação de arquivos binários, acesso raso ao sistema operacional e sorteio de variáveis.
- É possível encerrar o sistema a qualquer momento facilmente.
- Os textos exibidos durante a execução do sistema não estão indentados no arquivo `main.py` para melhor visualização. 
- Três empresas fictícias foram adicionadas ao sistema para fins experimentais, além de um centro de dados governamental qualquer. Empresas com 0 stake não participarão do processo de validação. Quanto maior for a quantidade de stakes que uma empresa tiver, maior a chance de ser escolhida para validação.
- É possível que a empresa inserida seja escolhida para validar um bloco. Portanto, é importante estar atento às informações de registro de blockchains.
- Arquivos binários são criados fora da pasta do projeto, sendo utilizados para armazenar e carregar todos os tipos de transações e podendo ser excluídos, se for preferível.
- O sistema foi desenvolvido parcialmente com orientação a objetos.

<br>

# TECNOLOGIAS
**[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)**

<br>

# REFERÊNCIAS
- **[Dá pra COPIAR e COLAR BITCOIN? Entenda BLOCKCHAIN](https://www.youtube.com/watch?v=0Mt16eeCv78)**
- **[Crie sua PRÓPRIA CRIPTOMOEDA](https://www.youtube.com/watch?v=IkXIA1NNocY&t=13s)**
- **[Desvendando a Blockchain](https://www.sp.senai.br/inscricaogratuita/desvendando-a-blockchain/87241/403/29279)**
- **[Construa sua própria Blockchain com Python: Tutorial Passo a Passo](https://www.youtube.com/watch?v=yBuzx8akAd0)**
- **[CarbonCredits.com](https://carboncredits.com)**
