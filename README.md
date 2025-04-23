# IoT Monitorovanie a Riadenie – Záverečný projekt

Tento projekt je súčasťou záverečného zadania ku skúške a zameriava sa na vytvorenie IoT systému pre **monitorovanie a riadenie signálov z reálnych senzorov**, s využitím **webovej aplikácie** nasadenej v cloude.

## 🎯 Ciele projektu

- Vyvinúť **kontajnerizovanú webovú aplikáciu (backend)** v jazyku **Python** pomocou frameworku **FastAPI**
- Vytvoriť **klientskú časť** pomocou **HTML, CSS a JavaScript**
- Nasadiť aplikáciu do **Azure cloudu**
- Použiť **ESP32** ako riadiacu jednotku
- Monitorovať signály z:
  - **DHT22** – senzor teploty a vlhkosti
  - **ADXL335** – senzor vibrácií
  - **ESP32-CAM** – vizuálne sledovanie prostredia
- Riadiť **servo motor** na ovládanie vetrania (otváranie dvierok)
- Uchovávať údaje v databáze **PostgreSQL**
- Vizualizovať údaje cez grafy a ručičkové ukazovatele
- Logovať a exportovať údaje do súborov

---

## ✅ Funkcie systému

1. **Open** – inicializácia systému a spojenie s ESP32
2. **Nastavenie parametrov** monitorovania a riadenia (napr. prahové hodnoty)
3. **Start** – spustenie monitorovania alebo regulácie
4. **Zobrazenie údajov** vo forme zoznamu
5. **Zobrazenie grafov** (napr. teplota, vlhkosť, vibrácie)
6. **Zobrazenie údajov cez cíferníky** (gauge vizualizácia)
7. **Ukladanie do databázy PostgreSQL**
8. **Export údajov do súborov** (napr. CSV)
9. **Stop** – ukončenie monitorovania alebo riadenia
10. **Close** – deaktivácia systému a ukončenie spojenia
11. **Riadenie vetrania** – automatické alebo manuálne ovládanie **servo motorom** na otvorenie/zatvorenie vetracích dvierok podľa aktuálnej teploty/vlhkosti alebo podľa príkazu z klienta

---

## ⚙️ Použité technológie

### Backend:
- **Python 3.10+**
- **FastAPI** – REST API pre komunikáciu medzi frontendom a hardvérom
- **PostgreSQL** – relačná databáza pre archiváciu údajov
- **Docker** – kontajnerizácia backendu
- **Azure** – cieľová platforma na nasadenie

### Frontend:
- **HTML5, CSS3, JavaScript**
- *(tu doplním konkrétne knižnice/frameworky, napr. React/Vue, Chart.js, JustGage)*

### Hardvér:
- **ESP32** – hlavná mikrokontrolérová jednotka
- **DHT22** – senzor teploty a vlhkosti
- **ADXL335** – senzor vibrácií (analógový akcelerometer)
- **ESP32-CAM** – vizuálny monitoring
- **Servo motor** – riadenie vetrania (otváranie/zatváranie dvierok)

---

## 🧠 Architektúra systému

- ESP32 zhromažďuje údaje zo senzorov a posiela ich na backend cez REST API
- Backend spracováva údaje a ukladá ich do databázy PostgreSQL
- Frontend vizualizuje údaje v reálnom čase
- Ovládanie serva prebieha buď automaticky (na základe podmienok) alebo manuálne cez frontend

