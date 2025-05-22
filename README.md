Swagger UI (API testlash uchun):  
 👉 https://mohirdevtask.dialektalcorpus.uz

## 📚 Mavzular (Navigatsiya)


1. [Loyiha haqida](#intakehub-loyihasi)  
2. [Talablar](#-talablar-dependencies)  
3. [Ishga tushirish](#-loyihani-ishga-tushurish-docker-orqali)  
4. [Testlar](#-testlarni-ishga-tushirish)  
5. [Admin va foydalanuvchilar](#-superuser-admin-yaratish)  
6. [Email funksiyasi](#-email-qabul-qiluvchilarni-qoshish)  
7. [Rezyume talablari](#-rezyume-fayliga-qoyilgan-talablar)  
8. [Ishlash prinsipi](#sayt-qanday-ishlaydi)
9. [Deploy haqida qisqacha](#-deploy-haqida-qisqacha)


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
POSTGRES_DB = intakehub_db
POSTGRES_USER = intakehub_user
POSTGRES_PASSWORD = intakehub_password
POSTGRES_HOST = intakehub_host
POSTGRES_PORT = 5432

EMAIL_HOST_USER = "asadbektuygunov9@gmail.com"
EMAIL_HOST_PASSWORD = "hjvkbwjmykkmajhn"
DEFAULT_FROM_EMAIL = "asadbektuygunov9@gmail.com"
```

## Docker konteynerlarini ishga tushiring

```bash
docker-compose up --build
```

Swagger API hujjati ochib tekshirib koring: [http://localhost:8001/swagger/](http://localhost:8001/swagger/)

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

### 👤 Superuser (admin) yaratish

```bash
docker-compose exec web bash
python manage.py createsuperuser
```

# 📩 Email qabul qiluvchilarni qo‘shish

> ⚠️ **MUHIM ESLATMA**  
> 📌 **Email xabarlar Advokatlarga aynan Admin panel orqali kiritilgan email manzillarga yuboriladi.**
>
> Admin panelga kiring: [http://localhost:8001/admin/](http://localhost:8001/admin/)
>
> `Attorney Emails` bo‘limidan yangi email qo‘shing.
>
> Har bir advokat uchun yoki umumiy email manzil kiriting.
>
> 📌 **Email manzillar faqat admin panel orqali qo‘shiladi.**

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

---

## 🚀 Deploy haqida qisqacha

Loyiha quyidagi texnologiyalar yordamida muvaffaqiyatli deploy qilindi:

    🐳 Docker va Docker Compose orqali konteynerlashgan holda ishga tushirildi

    🌐 Nginx yordamida domen orqali backend'ga yo‘naltirish sozlandi

    🔒 HTTPS (SSL) xavfsiz aloqa uchun Let's Encrypt sertifikati bilan ta’minlandi

    🔐 CSRF va CORS sozlamalari to‘g‘ri konfiguratsiya qilindi

    🛡️ Admin panel orqali tizimni boshqarish imkoniyati yaratilgan

### 🌍 Kirish manzillari

>    Swagger UI (API testlash uchun):
>    👉 https://mohirdevtask.dialektalcorpus.uz
>
>    Admin panel:
>    👉 https://mohirdevtask.dialektalcorpus.uz/admin/
>
>    Kirish uchun:  
>    username: `admin`  
>    password: `1234`
 
### 🧪 Test qilish bo‘yicha ko‘rsatma

- Admin panel orqali yangi advokat (attorney) yarating

- Unga tegishli Gmail manzili kiriting

- Postman yoki Swagger orqali JWT login qilin

- JWT token bilan boshqa endpointlarni test qiling

Eslatma: faqat advokatlar login qiladi – foydalanuvchilar ro‘yxatdan o‘ta olmaydi.

### 🛠 Qo‘shimcha (avtomatik)

- Swagger sahifasi root (/) ga redirect bo‘ladi

- Barcha trafik 80 → 443 (HTTPS) ga avtomatik o‘tkaziladi

- Swagger orqali barcha endpointlar test qilinishi mumkin

- Backend statik fayllarni ham serve qiladi (agar kerak bo‘lsa)



## Muallif

Asadbek Tuygunov — dasturchi va loyiha muallifi.



