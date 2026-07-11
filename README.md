# DayRoute AI

> World-aware city route generator powered by AI — turns a destination and a time budget into a realistic, walkable day itinerary.
> Süni intellekt əsaslı şəhər marşrut generatoru — şəhər adı və vaxt büdcəsini real, gəzilə bilən gündəlik marşruta çevirir.

🔗 **Live demo:** https://toghrulahmad.github.io/dayroute-ai/frontend/index.html
🔗 **Backend API:** https://164-90-222-131.nip.io
🔗 **Repository:** https://github.com/toghrulahmad/dayroute-ai

---

## 🇬🇧 English

### Overview
DayRoute AI generates a personalized, time-aware day itinerary for any city. The user enters a destination and a total time budget (in minutes); the system uses an LLM (Claude via LangChain) combined with real-world geographic and routing data to produce a realistic sequence of stops that fits within the given time.

### Features
- 🌍 Destination-based itinerary generation for any city worldwide
- ⏱️ Time-budget aware planning (won't overbook the day)
- 🗺️ Real geocoding via **Nominatim** (OpenStreetMap)
- 🚗 Real travel-time/distance calculation via **OSRM**
- 🧠 Reasoning and itinerary composition via **LangChain + Claude**
- 💾 Persistent storage with **PostgreSQL**
- ✈️ Boarding-pass style UI — displays the itinerary like a travel ticket
- 🔒 Served entirely over **HTTPS** (Nginx + Let's Encrypt/Certbot)
- 🔔 **Automated Telegram notifications** via an **n8n** workflow whenever a new route is generated

### Tech Stack
| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| AI / Orchestration | LangChain, Anthropic Claude |
| Geocoding | Nominatim (OpenStreetMap) |
| Routing | OSRM |
| Automation / Notifications | n8n (Webhook → Telegram) |
| Frontend | HTML / CSS / JavaScript (boarding-pass design) |
| Hosting (backend) | DigitalOcean Droplet + Nginx reverse proxy |
| Hosting (frontend) | GitHub Pages |
| SSL | Let's Encrypt via Certbot (nip.io domain) |

### Architecture
```
[ Frontend (GitHub Pages) ]
          │  HTTPS
          ▼
[ Nginx reverse proxy (DigitalOcean) ]
          │
          ▼
[ FastAPI backend ]
   │        │            │            │
   ▼        ▼            ▼            ▼
[Nominatim] [OSRM]  [LangChain → Claude]  [n8n Webhook]
   │                                          │
   ▼                                          ▼
[PostgreSQL]                            [Telegram Bot]
```

Whenever a route is successfully generated, the backend fires an async, non-blocking HTTP call to an n8n Webhook, which then sends a formatted notification to a Telegram bot. If the notification call fails for any reason, it's caught and logged — it never breaks the main route-generation response.

### Running locally
```bash
git clone https://github.com/toghrulahmad/dayroute-ai.git
cd dayroute-ai
docker compose up --build
```
The API will be available at `http://localhost:8000`. Open `frontend/index.html` in a browser to use the UI (update `API_BASE` in `index.html` to point at your local backend if needed).

### Environment variables
Create a `.env` file in the project root (see `.env.example` if present) with values such as:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dayroute
ANTHROPIC_API_KEY=your_key_here
N8N_WEBHOOK_URL=https://your-n8n-instance/webhook/dayroute-notify
```

---

## 🇦🇿 Azərbaycanca

### Ümumi baxış
DayRoute AI istənilən şəhər üçün fərdiləşdirilmiş, vaxta uyğun gündəlik marşrut yaradır. İstifadəçi bir şəhər adı və ümumi vaxt büdcəsini (dəqiqə ilə) daxil edir; sistem LLM (LangChain vasitəsilə Claude) ilə real coğrafi və marşrutlaşdırma məlumatlarını birləşdirərək verilən vaxta uyğun realist dayanacaqlar ardıcıllığı yaradır.

### Xüsusiyyətlər
- 🌍 Dünyanın istənilən şəhəri üçün marşrut yaradılması
- ⏱️ Vaxt büdcəsinə uyğun planlaşdırma (günü həddindən artıq doldurmur)
- 🗺️ **Nominatim** (OpenStreetMap) vasitəsilə real geokodlaşdırma
- 🚗 **OSRM** vasitəsilə real səyahət vaxtı/məsafə hesablanması
- 🧠 **LangChain + Claude** vasitəsilə fikirləşmə və marşrut tərtibi
- 💾 **PostgreSQL** ilə davamlı saxlama
- ✈️ Boarding-pass (təyyarə bileti) dizaynlı interfeys
- 🔒 Tamamilə **HTTPS** üzərindən işləyir (Nginx + Let's Encrypt/Certbot)
- 🔔 **n8n** workflow vasitəsilə hər yeni marşrut yaradıldıqda **avtomatik Telegram bildirişi**

### Texnologiya yığını
| Qat | Texnologiya |
|---|---|
| Backend | FastAPI (Python) |
| Verilənlər bazası | PostgreSQL |
| AI / Orkestrasiya | LangChain, Anthropic Claude |
| Geokodlaşdırma | Nominatim (OpenStreetMap) |
| Marşrutlaşdırma | OSRM |
| Avtomatlaşdırma / Bildirişlər | n8n (Webhook → Telegram) |
| Frontend | HTML / CSS / JavaScript (boarding-pass dizaynı) |
| Hosting (backend) | DigitalOcean Droplet + Nginx reverse proxy |
| Hosting (frontend) | GitHub Pages |
| SSL | Let's Encrypt (Certbot, nip.io domeni) |

### Necə işləyir (bildiriş axını)
Marşrut uğurla yaradıldıqda, backend asinxron şəkildə n8n Webhook-una HTTP sorğu göndərir; n8n də formatlanmış bir bildirişi Telegram bota ötürür. Bildiriş göndərilməsi uğursuz olarsa, xəta tutulub loglanır — əsas marşrut yaratma cavabına heç bir təsir etmir.

### Yerli mühitdə işə salmaq
```bash
git clone https://github.com/toghrulahmad/dayroute-ai.git
cd dayroute-ai
docker compose up --build
```
API `http://localhost:8000` ünvanında əlçatan olacaq. İnterfeysi istifadə etmək üçün `frontend/index.html` faylını brauzerdə aç (lazım gələrsə `index.html`-dəki `API_BASE`-i öz local backend-inə uyğun dəyiş).

### Mühit dəyişənləri (Environment variables)
Layihə kökündə `.env` faylı yarat (əgər varsa `.env.example`-a bax) və bu kimi dəyərləri əlavə et:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dayroute
ANTHROPIC_API_KEY=sənin_açarın
N8N_WEBHOOK_URL=https://sənin-n8n-instansiyan/webhook/dayroute-notify
```

---

## License
MIT

## Author
**Toghrul Ahmadov** — [github.com/toghrulahmad](https://github.com/toghrulahmad)
