# fullstack-pro-max

[![CI](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml/badge.svg)](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/0x61A/fullstack-pro-max)](https://github.com/0x61A/fullstack-pro-max/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

*English version: [README.md](README.md)*

Gerçek bir web ürününü uçtan uca çıkarmak için tek parça, kendi kendine yeten bir [Claude Code](https://claude.com/claude-code) skill'i — özgün (şablon görünümlü olmayan) UI/UX, backend mimarisi, veritabanı & auth, deployment, test, siber güvenlik, SEO, reklam, e-ticaret ödemeleri, AI özellik entegrasyonu, analitik, e-posta ve i18n/yerelleştirme. Tek bir sabit frontend+backend ikilisine kilitlenmek yerine projeye göre uyarlanan stack seçimi yapar.

İki kullanım senaryosu için tasarlandı: ajans/müşteri teslimatı ve kişisel SaaS projeleri.

## İçinde ne var

On üç modül; her biri yapılandırılmış veri (CSV), ihtiyaç anında yüklenen referans dokümanları ve yalnızca stdlib kullanan Python script'leriyle destekleniyor:

| Modül | Kapsam |
|---|---|
| **Backend & API** | Uyarlanabilir stack seçimi (Next.js/Express/Nest.js/Fastify · FastAPI/Django · Supabase/Firebase · Cloudflare Workers), API tasarımı, hata yönetimi |
| **Veritabanı & Auth** | Şema tasarımı, RLS/multi-tenancy, auth strateji matrisi, güvenli migration |
| **DevOps & Deployment** | CI/CD, Vercel/Netlify/Cloudflare/Railway karar matrisi, env & secrets |
| **Test/QA** | Stack'e göre test stratejisi, erişilebilirlik + Core Web Vitals kontrol listesi |
| **Güvenlik/Siber Güvenlik** | 124 kontrol: OWASP Top 10, STRIDE tehdit modelleme, stack'e göre güvenli kodlama, API/altyapı güvenliği, olay müdahalesi — artı stdlib statik secret/desen tarayıcısı |
| **E-ticaret & Ödemeler** | Stripe + Shopify entegrasyon desenleri, imza doğrulamalı webhook iskeleti |
| **UI/UX & Özgün Frontend** | "Jenerik AI tasarımı" karşıtı el kitabı — şablon görünümünden kaçınmak için yerleşim/tipografi/hareket teknikleri |
| **SEO** | 92 kontrol: teknik, on-page, içerik/E-E-A-T, schema seçimi, GEO/AI atıf edilebilirliği |
| **Reklam** | 64 kontrol: Google/Meta/LinkedIn/TikTok/Microsoft + platformlar arası izleme/atıf |
| **AI Entegrasyonu** | Claude API: model seçimi & yönlendirme, streaming endpoint'ler, tool use, RAG, prompt cache/maliyet kontrolü, eval disiplini, 16 LLM güvenlik kontrolü (OWASP LLM Top 10) |
| **Analitik** | GA4/PostHog/Plausible seçimi, event taksonomisi & kod-olarak-track-planı, funnel/retention, consent uyumlu ölçümleme |
| **E-posta** | Resend/Postmark/SES seçimi, kuyruklu idempotent gönderim, 14 deliverability kontrolü (SPF/DKIM/DMARC, toplu gönderici kuralları, warmup) |
| **i18n / Yerelleştirme** | next-intl/react-i18next seçimi, URL stratejisi, hreflang, RTL, ICU çoğullama, 12 l10n kontrolü |

~789 veri satırı, 34 referans dokümanı, 14 script. **Sıfır paketlenmiş bağımlılık** — venv yok, `requirements.txt` yok.

## Kurulum

Bu depoyu Claude Code skills klasörüne klonlayın:

```bash
git clone https://github.com/0x61A/fullstack-pro-max.git ~/.claude/skills/fullstack-pro-max
```

Sonra yeni bir Claude Code oturumu başlatın — skill, `SKILL.md` frontmatter'ından otomatik algılanır. `/fullstack-pro-max <istek>` ile çağırın ya da ilgili görevlerde (stack planlama, API kurma, yayın öncesi güvenlik/SEO denetimi vb.) kendiliğinden devreye girmesine izin verin.

## Gereksinimler

- **Claude Code** (CLI, masaüstü, web veya IDE eklentisi).
- Yardımcı script'ler için **Python 3** — yalnızca standart kütüphane, kurulacak paket yok.
- **İsteğe bağlı MCP sunucuları**: bazı modüller bağlıysa MCP araçlarını (Supabase, Vercel, Netlify, Cloudflare, Shopify) canlı işlemler için kullanabilir. Bunlar isteğe bağlıdır — skill'in rehberliği onlarsız da çalışır.

## Script'ler

Her script `--help` destekler:

```bash
python3 scripts/common/search.py data/backend/stacks.csv --query "edge"   # herhangi bir CSV'yi sorgula
python3 scripts/common/score.py data/security --results results.json       # önem-ağırlıklı güvenlik skoru
python3 scripts/security/audit.py ./projem                                 # secret/tehlikeli desen taraması
python3 scripts/backend/generate.py posts --stack nextjs-api               # CRUD endpoint iskeleti
python3 scripts/common/validate.py                                          # tüm veri CSV'lerini doğrula (CI ile aynı)
python3 scripts/ai/generate.py --stack nextjs-api --dry-run                 # streaming Claude chat endpoint'i
```

## Notlar

- **Özgün içerik, kendi kendine yeten.** Başka hiçbir skill'e çalışma zamanı bağımlılığı yok.
- **CI kendi ilacını içiyor.** Her push'ta tüm veri satırları ortak şemaya göre doğrulanır, tüm script'ler smoke-test edilir, dosya referansları kontrol edilir ve depo, skill'in kendi `scripts/security/audit.py` script'iyle taranır.
- **Rehberlik, garanti değil.** Güvenlik, ödeme, SEO ve reklam içeriği güçlü bir başlangıç noktasıdır — üretimde kullanmadan önce kendi projenizin bağlamına, uyumluluk gereksinimlerine ve güncel platform dokümanlarına göre doğrulayın.

## Lisans

[MIT](LICENSE) © 2026 Ahmet Şerif Kart
