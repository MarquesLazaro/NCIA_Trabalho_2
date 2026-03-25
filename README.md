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

*   **Ativar Pre-commit (Proteção de git):**
    Garanta que o pre-commit esteja instalado para verificar seu código antes de cada commit.
    ```bash
    pre-commit install
    ```

## 🎧 Pipeline de Processamento de Áudio

O projeto implementa um pipeline robusto para tratamento dos dados antes do treinamento:

1.  **Denoising (Redução de Ruído)**: Aplicação de filtro High-Pass e redução de ruído estacionário para limpar o sinal bruto.
2.  **Padding (Padronização)**: Todos os áudios são ajustados para ter exatamente 10 segundos (240.000 amostras a 24k Hz).
3.  **Extração de Features**:
    *   **Mel-Spectrograma**: Extraído do áudio limpo e padronizado.
    *   **MFCC**: Calculado corretamente a partir do Mel-Spectrograma **bruto** (antes da normalização).
4.  **Normalização**: Aplicação de Min-Max Scaling [0, 1] individualmente para cada feature antes de alimentar o modelo.

## 🤝 Workflow e Branches

Para manter a organização e evitar conflitos, cada membro da equipe deve trabalhar em sua própria branch antes de enviar código para a `main`.

### Branches Ativas

*   **`main`**: Código estável e versão de produção.
*   **`lazaro`**: Branch de desenvolvimento do Lazaro.
*   **`giovana`**: Branch de desenvolvimento da Giovana.
*   **`alef`**: Branch de desenvolvimento do Alef.

### Fluxo de Trabalho Recomendado

1.  Mude para sua branch: `git checkout <seu-nome>`
2.  Faça suas alterações e commits.
3.  Atualize sua branch com a main: `git merge main` (para resolver conflitos localmente).
4.  Envie para o remoto: `git push origin <seu-nome>`
5.  Abra um **Pull Request (PR)** no GitHub da sua branch para a `main`.

## 🧩 Tecnologias

*   **Python 3.10+**
*   **Librosa**: Processamento de áudio.
*   **NoiseReduce**: Redução de ruído estacionário.
*   **Ruff**: Linter e formatador de código ultrarrápido.
*   **Taskipy**: Automação de tarefas simples.
