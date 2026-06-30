# Guto — Painel Financeiro e Contábil (GrayCat · Tupham)

App web (arquivo único) hospedado no GitHub Pages. Login e dados compartilhados via Supabase.

## Publicar (uma vez)

1. **github.com** → canto superior direito **+ → New repository**.
   - Nome: `guto` (ou o que preferir)
   - Visibilidade: **Public** (o GitHub Pages grátis exige repositório público — é seguro: o app só guarda a *publishable key* do Supabase, que é pública por design; os dados ficam protegidos por login).
   - Clique **Create repository**.
2. Na página do repo: **Add file → Upload files** → arraste o **`index.html`** (e, se quiser, o `.nojekyll` e este `README.md`) → **Commit changes**.
3. **Settings → Pages** → em "Source" escolha **Deploy from a branch** → branch **main** / pasta **/ (root)** → **Save**.
4. Aguarde ~1 minuto e atualize a página de Pages: aparece o link, tipo
   **`https://SEU-USUARIO.github.io/guto/`**.

Pronto — você e os sócios acessam esse link de qualquer lugar. Cada um cria conta na primeira vez (e-mail + senha) e todos veem os mesmos dados.

## Atualizar depois

Quando eu te passar um `index.html` novo:
- Repo → **Add file → Upload files** → arraste o novo `index.html` → **Commit changes**.
- O site republica sozinho em ~1 min.

## Observações
- O `.nojekyll` garante que o GitHub Pages sirva o arquivo sem processamento extra.
- Configurações do Supabase já estão embutidas no `index.html` (URL + publishable key).
- Recomendado no Supabase: **Authentication → Providers → Email → desligar "Confirm email"** para os sócios entrarem direto.
