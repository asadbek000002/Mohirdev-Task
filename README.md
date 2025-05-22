# IntakeHub loyihasi

**IntakeHub** — bu foydalanuvchilar ariza (lead) yuborishi mumkin bo‘lgan va ariza yuborilgach hodimlarga avtomatik
email xabar yuboriladigan veb ilova.

---

## 🔧 Talablar (Dependencies)

- Python 3.10+
- PostgreSQL
- Redis
- celery
- Docker & Docker Compose

---

## 📦 Loyihani ishga tushurish (Docker orqali)

### 1. Repository'ni klon qiling

```bash
git clone https://github.com/asadbek000002/Mohirdev-Task.git
cd Mohirdev-Task
```

## `.env` faylini yarating

```python
# PostgresQl
POSTGRES_DB = intakehub_db
POSTGRES_USER = intakehub_user
POSTGRES_PASSWORD = intakehub_password
POSTGRES_HOST = intakehub_host
POSTGRES_PORT = 5432

# Email
EMAIL_HOST_USER = 'asadbektuygunov9@gmail.com'
EMAIL_HOST_PASSWORD = 'hjvkbwjmykkmajhn'
DEFAULT_FROM_EMAIL = 'asadbektuygunov9@gmail.com'

```

## Docker konteynerlarini ishga tushiring

```bash
docker-compose up --build
```

Ilova http://localhost:8001 manzilida ishga tushadi.

---- 

### ✅ Testlarni ishga tushirish

Loyhadagi barcha testlarni ishga tushirish uchun quyidagi amallar bajariladi:

Docker konteynerlar ishlab turgan bolishi kerak:

intake app testlari:

```bash
sudo docker-compose exec web pytest intake/tests.py
```

attorney app testlari:

```bash
sudo docker-compose exec web pytest attorney/tests.py
```

☑️ Testlar pytest orqali yozilgan bo‘lib, har bir ilovaning tests.py faylida joylashgan. Ular forma validatsiyasi, API
endpoint ishlashi va ma'lumotlar bazasiga yozish holatlarini avtomatlashtirib tekshiradi.

---

## super user `(admin)` yarating

```bash
docker-compose exec -it mohirdev_task-web-1 /bin/bash

python manage.py createsuperuser
```

## 📩 Email qabul qiluvchilarni qo‘shish

Email xabarlar aynan Admin panel orqali kiritilgan email manzillarga yuboriladi. Buning uchun:

Admin panelga kiring: http://localhost:8001/admin/

Attorney Emails bo‘limidan yangi email qo‘shing.

Har bir advokat uchun yoki umumiy email manzil kiriting.

📌 Email manzillar faqat admin panel orqali qo‘shiladi.

## 👨‍⚖️ Advokatlarni tizimga qo‘shish

Advokatlar admin panel orqali qo‘shiladi. Har bir advokatga username, email va password beriladi.

Admin panelga kirib Users bo‘limidan yangi foydalanuvchi yarating, unga staff huquqi bering va login ma’lumotlarini
advokatga yuboring.

📌 Eslatma: Advokatlar tizimga faqat admin panel orqali qo‘shiladi. Ular uchun maxsus ro‘yxatdan o‘tish sahifasi mavjud
emas.

----

## Sayt qanday ishlaydi?

- Foydalanuvchilar (iste'dodlilar) forma orqali o‘z ma’lumotlari va rezyumesini yuboradi.

- Ariza yuborilgach, u admin panel orqali kiritilgan advokat email manzillariga avtomatik xabar sifatida yuboriladi.

- Advokatlar admin panelga login qilib, arizalarni ko‘rib chiqadi.

- Har bir ariza boshlanishida "PENDING" holatda bo‘ladi.

- Agar advokat qabul qilishga qaror qilsa, statusni "REACHED_OUT" ga o‘zgartiradi.

- Shunda iste’dodli email manziliga rezyumesi qabul qilinganligi haqida xabar boradi.

- Advokatlar:

    - Arizalarni status bo‘yicha filtrlashi,

    - Email orqali qidirishi mumkin.

### 📎 Rezyume fayliga qo‘yilgan talablar:

Maksimal hajm: 10 MB

Ruxsat etilgan formatlar: .pdf, .doc, .docx