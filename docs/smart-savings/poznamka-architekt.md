# Tech poznámky — savings goal service / integrace

**Autor:** Tomáš H. (Solution Architect)\
**Datum:** 5. 6. 2025\
**Status:** draft, nekompletní

------------------------------------------------------------------------

## Core banking (CBS) integrace

CBS = SAP Banking (verze 9.0, upgrade na 10 plánovaný Q1/2026, NEMIGROVAT teď).

Účty:

- BÚ (běžný účet) — standardní, read/write přes CBS API
- SÚ (spořicí účet) — SavingsAccount entita, limit 3 per klient (CHECK constraint, tbl_savings_plan). Změna = DB migrace, change window 1. víkend v měsíci.
- Sub-účty / earmarking — CBS NEPODPORUJE. Pokud chceme earmarking, musíme si to držet v naší DB a renderovat na FE. CBS o tom nebude vědět.

Transakce:

- Interní převody BÚ→SÚ jdou POUZE přes batch processing. Batch runy: 06:00, 12:00, 18:00. Žádný real-time pro interní převody.
- Karetní tx jsou real-time (přes PG — payment gateway), ale to je jiný flow, nesouvisí.
- Max 15 interních tx / den / klient (hard limit v CBS, prý kvůli fraud prevention). Pokud chceme víc, musíme žádat o výjimku u CBS týmu — vyřizování cca 6–8 týdnů.

API:

- CBS REST API — rate limit 100 req/min per API key (ne per user!). Při překročení 429 + 60s cooldown.
- transaction-history-api — max 90 dní zpětně, stránkování po 50 záznamech. Pozor: nevrací pending tx, jen settled.
- Není webhook/push pro změny zůstatku. Musíme pollovat nebo se napojit na event bus (Kafka topic `account.balance.changed`, ale je to fire-and-forget, žádná garance doručení).

## Notifikace

Existující notif systém (NotifHub):

- Push notifikace přes FCM/APNS
- Fronta (RabbitMQ), průměrná latence 15–30 min, peak 2h+ (páteční odpoledne, pondělní ráno)
- Prioritní fronta existuje, ale je vyhrazená pro security alerts (OTP, podezřelé transakce). NEPOUŽÍVAT pro business notifikace.
- Rate limit: max 5 push notifikací / den / uživatel (anti-spam policy, definuje product, ne tech)

## ML model hosting

Doporučení: separátní microservice (recommendation-engine).

- Python/FastAPI, kontejnerizovaný v K8s
- Model: pro MVP stačí rule-based (průměr příjmů - pravidelné výdaje - buffer = doporučená částka). ML model nasadíme ve fázi 2, až budeme mít dost dat.
- POZOR: pro trénink ML modelu potřebujeme anonymizovaná data. GDPR — nelze použít produkční data bez anonymizace. ETL pipeline na anonymizaci zatím NEMÁME, museli bychom vybudovat.

## Otevřené otázky

- Earmarking vs. fyzický převod — závisí na tom, jestli CBS tým stihne zrušit limit 3 plánů do MVP deadline
- Consent flow pro analýzu transakcí — čeká se na legal
- Monitorování accuracy modelu — kdo to bude dělat? DS tým nemá kapacitu na ongoing monitoring
- Co se stane s earmarkovanými penězi, když uživatel zruší cíl? (nikdo tohle zatím neřešil)
- Shared/joint accounts — CBS API pro ně vrací jiné response structure, nepodporováno v MVP? potvrdit s PM
