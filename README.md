# 🌱 Arduino ve Yapay Zeka Tabanlı Akıllı Sulama Sistemi

Bu proje, **Arduino tabanlı sensör verileri**, **gerçek zamanlı hava durumu bilgileri** ve  
**Makine Öğrenmesi (Machine Learning)** kullanarak sulama gerekip gerekmediğine karar veren  
**akıllı bir sulama karar destek sistemi**dir.

---

## 🎯 Projenin Amacı

Bu projenin temel amacı:

- Gereksiz sulamayı önlemek
- Su kaynaklarını daha verimli kullanmak
- Sabit eşikler yerine **veriye dayalı kararlar almak**
- Klasik kural tabanlı sistemleri **yapay zeka ile güçlendirmek**

---

## ⚙️ Sistem Mimarisi

Proje **3 ana katmandan** oluşur:

### 1️⃣ Arduino Katmanı
- Toprak nem sensörü ve ışık sensöründen veri okur
- Sensör verilerini seri port üzerinden bilgisayara gönderir
- Python tarafından gelen karara göre LED’leri kontrol eder

### 2️⃣ Yapay Zeka & Karar Katmanı (Python)
- Arduino’dan gelen anlık verileri işler
- Hava durumu API’sinden dış ortam verilerini alır
- Makine öğrenmesi modeli ile sulama kararı verir
- Kararı tekrar Arduino’ya gönderir

### 3️⃣ Makine Öğrenmesi Katmanı
- Geçmiş sensör ve hava durumu verileriyle model eğitilir
- Model, sulama gerekliliğini **0 / 1** olarak tahmin eder

---

## 📂 Proje Dosya Yapısı

```text
├── kayit.py
├── ml_model.py
├── weather_merge.py
├── irrigation_model.py
├── live_irrigation.py
