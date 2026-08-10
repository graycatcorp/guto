# Guto — contexto do projeto (handoff)

App de **gestão de caixa** da GrayCat · Tupham. Web app de arquivo único (`index.html`),
sem build. Login + dados compartilhados via **Supabase**.

## Arquivos
- `index.html` — o app inteiro (HTML + CSS + JS embutidos; Chart.js e supabase-js via CDN).
- `.nojekyll` — para o GitHub Pages servir os arquivos sem processamento.
- `README.md` — passos de publicação.

## O que o app faz
- **Cadastro** central, com toggle **Custos | Receitas** (cadastra uma vez):
  - Custo: periodicidade Mensal/Anual/Esporádico, Fixo/Variável, parcelas, método, "cadastrado por".
  - Receita (modelo enxuto): descrição, valor previsto, Mensal (mesIni→mesFim) ou Pontual, forma de recebimento.
- **Extratos · Entradas e Saídas** mensais gerados automaticamente do cadastro:
  - Mensal: repete do "mês início" ao "mês fim" (ou Indeterminado = até Dez); datas iguais (dia padrão do Config).
  - Esporádico/Anual: cai no mês de referência; se **Parcelado**, espalha **1 parcela por mês** (1/3, 2/3, 3/3).
  - Variável: valor é prévia; pode-se lançar o **valor real** por ocorrência.
  - Saídas (custos) com tick **Pago?**; Entradas (receitas) com tick **Recebido?** + valor recebido real.
- **Dashboard**: mês atual (auto), custo, receita recebida, saldo do mês, pago/a pagar, acumulado, gráfico Custo×Receita + categoria, painel de fechamento.
- **Resultado & Fechamento** (substituiu "Aportes"): para o mês, mostra gastos previstos, receita recebida e o **saldo de fechamento = receita recebida − gastos previstos** (base "necessidade do mês"). Saldo **negativo** → aporte por sócio (÷ nº sócios); **positivo** → distribuição de lucro por sócio. Cada sócio marca o próprio aporte/retirada + data. Inclui painel **Contas & Instituições** (banco, tipo, saldo manual editável — pronto pra integração com o Inter depois).
- **Contábil/Anual**: resumo mensal (custo/receita/pago/saldo/sócio), resultado do ano, por categoria, fixo×variável, export CSV (entradas+saídas)/JSON/PDF.
- **Produtos**: centros de custo de Chat, Documentos, Estuda, Música, Design e Esportes. Cada feature usa o mesmo chassi analítico: artefatos entregues com custo efetivo e detalhamento clicável por provedor/serviço, fontes de receita em painel gêmeo, dependências, custos fixos e variáveis, cotas, coorte (gratuita/mista/premium), payback e gráfico de cenários (10/100/1.000/10.000/100.000 operações × 10/100/1.000/10.000/100.000/1.000.000 usuários). Premissas são editáveis e persistem no estado compartilhado.
- Estado salvo: nuvem (Supabase, tabela `app_state`, linha `guto-graycat`) ou localStorage se as chaves estiverem vazias. `migrate()` garante os campos `revenues`/`receipts`/`accounts` em estados salvos antes desta versão.

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
