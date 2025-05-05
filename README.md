# IoT Monitorovanie a Riadenie – Záverečný projekt

Tento projekt je súčasťou záverečného zadania ku skúške a zameriava sa na vytvorenie IoT systému pre **monitorovanie a riadenie prostredia pri 3D tlači**, s využitím **webovej aplikácie** nasadenej v cloude.

## 🎯 Ciele projektu

- Vyvinúť **kontajnerizovanú webovú aplikáciu (backend)** v jazyku **Python** pomocou frameworku **FastAPI**
- Vytvoriť **klientskú časť** pomocou **HTML, CSS a JavaScript**
- Nasadiť aplikáciu do **cloudu**
- Použiť **ESP32** ako riadiacu jednotku
- Monitorovať signály z:
  - **DHT22** – senzor teploty a vlhkosti
- Spínať **ventilátor** pre vetranie uzavretého prostredia
- Uchovávať údaje v databáze **PostgreSQL**
- Vizualizovať údaje cez grafy a ručičkové ukazovatele
- Logovať a exportovať údaje do súborov .csv

---

## ✅ Funkcie systému

1. **Start measurement** – štart merania
2. **Toggle cooling** - riadenie ventilátora
3. **Zobrazenie grafov** - teplota, vlhkosť
4. **Zobrazenie údajov cez cíferníky** (gauge vizualizácia)
5. **Ukladanie do databázy PostgreSQL**
6. **Export údajov do súborov** - export meraní do .csv súboru
7. **Stop measurement** – ukončenie merania
8. **Dashboard** – nepretržité monitorovanie, možnosť ovládania ventilátora

---

## ⚙️ Použité technológie

### Backend:
- **Python 3.8**
- **FastAPI** – REST API pre komunikáciu medzi frontendom a hardvérom
- **PostgreSQL** – relačná databáza pre archiváciu údajov
- **Docker** – kontajnerizácia backendu
- **Railway** – cieľová platforma na nasadenie do cloudu

### Frontend:
- **HTML5, CSS3, JavaScript**
- **Použité JS knižnice:**
- Bootstrap 5.3.0-alpha1 – responzivita, rozloženie, štýly
- Chart.js – zobrazenie grafov
- JustGage – pre ručičkové ukazovatele
- Raphael.js – závislosť pre JustGage.


### Hardvér:
- **ESP32** – hlavný mikrokontroler
- **DHT22** – senzor teploty a vlhkosti
- **Relé** – riadenie vetrania spínanie ventilátoru
- **Ventilátor** - akčný člen pre vetranie
---

## 🧠 Architektúra systému

- ESP32 zhromažďuje údaje zo senzorov a posiela ich na backend cez REST API
- Backend spracováva údaje a ukladá ich do databázy PostgreSQL
- Frontend vizualizuje údaje
- Ovládanie vetrania prebieha buď automaticky (na základe podmienok) alebo manuálne cez frontend

