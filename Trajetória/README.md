# Trajetória

Esta seção do projeto está focada nos aspectos de planejamento e execução das trajetórias do plotter 2D. Para isso, utiliza-se transformações das coordenadas cartesianas em coordenadas de comprimento de corda (diretamente relacionadas com o giro do motor). Dessa forma, é possível transformar uma trajetória cartesiana em rotativa, conforme a sincronização controlada dos dois motores.

## Funcionalidades do Código

A pasta de Trajetória contém alguns scripts que permitem a simulação e visualização das dinâmicas do sistema de plotter 2D. Abaixo estão descritas as funcionalidades de cada código incluído nesta seção:

1. **trajetória_controlavel.py**: Este script permite a interação dinâmica com o mecanismo do plotter através de controles deslizantes, possibilitando a alteração dos comprimentos dos fios. Os usuários podem observar como essas mudanças afetam o movimento e a posição da caneta (ponto C).

2. **area_de_trabalho.py**: A partir dos tamanhos máximos definidos para as cordas, este código calcula e exibe a área de trabalho do sistema. Isso representa os pontos dentro do espaço que o plotter consegue alcançar, servindo como verificação da possibilidade de ser traçada uma circunferência e um triângulo.

3. **trajetoria_triangulo.py**: Este script transforma coordenadas cartesianas de entrada em coordenadas de comprimento de corda de maneira a formar um triângulo, alterando os comprimentos das cordas de forma adequada. 

4. **trajetoria_circunferencia.py**: Similar ao script de triângulo, este realiza transformações para criar uma trajetória circular. A circunferência é discretizada em segmentos lineares, permitindo que o plotter trace caminhos circulares com precisão.

5. **monalisa_test.py**: Executa um teste avançado que envolve a serialização e processamento de um arquivo SVG pré-processado, `monalisa.svg`, para desenhar a silhueta da Mona Lisa. O script aplica os mesmos princípios de transformação e controle de trajetória utilizados pelos outros códigos, demonstrando a capacidade do sistema de plotar imagens complexas.

## Instalação de Bibliotecas Necessárias

Este projeto depende de algumas bibliotecas Python. Abaixo estão as instruções para instalação usando diferentes gerenciadores de pacotes.

### Usando pip

Caso utilize `pip`, instale as bibliotecas diretamente com os seguintes comandos:

```bash
pip install svgpathtools
pip install numpy
pip install matplotlib
```

### Usando conda

Se preferir usar o `conda`, você pode instalar as bibliotecas da seguinte forma. Note que `svgpathtools` está disponível em `conda-forge`.

```bash
conda install numpy
conda install matplotlib
conda install -c conda-forge svgpathtools
```

## Executando o Projeto

Basta fazer execução dos códigos da pasta.
