---
description: Regra Global - Como editar ou ler arquivos Jupyter Notebook (.ipynb) de forma segura no projeto
---

# Regra Global de Edição de Notebooks
**ESTA É UMA REGRA CRÍTICA PARA ESTE WORKSPACE.**

O Antigravity (e outras ferramentas base text-replace) **NUNCA** deve usar ferramentas diretas de substituição de string/edição em linha de arquivos que terminam em `.ipynb` neste projeto. A edição em formato texto puro resulta em quebra da estrutura JSON requerida pelo Jupyter.

Sempre que a intenção do usuário for alterar, investigar ou criar código dentro de um `notebook`, utilize EXCLUSIVAMENTE o utilitário local da raiz do projeto: `notebook_helper.py`.

## Fluxo de Trabalho (Workflow / Steps):

1. **Listar as células para se orientar:**
   Execute via terminal (`run_command`): `python notebook_helper.py list [nome_do_notebook.ipynb]`
   
2. **Avaliar e Ler a célula alvo:**
   Execute via terminal (`run_command`): `python notebook_helper.py read [nome_do_notebook.ipynb] [índice]`

3. **Editar uma célula (Exigido pelo Helper):**
   - O comando de edição não aceita alterações fáceis enviadas puramente em string via shell (devido a eventuais quebras de aspas simples/strings formatadas no terminal). 
   - A ferramenta EXIGE o uso de `--source_file`. 
   - **Passo A:** Escreva o código atualizado ou refeito em um arquivo python temporário (ex: `c:\Users\alef.monteiro\PycharmProjects\NCIA_Trabalho_2\temp_edit.py`). Use a ferramenta segura de escrita de arquivos regular (suporta texto puro).
   - **Passo B:** Rode o utilitário executando `python notebook_helper.py edit [nome_do_notebook.ipynb] [índice] --source_file temp_edit.py`.
   - **Passo C:** Exclua ou limpe o arquivo `temp_edit.py` em seguida via terminal para manter a limppeza do projeto.

4. **Para adicionar código (Insert):**
   - Caso queira criar uma nova célula, repita a operação de criar um arquivo Python puro temporário com o novo código e usar `insert --source_file`: 
     `python notebook_helper.py insert [nome_do_notebook.ipynb] [índice] code --source_file temp_insert.py`

5. **Para deletar:**
   - Execute: `python notebook_helper.py delete [nome_do_notebook.ipynb] [índice]`

## Aviso para o Agente:
Se o usuário lhe pedir para modificar um Notebook, siga explicitamente este processo usando a ferramenta `run_command` sobrepondo os comandos python para manter estabilidade absoluta do projeto da IA.
