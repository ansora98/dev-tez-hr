"""Генератор вымышленного списка сотрудников (тестовые данные).
Все ФИО, паспорта и ПИНФЛ выдуманы и не принадлежат реальным людям."""
import csv, random
from datetime import date, timedelta

random.seed(2026)
TODAY = date(2026, 11, 3)
N, N_FIRED = 80, 10

M_NAMES = ["Akmal","Bekzod","Jasur","Sardor","Otabek","Shoxrux","Doniyor","Javohir","Sherzod","Ulug'bek",
           "Aziz","Farrux","Rustam","Islom","Temur","Bobur","Anvar","Dilshod","Elyor","Nodir","Sanjar","Mirjalol"]
F_NAMES = ["Dilnoza","Gulnora","Madina","Nilufar","Shahnoza","Zarina","Malika","Kamola","Sevara","Feruza",
           "Nodira","Mohira","Dildora","Laylo","Munisa","Sabina","Gulchehra","Yulduz","Durdona","Zilola"]
SURNAMES = ["Karimov","Rahimov","Toshmatov","Yusupov","Abdullayev","Ismoilov","Nazarov","Qodirov","Saidov",
            "Ergashev","Xolmatov","Mirzayev","Sobirov","Jo'rayev","Usmonov","Aliyev","Hasanov","Normatov",
            "Rasulov","Sultonov","Tursunov","Valiyev","Zokirov","Begmatov","Fayzullayev","Haydarov"]
FATHERS = ["Akmal","Baxtiyor","Shavkat","Rustam","Alisher","Farhod","Ilhom","Murod","Botir","Erkin",
           "Abdulla","Odil","Komil","Zafar","Hamid","Ravshan","Sobir","Tolib","Ulmas","Xurshid"]

DEPTS = {
    "IT": ["Backend-разработчик","Frontend-разработчик","QA-инженер","DevOps-инженер","Тимлид","Системный аналитик"],
    "Финансы": ["Бухгалтер","Финансовый аналитик","Главный бухгалтер","Казначей"],
    "HR": ["HR-менеджер","Рекрутер","Специалист по кадрам","HR бизнес-партнёр"],
    "Маркетинг": ["Маркетолог","SMM-специалист","Дизайнер","Руководитель маркетинга"],
    "Продажи": ["Менеджер по продажам","Старший менеджер по продажам","Руководитель отдела продаж","Аккаунт-менеджер"],
    "Клиентская поддержка": ["Оператор поддержки","Старший оператор","Супервайзер","Руководитель поддержки"],
}
SALARY = {"IT": (12, 35), "Финансы": (8, 22), "HR": (7, 18), "Маркетинг": (7, 20),
          "Продажи": (6, 18), "Клиентская поддержка": (5, 12)}  # млн сум
REASONS = [
    "По собственному желанию (ст. 99 ТК РУз)",
    "По соглашению сторон (ст. 98 ТК РУз)",
    "Переезд в другой город",
    "Переход в другую компанию",
    "Истечение срока трудового договора",
    "Непрохождение испытательного срока",
    "Сокращение штата",
    "Неоднократное нарушение трудовой дисциплины",
    "Поступление на учёбу",
    "По собственному желанию — уход за ребёнком",
]
DISTRICTS = ["261","262","263","264","265","266","267","268","271","272","273","274","275","276","281","282"]

def rnd_date(a, b):
    return a + timedelta(days=random.randint(0, (b - a).days))

def surname(base, female):
    return base[:-2] + "eva" if female and base.endswith("ev") else (base + "a" if female else base)

def pinfl(birth, female):
    c = (3 if birth.year < 2000 else 5) + (1 if female else 0)
    body = f"{c}{birth:%d%m%y}{random.choice(DISTRICTS)}{random.randint(1, 999):03d}"
    chk = sum(int(d) * w for d, w in zip(body, [7, 3, 1] * 5)) % 10
    return body + str(chk)

used_pass, used_pinfl, used_mail = set(), set(), set()
rows = []
for _ in range(N):
    female = random.random() < 0.45
    first = random.choice(F_NAMES if female else M_NAMES)
    last = surname(random.choice(SURNAMES), female)
    patr = f"{random.choice(FATHERS)} {'qizi' if female else "o'g'li"}"
    birth = rnd_date(date(1975, 1, 1), date(2003, 12, 31))
    hire = rnd_date(date(2019, 1, 9), date(2026, 10, 30))
    if (hire - birth).days < 18 * 365 + 5:
        hire = birth + timedelta(days=18 * 366 + 30)
    dept = random.choice(list(DEPTS))
    while True:
        p = random.choice(["AA", "AB", "AC", "AD"]) + f"{random.randint(0, 9999999):07d}"
        if p not in used_pass: used_pass.add(p); break
    while True:
        pn = pinfl(birth, female)
        if pn not in used_pinfl: used_pinfl.add(pn); break
    base = f"{first}.{last}".lower().replace("'", "")
    mail, k = base, 2
    while mail in used_mail: mail, k = f"{base}{k}", k + 1
    used_mail.add(mail)
    lo, hi = SALARY[dept]
    rows.append(dict(
        last_name=last, first_name=first, patronymic=patr,
        gender="Ж" if female else "М", birth_date=birth, department=dept,
        position=random.choice(DEPTS[dept]), hire_date=hire,
        passport=p, pinfl=pn,
        phone=f"+998 {random.choice(['90','91','93','94','95','97','99','33','88'])} "
              f"{random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}",
        email=f"{mail}@example.uz",
        salary_uzs=random.randint(lo * 10, hi * 10) * 100_000,
    ))

rows.sort(key=lambda r: r["hire_date"])
for i, r in enumerate(rows, 1):
    r["tab_number"] = f"TN-{i:05d}"
    r["status"], r["termination_date"], r["termination_reason"] = "Работает", "", ""

# уволенные — только среди принятых не позже чем за 60 дней до сегодня
candidates = [r for r in rows if (TODAY - r["hire_date"]).days > 60]
for r, reason in zip(random.sample(candidates, N_FIRED), random.sample(REASONS, N_FIRED)):
    lo = r["hire_date"] + timedelta(days=30 if "испытательного" in reason else 90)
    r["status"], r["termination_date"], r["termination_reason"] = "Уволен", rnd_date(min(lo, TODAY), TODAY), reason

COLS = ["tab_number","last_name","first_name","patronymic","gender","birth_date","department","position",
        "hire_date","status","termination_date","termination_reason","passport","pinfl","phone","email","salary_uzs"]
with open("data/test-employees.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for r in rows:
        w.writerow({c: (r[c].isoformat() if isinstance(r[c], date) else r[c]) for c in COLS})
print("ok", len(rows))
