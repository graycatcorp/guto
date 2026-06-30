# Guto — Handoff (continuação)

App de **gestão de caixa** da GrayCat (Projeto GUTO). Web app de **arquivo único**
(`index.html`), sem build, login + dados compartilhados via **Supabase**.
Ver também `CLAUDE.md` (contexto base do projeto).

> Última atualização desta sessão: tema vintage anos 60/70 + logo circular + pesquisa de
> integração bancária (Inter). Tudo commitado e pushado.

---

## 1. No ar / repositório
- **URL pública:** https://graycatcorp.github.io/guto/
- **Repo:** https://github.com/graycatcorp/guto (público, conta `graycatcorp`)
- **Pages:** branch `main` / root. Reconstrói automático a cada push (~1 min).

## 2. Arquivos
- `index.html` — o app inteiro (HTML + CSS + JS embutidos; Chart.js e supabase-js via CDN).
- `guto-mascote.png` — logo (senhor c/ máquina de escrever), recorte **circular**, fundo
  transparente. Gerado por `scripts/logo_circle.py`.
- `scripts/logo_circle.py` — regenera o logo a partir da arte original (ver cabeçalho do script).
  ⚠️ A arte original (`IMG_4855.PNG`) **não está no repo** — estava em `~/Downloads`. Se for
  trocar o logo, aponte o script para a nova arte. Params atuais: `cy_frac=0.42 r_frac=0.48`.
- `.nojekyll`, `README.md`, `Guto_SETUP.md`, `Guto_supabase_schema.sql`.

## 3. Estado atual da UI (tema vigente)
**Vibe anos 60/70 — "livro-caixa datilografado".**
- Paleta vintage em CSS vars (`:root` no topo do `<style>`): papel creme `--bg #efe6d2`,
  tinta `--ink/--txt #2c2317`, acentos **teal `--cyan #2f6e6a`** (primário), mostarda
  `--amber #c89a3c`, ferrugem `--red #b5432a`, oliva `--green #5f7d3a`.
- Fontes: `Special Elite` (`--disp`, títulos/logo), `Courier Prime` (`--ui`/`--mono`, corpo/números).
- Grafismo: molduras de formulário com borda entintada + **sombra dura deslocada**, réguas
  pontilhadas, réguas de livro-caixa no fundo (body), botões táteis. Gráficos com **contorno
  escuro grosso** (cara de desenhado), paleta retrô.
- **Login** (`#gate`): papel creme, "chuva" de caracteres datilografados (canvas `#matrix`,
  lenta, tinta desbotada), **GUTO** em Special Elite + mascote em emblema circular ao lado.
  Campos **"Operador (e-mail)"** e **"Senha"**.
- Histórico de temas (caso queira reverter/comparar): cyberpunk neon → claro "blueprint" →
  **vintage** (atual). Cada um foi um commit; ver `git log`.

> Truque do logo: o aro/sombra do emblema estão no CSS (`.brand-ico`, `.guto-ico`). A imagem
> já tem alpha circular. Para mexer no enquadramento, rode o script com outro `cy_frac`
> (menor = sobe) e/ou `r_frac`.

## 4. Funcionalidades-chave (além do CLAUDE.md)
- **Quem cadastrou cada custo:** ao criar um custo, grava `by` (sócio/operador logado) + `at`
  (data). Exibido na coluna **"Cadastrado por"** do Cadastro. Editar preserva o autor.
  Custos-semente antigos aparecem como "—". (Ver `c()`, `saveCost()`, `vCad()`.)
- **Login nuvem validado:** `readCreds()` valida e-mail/senha antes de chamar o Supabase
  (evita o erro "Anonymous sign-ins are disabled" quando o campo vinha vazio).

