Manual para utilizar o Backend (Python com Django e BeautifulSoup)

Antes de iniciar, certifique-se de que o Docker está instalado em sua máquina. 
Visite https://www.docker.com/ para instruções de instalação.

1. Construindo a Imagem Docker
    1.1 Navegue até o diretório do projeto backend no terminal.

    1.2 Construa a imagem Docker usando o seguinte comando:
        docker build -t wheretobuygames-backend .
    Isso criará uma imagem Docker com o nome wheretobuygames-backend.

2. Executando o container Docker
    2.1 Após a construção da imagem, inicie o contêiner usando:
        docker run -p 8000:8000 wheretobuygames-backend

    2.2 O backend agora estará acessível em http://localhost:8000.

3. Dicas adicionais:
    - Se você modificar o código fonte, precisará reconstruir a imagem Docker para refletir as mudanças.
    - Para verificar os contêineres em execução, use docker ps.
    - Para parar um contêiner, use docker stop [CONTAINER_ID].