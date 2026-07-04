# fullstack-pro-max

[![CI](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml/badge.svg)](https://github.com/0x61A/fullstack-pro-max/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/0x61A/fullstack-pro-max)](https://github.com/0x61A/fullstack-pro-max/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero dependencies](https://img.shields.io/badge/dependencies-zero-blue.svg)](#gereksinimler)

*English version: [README.md](README.md)*

**Gerçek bir web ürününü uçtan uca çıkaran tek bir [Claude Code](https://claude.com/claude-code) skill'i** — özgün (şablon görünümlü olmayan) UI/UX, backend mimarisi, veritabanı & auth, deployment, test, siber güvenlik, SEO, reklam, e-ticaret ödemeleri, AI özellikleri, analitik, e-posta ve i18n. Tek bir sabit frontend+backend ikilisine kilitlenmek yerine projeye göre uyarlanan stack seçimi yapar. İki kullanım senaryosu için: ajans/müşteri teslimatı ve kişisel SaaS projeleri.

<p align="center">
  <img src="assets/social-preview.png" alt="fullstack-pro-max" width="640">
</p>

## İçindekiler

[İçinde ne var](#i̇çinde-ne-var) · [Hızlı başlangıç](#hızlı-başlangıç) · [Kullanımda](#kullanımda-nasıl-görünüyor) · [Saha testleri](#saha-testleri) · [Gerçek örnekler](#gerçek-örnekler) · [Script'ler](#scriptler) · [Bilinen sınırlar](#bilinen-sınırlar)

## Hızlı başlangıç

```bash
git clone https://github.com/0x61A/fullstack-pro-max.git ~/.claude/skills/fullstack-pro-max
```

Yeni bir Claude Code oturumu başlatın — skill, `SKILL.md` frontmatter'ından otomatik yüklenir. Doğrudan `/fullstack-pro-max <istek>` ile çağırın, ya da görevi tarif edin ("SaaS backend'i planla", "yayın öncesi denetim yap", "bu landing page'i daha az jenerik yap") — ilgili görevlerde kendiliğinden devreye girer.

**Gereksinimler:** Claude Code (CLI/masaüstü/web/IDE) ve yardımcı script'ler için Python 3 — yalnızca standart kütüphane, `pip install` gereken hiçbir şey yok. Bazı modüller bağlıysa MCP araçlarını (Supabase, Vercel, Netlify, Cloudflare, Shopify) canlı işlemler için kullanabilir; bunlar isteğe bağlıdır, skill'in rehberliği onlarsız da çalışır ve bir connector faydalı olacaksa bunu açıkça söyler.

## İçinde ne var

On üç modül; her biri yapılandırılmış veri (CSV), ihtiyaç anında yüklenen referans dokümanları ve yalnızca stdlib kullanan Python script'leriyle destekleniyor. ~1038 veri satırı, 37 referans dokümanı, 16 script — **sıfır paketlenmiş bağımlılık**, venv yok, `requirements.txt` yok.

**Ürünü çıkar**

| Modül | Kapsam |
|---|---|
| **Backend & API** | Uyarlanabilir stack seçimi (Next.js/Express/Nest.js/Fastify · FastAPI/Django · Supabase/Firebase · Cloudflare Workers), API tasarımı, hata yönetimi |
| **Veritabanı & Auth** | Şema tasarımı, RLS/multi-tenancy, auth strateji matrisi, güvenli migration |
| **UI/UX & Özgün Frontend** | "Jenerik AI tasarımı" karşıtı el kitabı — 30 stillik estetik sözlük (brutalism → gradient-mesh), marka kişilik eksenlerinden Design DNA türetme, yerleşim/tipografi/hareket teknikleri. Örnek site linklerini kod öncesi Referans Tasarım Brief'ine dönüştürür; linki yoksa her stile 2 gerçek isimli site + galeri-arama kaynağı öneren 90 satırlık bilinen-siteler kütüphanesi; sıfırdan değil hazır bir component isteniyorsa 21st.dev, shadcn/ui, Aceternity UI, Magic UI, Tremor gibi 24 satırlık component-library indeksi + copy-paste/CLI/npm entegrasyon rehberi |
| **E-ticaret & Ödemeler** | Stripe + Shopify entegrasyon desenleri, imza doğrulamalı webhook iskeleti |
| **DevOps & Deployment** | CI/CD, Vercel/Netlify/Cloudflare/Railway karar matrisi, env & secrets |
| **Test/QA** | Stack'e göre test stratejisi, erişilebilirlik + Core Web Vitals kontrol listesi |
| **Güvenlik/Siber Güvenlik** | 134 kontrol: OWASP Top 10, STRIDE tehdit modelleme, stack'e göre güvenli kodlama, API/altyapı/tedarik zinciri güvenliği, olay müdahalesi — artı stdlib statik secret/desen tarayıcısı |

**Ürünü büyüt**

| Modül | Kapsam |
|---|---|
| **SEO** | 112 kontrol: teknik, on-page, içerik/E-E-A-T, schema seçimi, GEO/AI atıf edilebilirliği, yerel SEO (GBP/NAP/yorumlar) |
| **Reklam** | 74 kontrol: Google/Meta/LinkedIn/TikTok/Microsoft + platformlar arası izleme/atıf + kreatif/bütçe disiplini |
| **AI Entegrasyonu** | Claude API: model seçimi & yönlendirme, streaming endpoint'ler, tool use, RAG, prompt cache/maliyet kontrolü, eval disiplini, 16 LLM güvenlik kontrolü (OWASP LLM Top 10) |
| **Analitik** | GA4/PostHog/Plausible seçimi, event taksonomisi & kod-olarak-track-planı, funnel/retention, consent uyumlu ölçümleme |
| **E-posta** | Resend/Postmark/SES seçimi, kuyruklu idempotent gönderim, 14 deliverability kontrolü (SPF/DKIM/DMARC, toplu gönderici kuralları, warmup) |
| **i18n / Yerelleştirme** | next-intl/react-i18next seçimi, URL stratejisi, hreflang, RTL, ICU çoğullama, 12 l10n kontrolü |

## Kullanımda nasıl görünüyor

Her modülün verisi aynı şekilde sorgulanır — 13 modülün tamamında ortak CSV şeması:

```
$ python3 scripts/common/search.py data/ui-ux/distinctiveness-patterns.csv --query "layout"
id     category                option
-----  ----------------------  ----------------------------------------
UX052  Layout Distinctiveness  Break the vertical-stack-of-centered-sec
UX054  Grid Systems            Use an asymmetric or broken grid deliber
UX059  Typography as Layout    Let display type be a primary layout/com
...
6 match(es).
```

Generator'lar gerçek, isabetli kod üretir — örn. Next.js için security header'lar:

```
$ python3 scripts/security/generate.py --stack nextjs --dry-run
const securityHeaders = [
  { key: "Content-Security-Policy",
    // TODO: loosen deliberately per resource you actually need -- start strict.
    value: "default-src 'self'; script-src 'self'; ... frame-ancestors 'none'" },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  ...
];
```

## Saha testleri

İki gerçek prompt, gerçek script'lerle uçtan uca çalıştırıldı (dry-run değil, transkript değil) — çıktı [`examples/`](examples) altında commit'li:

| Senaryo | Prompt | Bulunan & düzeltilen |
|---|---|---|
| [`salon-site/`](examples/salon-site) | "Sıfırdan işletmeme bir site yap" (yerel kuaför, tercih belirtilmemiş) | `data/backend/stacks.csv`'de "backend gerekmiyor" satırı yoktu — bir broşür-site brief'i için en yaygın gerçek cevap bu. `BE088` + Stack Decision Tree'ye yeni soru-0 eklendi. |
| [`dark-technical-dashboard/`](examples/dark-technical-dashboard) | "Karanlık, teknik dashboard — sıfırdan değil hazır component kullan" | Bir palet satırının hex-çıkarma sezgiseli accent rengini sessizce düşürüyordu; `scripts/backend/generate.py` zaten çoğul verilen kaynak adlarını çift çoğulluyordu (`projects` → `projectses`). İkisi de düzeltildi. İki component-library kaynağı canlı çekilip `component-libraries.csv` iddialarıyla karşılaştırıldı — ikisi de hâlâ doğru, bir detay güncellendi. |

Her klasörün kendi `.md` yazısı çalıştırılan komutları ve hangi referans dosyası/CSV satırına denk geldiğini gösteriyor — routing mantığı sadece okunarak değil, skill'in güncel sürümüne karşı yeniden çalıştırılarak da kontrol edilebilir.

## Gerçek örnekler

Yukarıdaki `examples/` iskeletleri kasıtlı olarak yarım — TODO işaretli yapı, teslim edilebilir bir sayfa değil. Aşağıdakiler bu başlangıç noktasının gerçek, bitmiş bir siteye taşındığında nasıl göründüğünün ekran görüntüleri.

**AURA — Güzellik & Bakım Evi** (kuaför/güzellik). [`salon-site` saha testiyle](examples/salon-site) aynı karar yolu: `BE088` backend-gerekmiyor kararı, `UX269` kuaför sektör yönü, playful-rounded stil.

![AURA kuaför sitesi](assets/screenshot-salon-build.png)

**Meridyen Kahve** (kafe/restoran). `UX068` sektör yönüne göre: sıcak toprak tonu palet, editorial yemek fotoğrafçılığı, asimetrik hero.

![Meridyen Kahve kafe sitesi](assets/screenshot-cafe-build.png)

**Erdem & Kaya Hukuk Bürosu** (hukuk). `UX070` sektör yönü (deep ink, serif otorite) + `UX127` Swiss/International stili (strict grid, tek grotesk, sıfır süsleme) — açık mod, sadece hairline yapı, hiçbir yerde gölge/radius yok. Kuaförün yumuşak/rounded sıcaklığından skill'in sözlüğünde gidebileceği en uzak nokta.

![Erdem & Kaya hukuk sitesi](assets/screenshot-law-build.png)

**Fluxlane** (SaaS/dev-tool, kurgusal). `UX071` ürün-öncelikli sektör yönü + `UX138` bento-grid stili — bilinçli olarak `UX141` dark-technical *değil* (yukarıdaki dashboard saha testinde zaten kullanıldı, ve şu an SaaS'ta en doymuş görünüm) — aynı sektörün gerçekten farklı bir sonuç üretebildiğini kanıtlamak için.

![Fluxlane SaaS sitesi](assets/screenshot-saas-build.png)

Dört sektör, dört palet, dört tip eşleşmesi — ama gözden geçirince dördü de aynı sayfa mimarisini paylaşıyor (kicker → başlık → alt metin → 2 buton → kart/özellik grid'i → footer). Farklı kaplama, aynı iskelet: skill'in kendi verisinin adlandırdığı `UX051` anti-pattern'inin ("default AI/template görünüşü") ta kendisi, ve kendi `UX050` kontrolünü ("5 rakibe logo değişse geçer mi?") birbirine karşı bile geçemiyorlar. İncelemede yakalandı, yanlış iddia olarak kalması yerine düzeltildi.

### Paylaşılan iskeleti kırmak — birinci deneme ve nerede yanlış gitti

İlk düzeltme fazla ileri gitti: üç site (bir mimarlık stüdyosu, bir butik otel, bir fitness stüdyosu) **yapısal** yeniliği kovaladı — split-screen'ler, full-bleed bölümler, marquee-güdümlü collage — ama bunun için zanaati feda etti. Mimarlık ve otel yapımları fotoğrafı düz CSS gradient'lerle sahteledi; bu, sanat yönü tamamen gerçek görsele dayanan sektörler (`UX073`, `UX274`) için ölümcül — kendi `avoid_when` alanları bunu açıkça söylüyor. Fitness yapımı radial-gradient "blob" arka plana yaslandı, ki bu `UX051`'in kendi anti-pattern tanımının adı geçen bir bileşeni. Kullanıcı incelemesinde yakalandı, kötü örnek olarak tutulmak yerine üçü de kaldırıldı.

**NOKTA Stüdyo** (ses/hareket stüdyosu, `UX132` collage/zine) bu geçişten sağ çıktı — hero yok, kart yok: kayan bir marquee ana görsel eleman, döndürülmüş çakışan kartlar bilinçli grid kırılımı (`UX055`, `UX054`), yapısal bir jest olarak değil gerçek zanaatla uygulandı.

![NOKTA collage stüdyo sitesi](assets/screenshot-collage-build.png)

### İkinci deneme — sadece renk değil, gerçekten farklı *temalar*, düzgün yapılmış

"Farklı" görsel malzemenin kendisi olmalı, aynısının recolored versiyonu değil — ve hâlâ gerçekten iyi görünmesi lazım, ki mimarlık/otel/fitness'taki ilk deneme bunu başaramadı.

**Liman Emlak** (emlak, `UX073`). Hero yok — mülk envanterinin kendisi sayfayı açıyor, gerçek fotoğraflardan masonry grid (`UX054`), grid ritmini bir kez kıran editorial not. Yukarıdaki mimarlık-stüdyosu başarısızlığı "fotoğraf" için sahte gradient dikdörtgen kullanmıştı; bu, gerçek görsel kullanıyor — çünkü `UX073` gerçek görsel olmadan çalışmıyor.

![Liman Emlak emlak sitesi](assets/screenshot-realestate-build.png)

Bunun için iki deneme daha — claymorphism bir çocuk uygulaması ve glassmorphism bir fintech cüzdanı — kullanıcı incelemesinde skill'in kendi kalite çıtasını geçemedi ve kötü örnek olarak tutulmak yerine kaldırıldı. Temalı bir *malzeme* (cam, kil, ya da başka) hâlâ gerçek zanaatla uygulanmalı, sadece yenilik olsun diye seçilmemeli; bunların çalışan versiyonları, varsa, buraya sonra eklenecek.

## Script'ler

Her script `--help` destekler.

```bash
# sorgula & doğrula
python3 scripts/common/search.py data/backend/stacks.csv --query "edge"                    # herhangi bir CSV'yi sorgula
python3 scripts/common/validate.py                                                          # tüm veri CSV'lerini doğrula (CI ile aynı)
python3 scripts/common/score.py data/security --results results.json                        # önem-ağırlıklı güvenlik skoru

# scaffolder'lar (modül başına bir tane)
python3 scripts/backend/generate.py posts --stack nextjs-api                                # CRUD endpoint
python3 scripts/security/audit.py ./projem                                                  # secret/tehlikeli desen taraması
python3 scripts/ai/generate.py --stack nextjs-api --dry-run                                  # streaming Claude chat endpoint
python3 scripts/ui-ux/scan.py https://a.com https://b.com --brief                            # örnek sitelerden Referans Tasarım Brief taslağı
python3 scripts/ui-ux/generate.py --palette UX088 --components hero,nav                      # design token + bileşen iskeletleri

# UI/UX arama tabloları
python3 scripts/common/search.py data/ui-ux/known-sites-library.csv --tag style:UX141        # "dark-technical" için gerçek siteler
python3 scripts/common/search.py data/ui-ux/component-libraries.csv --category "Selection Guide"  # hazır component kaynakları
```

## Bilinen sınırlar

- **İki kez sahada test edildi, henüz ölçekte değil.** [İki gerçek prompt](#saha-testleri) gerçek script'lerle uçtan uca çalıştırıldı, ikisi de gerçek bug çıkardı ve düzeltildi — ama bu, çok geniş bir olasılık uzayından iki senaryo, ve ikisini de skill'in yazarı çalıştırdı, bağımsız bir kullanıcı değil. Routing mantığını "giderek daha çok kontrol edilmiş" olarak değerlendirin, "tamamen kanıtlanmış" değil — daha fazla/dağınık gerçek promptla sınanana kadar.
- **İki UI/UX arama CSV'si, model bilgisinden yazıldı, canlı çekilmedi.** `known-sites-library.csv` (görsel ilham) ve `component-libraries.csv` (gerçek kod kaynağı) token tasarrufu için mevcut bilgiden yazıldı, yazıldığı anda canlı web'e karşı doğrulanmadı. İkisi de kendi `last_verified` notunda bunu belirtiyor — bir siteyi/component'i güncel gerçek olarak aktarmadan önce her zaman doğrulayın.
- **Rehberlik, garanti değil.** Güvenlik, ödeme, SEO ve reklam içeriği güçlü bir başlangıç noktasıdır — üretimde kullanmadan önce kendi projenizin bağlamına, uyumluluk gereksinimlerine ve güncel platform dokümanlarına göre doğrulayın.

## Notlar

- **Özgün içerik, kendi kendine yeten.** Başka hiçbir skill'e çalışma zamanı bağımlılığı yok.
- **CI kendi ilacını içiyor.** Her push'ta tüm veri satırları ortak şemaya göre doğrulanır, tüm script'ler smoke-test edilir, dosya referansları kontrol edilir ve depo, skill'in kendi `scripts/security/audit.py` script'iyle taranır.

Bu skill'in arkasındaki mimari kararlar için [`docs/how-it-was-built.md`](docs/how-it-was-built.md), tüm sürüm geçmişi için [`CHANGELOG.md`](CHANGELOG.md).

## Lisans

[MIT](LICENSE) © 2026 Ahmet Şerif Kart
