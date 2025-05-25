Claro, aquí tienes el contenido traducido completamente al **turco**:

---

### 📄 `README.md`

```markdown
# 🎓 Akademik Yönetim Sistemi - Flask + SQLite

Bu proje, **Flask**, **SQLAlchemy** ve **SQLite** kullanılarak geliştirilmiş bir web tabanlı akademik yönetim uygulamasıdır. Yöneticilerin, öğretmenlerin ve öğrencilerin dersleri, notları, günlükleri ve daha fazlasını yönetmesini sağlar.

---

## 🧩 Temel Özellikler

### 🔐 Kullanıcı Kimlik Doğrulama
- Rollerle kayıt ve giriş: Yönetici, Öğretmen, Öğrenci
- Role göre farklı izinler

### 👨‍🏫 Öğretmenler
- Derslere kayıt ve atama
- Öğrencileri görüntüleme
- Not ve akademik günlük ekleme

### 👨‍🎓 Öğrenciler
- Kayıt olurken ders seçimi
- Notlarını ve derslerini görüntüleme

### 📚 Dersler
- Ders ekleme, listeleme ve silme
- Öğretmenlere ve öğrencilere ders atama

### 📝 Notlar
- Öğretmenler öğrencilere not ekleyebilir

### 📖 Günlükler
- Öğretmenler öğrenciler için günlük gözlemler yazabilir

### 📤 Dışa Aktarımlar
- Öğrencileri ve öğretmenleri indirilebilir JSON dosyalarına aktarma

---

## 🧱 Kullanılan Teknolojiler

- **Python 3.x**
- **Flask**
- **Flask-Login**
- **Flask-SQLAlchemy**
- **SQLite**
- **Bootstrap 5**
- HTML5, CSS3, Jinja2

---

## 📂 Proje Yapısı

```

/project-root
│
├── app.py                  # Flask ana dosyası
├── models.py               # SQLAlchemy modelleri
├── /templates              # HTML dosyaları (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── lessons.html
│   ├── notes.html
│   ├── diaries.html
│   ├── login.html
│   └── register.html
├── /static                 # Statik dosyalar (CSS, görseller, JS)
├── /instance
│   └── app.db              # SQLite veritabanı
└── README.md               # Bu dosya

````

---

## ⚙️ Kurulum ve Kullanım

### 1. Depoyu klonlayın
```bash
git clone https://github.com/kullaniciadi/akademik-yonetim-flask.git
cd akademik-yonetim-flask
````

### 2. Sanal ortam oluşturun (isteğe bağlı ama önerilir)

```bash
python -m venv venv
source venv/bin/activate   # Windows için: venv\Scripts\activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

> Eğer `requirements.txt` dosyanız yoksa şunu kullanarak oluşturabilirsiniz:
> `pip freeze > requirements.txt`

### 4. Uygulamayı çalıştırın

```bash
python app.py
```

Tarayıcınızdan `http://127.0.0.1:5000` adresini ziyaret edin.

---

## 🔒 Sistem Rolleri

| Rol      | Temel İzinler                               |
| -------- | ------------------------------------------- |
| Yönetici | Tam kontrol: dersler, kullanıcılar, veriler |
| Öğretmen | Not ekleme, günlük yazma, öğrencileri görme |
| Öğrenci  | Derslerini ve notlarını görüntüleme         |

---

## 🛠 Özel Özellikler

* 🌐 Bootstrap ile duyarlı arayüz
* 🔄 SQLAlchemy ilişkileri: One-to-One, Many-to-Many
* 📤 JSON formatında veri dışa aktarma (`/export/students`, `/export/teachers`)
* ✨ Çoklu kullanıcı desteği

---

## 📬 Katkı

Katkıda bulunmak ister misiniz? Hoş geldiniz! Bir issue açın veya pull request gönderin.

---

## 📄 Lisans

Bu proje MIT lisansı altındadır. Uygun atıf verdiğiniz sürece istediğinizi yapabilirsiniz.

---

## 👨‍💻 Geliştirici

Geliştiren: \[Adınız veya GitHub kullanıcı adınız]

```

---

Dilersen `requirements.txt` dosyasını da Türkçe açıklamalarla hazırlayabilirim. İster misin?
```

