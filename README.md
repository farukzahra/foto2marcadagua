# foto2marcadagua

Este projeto adiciona uma marca d'água com a localização GPS nas fotos de uma pasta.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação das dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install pillow exifread
```

## Como usar

1. Coloque suas fotos na pasta `fotos_originais/`.
2. Execute o script principal:

```bash
python index.py
```

3. As fotos com marca d'água serão salvas na pasta `fotos_com_marcadagua/`.

## Observações
- O script só adiciona marca d'água em fotos que possuem informações de localização GPS.
- A fonte utilizada é a Arial. Caso não esteja disponível no seu sistema, será usada a fonte padrão do Pillow.

## Personalização
Se quiser mudar o texto, tamanho da fonte ou estilo da marca d'água, edite a função `adicionar_marcadagua` no arquivo `index.py`. 