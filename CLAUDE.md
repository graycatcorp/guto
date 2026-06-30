# Guto — contexto do projeto (handoff)

App de **gestão de caixa** da GrayCat · Tupham. Web app de arquivo único (`index.html`),
sem build. Login + dados compartilhados via **Supabase**.

## Arquivos
- `index.html` — o app inteiro (HTML + CSS + JS embutidos; Chart.js e supabase-js via CDN).
- `.nojekyll` — para o GitHub Pages servir os arquivos sem processamento.
- `README.md` — passos de publicação.

## O que o app faz
- **Cadastro** central de custos (cadastra uma vez).
- **Extratos** mensais gerados automaticamente do cadastro:
  - Mensal: repete do "mês início" ao "mês fim" (ou Indeterminado = até Dez); datas iguais (dia padrão do Config).
  - Esporádico/Anual: cai no mês de referência; se **Parcelado**, espalha **1 parcela por mês** (1/3, 2/3, 3/3).
  - Variável: valor é prévia; pode-se lançar o **valor real** por ocorrência.
- **Dashboard**: mês atual (auto), total, por sócio (÷ nº de sócios), pago/a pagar, acumulado do ano, gráficos.
- **Aportes**: cada sócio vê quanto deve aportar no mês, marca data + "aporte feito" → consolida no dashboard.
- **Contábil/Anual**: resumo mensal, por categoria, fixo×variável, export CSV/JSON/PDF.
- Estado salvo: nuvem (Supabase, tabela `app_state`, linha `guto-graycat`) ou localStorage se as chaves estiverem vazias.

## Supabase (já configurado no index.html)
- `SUPABASE_URL = https://hzznxohbrwhgxuzvkwmr.supabase.co`
- `SUPABASE_ANON_KEY` = a **publishable key** (pública por design — pode ir no repo).
- ⚠️ A **secret key** NÃO entra no código nem no repositório. (Recomendado rotacioná-la no painel, pois foi exposta em chat.)
- Schema do banco: tabela única `app_state(id text pk, data jsonb, updated_at)` com RLS para usuários autenticados (arquivo `Guto_supabase_schema.sql` na conversa original).

## Próximos passos pedidos pelo Diego
1. **Publicar no GitHub Pages** com link próprio (sem domínio): criar repo público (ex.: `guto`), `git init/add/commit/push`, e habilitar Pages (branch main / root). Sugestão de usar `gh repo create ... --public --source=. --push` e depois `gh api` para ativar Pages.
2. Confirmar a URL no ar e o login dos 3 sócios funcionando.
3. **Personalização visual** (cores/logo da GrayCat).
4. Possível evolução: marcar "pago" e aportes por ocorrência já existem; avaliar relatório contábil mais completo e projeção de caixa.

## Como rodar/testar local
Abrir `index.html` no navegador. Se as chaves do Supabase estiverem preenchidas, abre em tela de login (modo nuvem); senão, modo local com seleção de perfil.
