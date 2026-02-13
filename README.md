# NCIA - Detecção de Anomalias em Áudio (DCASE)

Este projeto foca na detecção de anomalias em sons de máquinas industriais, utilizando datasets do desafio DCASE (2022/2024). O objetivo é identificar padrões anômalos em áudios para manutenção preditiva.

## 🗂️ Estrutura do Projeto

```
NCIA/
├── data/               # Dados brutos e processados (não versionados)
├── notebooks/          # Notebooks experimentais
├── src/                # Código fonte reutilizável
│   ├── denoise/        # Métodos de redução de ruído e filtragem
│   ├── features/       # Extração de características (Mel-Spectrograma, MFCC)
│   └── utils/          # Utilitários gerais
├── main.ipynb          # Notebook principal de orquestração
├── pyproject.toml      # Configuração de ferramentas (Ruff, Taskipy)
└── requirements.txt    # Dependências do projeto
```

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/MarquesLazaro/NCIA_Trabalho_2.git
   cd NCIA
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Como Usar

O fluxo principal está definido no arquivo `main.ipynb`. Certifique-se de que os dados do DCASE estejam na pasta `data/raw/` conforme esperado pelos scripts.

### Comandos de Automação

Este projeto utiliza **Taskipy** para gerenciar tarefas comuns de desenvolvimento.

*   **Verificar e corrigir estilo de código (Lint):**
    ```bash
    task lint
    ```
*   **Formatar código automaticamente:**
    ```bash
    task format
    ```
*   **Fazer ambos (Lint + Format):**
    ```bash
    task fix
    ```

## 🧩 Tecnologias

*   **Python 3.10+**
*   **Librosa**: Processamento de áudio.
*   **NoiseReduce**: Redução de ruído estacionário.
*   **Ruff**: Linter e formatador de código ultrarrápido.
*   **Taskipy**: Automação de tarefas simples.