## 5. Nuvem / dados (Supabase)
- Tabela única `app_state(id, data jsonb, updated_at)`, linha `ORG_ID = "guto-graycat"`.
- `SUPABASE_URL` e `SUPABASE_ANON_KEY` (publishable) ficam no `index.html` (públicas por design).
- ⚠️ **Secret key** nunca vai pro código/repo (rotacionar no painel se exposta).
- `save()` faz upsert (debounce 400ms); `loadState()` lê na entrada. **Sem realtime**: outro
  sócio só vê mudanças ao recarregar (F5); last-write-wins.
- Modo local (localStorage) só se as chaves estiverem vazias.

## 6. Como rodar / testar
- Abrir `index.html` no navegador (com chaves preenchidas → tela de login nuvem).
- **Screenshot headless** (usado nesta sessão para validar visual):
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --window-size=1280,820 --screenshot=out.png --virtual-time-budget=2600 \
    "file:///Users/diegobranco/DevPrograms/guto/index.html"
  ```
- Para ver telas internas sem login: copiar o html zerando as 2 chaves do Supabase (vira modo
  local) e injetar no `load`: `currentUser={id:"admin",name:"Empresa"};view="dash";enter();`

---

## 7. PRÓXIMO TEMA EM ABERTO: integração bancária (Banco Inter PJ)

Objetivo do Diego: **plugar a conta PJ do Inter** e acompanhar entradas/saídas no Guto.

### Achados (pesquisa nesta sessão — confirmar na doc ao implementar)
**API oficial do Inter PJ** (developers.inter.co / inter.co/empresas/api-banking):
- ✅ **Pix**: enviar (Pix Cash-Out / pagamento) **e** receber (cobranças Cob/CobV + webhook).
- ✅ **Extrato/saldo** da conta corrente (consulta detalhada; PDF até 90 dias).
- ✅ **Pagamento de boletos** / agendamento.
- ❌ **Cartão de crédito** (fatura/transações item-a-item): **NÃO** exposto pela API do Inter.
  Vários custos do Guto são pagos no cartão → não viriam automático. Alternativas: marcar
  manual (atual), ou usar **agregador (Pluggy/Belvo)** que puxa cartão via Open Finance.
- Open Finance "oficial" direto **não** é viável num front estático (exige instituição
  participante, certificados, mTLS/FAPI, backend). Por isso: **API do próprio Inter** ou agregador.

### Arquitetura proposta (quando for implementar)
- **Backend = Supabase Edge Functions** (já temos Supabase; não subir servidor novo).
- Guardar **client id/secret + certificado** do Inter **no servidor** (env da function),
  nunca no `index.html`.
- Fluxo: consentimento/credenciais → **sync periódico** (ex.: cron/hora) → gravar em uma
  **nova tabela `transactions`** (ou outra linha jsonb) → tela no Guto de entradas/saídas.
- **Conciliação:** casar saídas do extrato com os custos cadastrados (auto-marcar "pago"
  quando bate valor/descrição/data).
- Atenção a **LGPD/segurança** (dado bancário sensível).

### Caminhos e decisão pendente
- **(A) Importação manual OFX/CSV** do extrato Inter → rápido, sem custo, sem backend.
  Bom primeiro passo: botão "Importar extrato" no Guto que lê o arquivo e lança movimentações.
- **(B) API do Inter automática** (Edge Function + tabela + conciliação) → mais trabalho,
  precisa criar a "Aplicação" no Internet Banking do Inter (gera credenciais + certificado).
- **(C) Agregador (Pluggy/Belvo)** → cobre **cartão** também, multi-banco, mas tem custo mensal.

**Aguardando o Diego decidir A, B ou C** (ou A agora + B depois).

---

## 8. Outras ideias/pendências
- Botão "Atualizar" (recarregar dados) na topbar p/ quando outro sócio mexeu (sem realtime).
- Migrar/atribuir autor aos 7 custos-semente antigos (hoje "—"), se desejado.
- Carimbo "PAGO" estilo borracha nos status (reforço visual do tema), se quiserem.
