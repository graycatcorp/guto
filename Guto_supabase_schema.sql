-- ===========================================================
-- Guto — banco de dados (Supabase / PostgreSQL)
-- Cole tudo isto no Supabase: SQL Editor > New query > Run
-- ===========================================================

-- Tabela única que guarda todo o estado do app (custos, pagamentos, aportes, config)
create table if not exists public.app_state (
  id          text primary key,
  data        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

-- Linha compartilhada da empresa (mesmo ORG_ID usado no app)
insert into public.app_state (id, data)
values ('guto-graycat', '{}'::jsonb)
on conflict (id) do nothing;

-- Segurança: só usuários LOGADOS podem ler/gravar (os 3 sócios)
alter table public.app_state enable row level security;

drop policy if exists "socios leem"   on public.app_state;
drop policy if exists "socios gravam" on public.app_state;
drop policy if exists "socios criam"  on public.app_state;

create policy "socios leem"   on public.app_state
  for select to authenticated using (true);

create policy "socios gravam" on public.app_state
  for update to authenticated using (true) with check (true);

create policy "socios criam"  on public.app_state
  for insert to authenticated with check (true);
