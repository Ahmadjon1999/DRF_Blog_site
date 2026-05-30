# Blog API

Django Rest Framework yordamida yozilgan Token autentifikatsiyali Blog API tizimi.

## O'rnatish bosqichlari

### 1. Reponi clone qiling
git clone <github_link>
cd rest_frame

### 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate

### 3. Kutubxonalarni o'rnating
pip install -r requirements.txt

### 4. .env fayl yarating
Quyidagi .env namunasidan foydalaning

### 5. Migratsiya
python manage.py migrate

### 6. Serverni ishga tushiring
python manage.py runserver

## .env namunasi
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

## API Endpointlar

### Auth
| URL | Method | Tavsif | Token kerakmi |
|-----|--------|--------|---------------|
| /signup/ | GET | Ro'yxatdan o'tish sahifasi | Yo'q |
| /signup/ | POST | Ro'yxatdan o'tish | Yo'q |
| /signin/ | GET | Login sahifasi | Yo'q |
| /signin/ | POST | Login | Yo'q |
| /signOut/ | POST | Logout | Ha |
| /profile/ | GET | Profil ma'lumotlari | Ha |
| /profile_update/ | GET | Yangilash sahifasi | Ha |
| /profile_update/ | PATCH | Profilni yangilash | Ha |

### Post
| URL | Method | Tavsif | Token kerakmi |
|-----|--------|--------|---------------|
| /post_list/ | GET | Barcha postlar | Yo'q |
| /post_list/ | POST | Post yaratish | Ha |
| /post_detail/<pk>/ | GET | Post detail | Yo'q |
| /post_detail/<pk>/ | PATCH | Postni yangilash | Ha (owner) |
| /post_detail/<pk>/ | DELETE | Postni o'chirish | Ha (owner) |
| /post_search/ | GET | Qidirish | Yo'q |

### Comment
| URL | Method | Tavsif | Token kerakmi |
|-----|--------|--------|---------------|
| /comments/ | GET | Barcha izohlar | Yo'q |
| /comments/<pk>/ | POST | Izoh yaratish | Ha |
| /comments/<pk>/ | GET | Izoh detail | Yo'q |
| /comments/<pk>/ | PATCH | Izohni yangilash | Ha (owner) |
| /comments/<pk>/ | DELETE | Izohni o'chirish | Ha (owner) |

### Like
| URL | Method | Tavsif | Token kerakmi |
|-----|--------|--------|---------------|
| /like/<pk>/ | POST | Like bosish/olib tashlash | Ha |

## Qidiruv
| Parametr | Misol | Tavsif |
|----------|-------|--------|
| search | /post_search/?search=fantasy | Title, content, category bo'yicha |
| category | /post_search/?category=fiction | Category nomi bo'yicha |
| ordering | /post_search/?ordering=create_at | Sana bo'yicha tartiblash |