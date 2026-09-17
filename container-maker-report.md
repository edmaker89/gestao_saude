# Relatório de containerização

## Análise

- Linguagens: python
- Gerenciadores de dependências: pip
- Serviços:
  - app (.): linguagem python, portas [5000, 8080, 9000, 8000, 587], entrypoints ['app/app.py']

## Artefatos gerados

- Dockerfile
- docker-compose.yml
- k8s/configmap.yaml
- k8s/secret.yaml
- k8s/deployment-app.yaml
- k8s/service-app.yaml
- k8s/deployment-db.yaml
- k8s/service-db.yaml
- k8s/pvc.yaml

## Decisões

**Decisões**

- **Imagem base**: A análise identifica linguagem Python e gerenciador de dependências `pip`. Com base nisso, a containerização do serviço `app` foi orientada para uma imagem base compatível com Python. O artefato `Dockerfile` gerado materializa essa escolha; versão exata ou variante da imagem não está detalhada na análise fornecida.

- **Estrutura dos serviços**: A análise detectou um único serviço de aplicação, denominado `app`, localizado na raiz do repositório, com entrypoint `app/app.py`. Os artefatos Kubernetes também incluem um serviço de banco de dados (`deployment-db.yaml`, `service-db.yaml`, `pvc.yaml`), indicando a decisão de prover persistência via PVC. Para orquestração local, foi gerado `docker-compose.yml`. Como a análise fornecida não lista o banco de dados entre os serviços detectados, não há informações sobre sua linguagem, imagem ou portas.

- **Portas**: A análise lista as portas `5000, 8080, 9000, 8000, 587` para o serviço `app`. A exposição de portas deve considerar essa lista; contudo, sem o conteúdo dos manifestos de serviço e do `docker-compose.yml`, não é possível afirmar quais portas foram efetivamente publicadas ou qual é a porta principal da aplicação.

- **Variáveis de ambiente**: Foi adotada a separação entre configuração não sensível e sensível por meio dos artefatos `k8s/configmap.yaml` e `k8s/secret.yaml`. Os nomes e valores específicos das variáveis não estão presentes na análise.

**Limitações encontradas**

- A análise determinística não contempla o serviço de banco de dados, embora os artefatos gerados incluam manifestos para ele.
- Não há detalhes sobre versão da imagem base, dependências Python, comando de inicialização ou variáveis de ambiente.
- A lista de portas é ambígua quanto às funções de cada porta, impossibilitando confirmar a real necessidade de exposição de todas.
- A avaliação está limitada à lista de artefatos e aos dados da análise; o conteúdo efetivo dos arquivos gerados não foi fornecido.

## Limitações

- Nenhuma limitação detectada