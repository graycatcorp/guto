# Guto — Seu Painel Financeiro e Contábil

Mini-CRM de gestão de caixa para GrayCat · Tupham. Cadastro central de custos → extratos mensais automáticos → dashboard, aportes por sócio e visão contábil/anual.

## Usar agora (modo local)

Basta abrir o arquivo **`Guto_app.html`** no navegador (duplo clique). Já vem com seus 7 custos atuais e 3 sócios. Funciona offline.

No modo local os dados ficam salvos **só naquele navegador/computador**. Use **Contábil → Backup (JSON)** para guardar/levar os dados.

O que dá pra fazer:
- **Cadastro**: cadastra cada custo uma vez (tipo, periodicidade, classe, valor, período, parcelamento, método).
- **Extratos**: preenchidos automaticamente; marque **Pago** por mês e informe o **valor real** dos variáveis.
- **Aportes**: cada sócio vê quanto deve aportar no mês, a data e marca "aporte feito" — consolida no Dashboard.
- **Contábil/Anual**: resumo mensal, por categoria, fixo×variável, pago×a pagar e exportação (CSV/JSON/PDF).

---

## Ativar nuvem: login dos sócios + dados compartilhados entre computadores

Para os 2 sócios acessarem de máquinas diferentes com login próprio e verem os mesmos dados, ative o backend gratuito (Supabase). É uma configuração única.

**1. Criar o projeto (grátis)**
- Acesse supabase.com → crie conta → **New project**. Dê um nome e uma senha de banco. Aguarde ~2 min.

**2. Criar o banco**
- No projeto: menu **SQL Editor → New query** → cole o conteúdo de **`Guto_supabase_schema.sql`** → **Run**.

**3. Pegar as 2 chaves**
- Menu **Project Settings → API**. Copie:
  - **Project URL** (ex.: `https://xxxx.supabase.co`)
  - **anon public** key (uma chave longa)

**4. Colar no app**
- Abra `Guto_app.html` num editor de texto e preencha no topo:
  ```js
  const SUPABASE_URL = "https://xxxx.supabase.co";
  const SUPABASE_ANON_KEY = "cole_a_anon_key_aqui";
  ```
- Salve. Agora o app abre numa tela de **login**.

**5. Criar os logins dos sócios**
- Cada sócio abre o app e clica **Criar conta** (e-mail + senha). Pronto — todos compartilham os mesmos dados.
- Opcional: em **Authentication → Providers**, desligue "Confirm email" para entrar na hora sem confirmar e-mail.

**6. (Opcional) Deixar online com um link**
- Para um endereço fixo em vez de mandar o arquivo: arraste `Guto_app.html` (renomeie para `index.html`) em **app.netlify.com/drop**. Ele gera um link que os sócios acessam de qualquer lugar.

> A chave **anon** é pública por design (segura para o navegador). A proteção dos dados vem do login + regras (RLS) que o SQL já configura: só usuários autenticados leem/gravam.

---

## Observações
- A divisão por sócio é igual (÷ nº de sócios), ajustável em **Configurações**.
- "Marcar pago" e "valor real" são por mês/ocorrência (o que a planilha não fazia).
- No modo local, qualquer pessoa do computador escolhe um perfil; o controle por login só existe no modo nuvem.
