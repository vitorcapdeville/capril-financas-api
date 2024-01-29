# Meu Projeto FastAPI

Este é um projeto de backend usando FastAPI e SQLModel.

## Instalação

Para instalar as dependências do projeto, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Uso

Para iniciar o servidor, execute o seguinte comando:

```bash
uvicorn app.main:app --reload
```

## Testes

Para executar os testes, execute o seguinte comando:

```bash
pytest
```

## Docker

Para construir e executar a aplicação usando Docker, execute os seguintes comandos:

```bash
docker build -t meu-projeto-fastapi .
docker run -p 8000:8000 meu-projeto-fastapi
```

Acesse `http://localhost:8000` no seu navegador para ver a aplicação em execução.

## Contribuição

Pull requests são bem-vindos. Para mudanças importantes, por favor, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
```

Lembre-se de substituir as partes do texto que são específicas para o seu projeto.