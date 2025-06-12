# ♻️ EcoSortify - Capstone Project (Machine Learning)

Selamat datang di file README untuk bagian *Machine Learning* dari proyek **EcoSortify**. File ini berisi penjelasan struktur proyek, fungsi folder dan file, dokumentasi model klasifikasi gambar dan chatbot edukasi sampah, serta penjelasan dataset yang digunakan.

---

## 📘 Cara Melihat Preview Markdown (di VS Code)

1. Buka **Visual Studio Code**.
2. Tekan `Ctrl+Shift+X` lalu cari **Markdown Preview Enhanced**.
3. Instal ekstensi tersebut.
4. Tekan `Ctrl+Shift+V` untuk membuka tampilan preview.

---

## 🗂️ Struktur Direktori

| Nama File/Folder                              | Tipe               | Deskripsi                                                                                   |
|-----------------------------------------------|--------------------|---------------------------------------------------------------------------------------------|
| `datasets/`                                   | Folder             | Menyimpan dataset asli (`raw/`) dan hasil preprocessing (`preprocessed/`).                 |
| └── `raw/`                                     | Folder             | Dataset mentah yang belum diproses.                                                        |
| └── `preprocessed/`                            | Folder             | Dataset yang telah dibersihkan dan diaugmentasi.                                           |
| └── `README.md`                                | Markdown           | Penjelasan isi dan label pada dataset.                                                     |
| `inferences/`                                  | Folder             | Berisi kode/script untuk inference model.                                                  |
| └── `chatbot_v1beta/`                          | Folder             | Script untuk inference chatbot QnA edukasi sampah (versi beta).                            |
| └── `garbage_classifier/`                      | Folder             | Script inference untuk klasifikasi gambar sampah.                                          |
| `models/`                                      | Folder             | Menyimpan semua format hasil ekspor model klasifikasi.                                     |
| └── `saved_model/`                             | Folder             | Model dalam format asli TensorFlow (SavedModel).                                           |
| └── `tfjs_model/`                              | Folder             | Model dalam format TensorFlow.js untuk integrasi web.                                      |
| └── `tflite/`                                  | Folder             | Model dalam format TensorFlow Lite untuk aplikasi mobile.                                  |
| `notebooks/`                                   | Folder             | Notebook Jupyter untuk pelatihan dan evaluasi model.                                       |
| └── `Capstone_Klasifikasi_Sampah.ipynb`        | Notebook           | Pipeline lengkap model klasifikasi gambar sampah.                                          |
| └── `Chatbot_Fine_Tuning.ipynb`                | Notebook           | Fine-tuning model chatbot edukasi persampahan.                                             |
| └── `Evaluation_Fine_Tuning_Chatbot.ipynb`     | Notebook           | Evaluasi performa chatbot setelah pelatihan.                                               |
| └── `QnA_Chatbot_Dataset_Preparation.ipynb`    | Notebook           | Notebook untuk preprocessing dan formatting dataset chatbot.                               |
| `.gitattributes`                               | File               | Pengaturan atribut Git.                                                                    |
| `README.md`                                    | Markdown           | Dokumentasi utama proyek Machine Learning EcoSortify ini.                                  |

---

## 📓 Penjelasan Notebook

### 1. Capstone_Klasifikasi_Sampah.ipynb
Notebook utama untuk melatih model klasifikasi gambar sampah. Mencakup:
1. **Import Library**
    
    Mengimpor pustaka TensorFlow, matplotlib, dan lainnya untuk proses data, visualisasi, dan pemodelan.

2. **Persiapan Dataset**

    * Dataset berisi gambar sampah yang diklasifikasikan ke dalam beberapa kategori (misal: organik, anorganik, B3, dll).
    * Dataset dibagi ke dalam folder `train/`, `val/`, dan `test/` sesuai standar machine learning.

3. **Augmentasi Gambar**

    Dilakukan augmentasi seperti rotasi, flipping, zoom, dan brightness adjustment untuk meningkatkan keragaman data.

4. **Pembangunan Model**

    * Menggunakan arsitektur `Sequential` dengan beberapa lapisan `Conv2D`, `MaxPooling2D`, dan `Dense`.
    * Model di-compile dengan optimizer `Adam` dan fungsi loss `categorical_crossentropy`.

5. **Konversi model ke `.tflite`, `.tfjs`, dan SavedModel**

    * Disertai callback seperti `EarlyStopping` dan `ModelCheckpoint`.
    * Visualisasi training & validation accuracy/loss dibuat untuk monitoring performa.

6. **Evaluasi akurasi dan confusion matrix**

    * Evaluasi dilakukan pada data testing.
    * Akurasi model ditampilkan dan dibandingkan dengan target performa (≥ 85%). Kenapa cuman 85%? Karena Limit Collab menghalangi kami mencoba model yang lebih kompleks dan lama.

---

### 2. Chatbot_Fine_Tuning.ipynb
Notebook untuk **fine-tuning chatbot edukasi** berbasis QnA menggunakan data yang telah dipersiapkan. Mencakup:
- Pemilihan base model Gemini 2.0
- Tokenisasi dan formatting data
- Training lanjutan (Dataset & Instrution Tuning)
- Deployment model hasil pelatihan

---

### 3. Evaluation_Fine_Tuning_Chatbot.ipynb
Notebook untuk mengevaluasi hasil fine-tuning chatbot, menggunakan:
- **Exact Match & F1 Score**
- **Manual review jawaban**
- **Prompt benchmarking** (uji model terhadap berbagai jenis pertanyaan umum hingga edge cases)

---

### 4. QnA_Chatbot_Dataset_Preparation.ipynb
Notebook untuk:
- **Menggabungkan dan membersihkan pertanyaan** seputar persampahan dari berbagai part dokumen pdf
- **Membentuk struktur `question-answer`**
- **Export dataset ke format JSON/CSV** yang siap digunakan untuk pelatihan model chatbot

---

## 🧠 Model Klasifikasi Gambar Sampah

Model klasifikasi ini dibangun menggunakan arsitektur **MobileNetV2** dengan top layer yang disesuaikan untuk 4 kelas utama:
1. **Organik**: 15530 gambar
2. **Anorganik**: 17237 gambar
3. **Elektronik**: 11326 gambar
4. **Residu & B3**: 6744 gambar

♻️ Berikut penjelasan mengenai setiap label:

### 1. 🌿 Organik

* **Definisi**: Sampah yang berasal dari bahan hayati (tumbuhan/hewan) dan dapat terurai secara alami.
* **Contoh**:

  * Sayuran dan buah-buahan busuk
  * Daun dan ranting kering
  * Sisa makanan
* **Sub-kategori**:

  * Organik Basah: cepat membusuk (mis. sisa makanan)
  * Organik Kering: lebih lambat terurai (mis. daun kering)
* **Penanganan**: Kompos, bank sampah organik, biogas, atau pakan ternak.

---

### 2. 🧴 Anorganik

* **Definisi**: Sampah dari bahan non-hayati yang sulit terurai secara alami.
* **Contoh**:

  * Plastik (PET, HDPE, PVC, LDPE)
  * Kaca, logam, kertas
  * Pakaian bekas, ban, dan mainan sintetis
* **Penanganan**: Daur ulang (3R: Reduce, Reuse, Recycle), drop ke bank sampah, atau industri pengolahan.

---

### 3. 💻 Elektronik (E-Waste)

* **Definisi**: Peralatan elektronik yang sudah tidak digunakan, termasuk limbah yang mengandung B3.
* **Contoh**:

  * HP rusak, charger, laptop bekas
  * Lampu, remote, baterai, kamera
* **Bahaya**: Mengandung logam berat (merkuri, timbal, kadmium) yang dapat mencemari tanah dan air.
* **Penanganan**: Disetor ke bank sampah elektronik, pusat daur ulang resmi, atau program take-back produsen.

---

### 4. ☢️ Residu & B3 (Bahan Berbahaya dan Beracun)

* **Definisi**: Sampah yang tidak bisa didaur ulang dan/atau mengandung zat berbahaya.
* **Contoh**:

  * Popok, pembalut, sachet makanan
  * Masker medis, baterai, lampu neon, kosmetik bekas
* **Bahaya**:

  * Bersifat racun, korosif, reaktif, atau karsinogenik.
* **Penanganan**: Harus dipisah dari sampah lain. Diserahkan ke TPS3R atau fasilitas pengelolaan limbah B3 yang resmi.

Model diekspor ke tiga format:
- `.tflite` → untuk aplikasi mobile
- `.tfjs` → untuk integrasi ke web
- `SavedModel` → untuk inference Python

Evaluasi model mencapai akurasi validasi **> 85%** dengan teknik augmentasi gambar dan fine-tuning.

---

## 🤖 Model Chatbot Edukasi Sampah

Model chatbot dirancang untuk menjawab pertanyaan edukatif tentang:
- **Klasifikasi dan jenis sampah**
- **Pengelolaan dan daur ulang**
- **Bahaya limbah B3**
- **TPS3R dan gerakan ramah lingkungan**

Base Model menggunakan Gemini 2.0 pendekatan **Fine-Tuning Instruction & Dataset**

Langkah:
1. Format dataset ke `{"question": "...", "answer": "..."}`.
2. Fine-tune model agar paham konteks pertanyaan spesifik terkait persampahan.
3. Evaluasi respons menggunakan EM, F1-Score, dan penilaian manual.
4. Deploy model ke Vertex AI untuk digunakan di backend chatbot (`inferences/chatbot_v1beta/`).

---

## 🗃️ Penjelasan Dataset Klasifikasi Sampah

Dataset berisi gambar dari 4 kategori:

| Kategori         | Contoh                                 | Penanganan Umum                                             |
|------------------|------------------------------------------|-------------------------------------------------------------|
| **Organik**       | Sisa makanan, daun, kulit buah          | Kompos, pakan ternak, biogas                                |
| **Anorganik**     | Botol plastik, kaleng, kardus bekas     | Daur ulang, upcycle, dijual ke pengepul                    |
| **Elektronik**    | HP rusak, kabel, charger, baterai       | Daur ulang e-waste, dropbox resmi, produsen take-back      |
| **Residu/B3**     | Masker bekas, popok, kemasan detergen   | Dipisahkan, dibuang ke TPS khusus limbah B3                |

Dataset berasal dari: [Kaggle - Garbage Dataset](https://www.kaggle.com/datasets/abutoyibalaziz/garbage-dataset)

Total gambar: ±50.000 (setelah augmentasi & preprocessing)

---

## 🗃️ Penjelasan Dataset Chatbot

Dataset chatbot berisi kumpulan **pertanyaan dan jawaban edukatif** seputar persampahan. Disusun berdasarkan:
- Dokumen resmi Kementerian Lingkungan Hidup
- FAQ publik dari komunitas daur ulang
- Sumber artikel edukasi lingkungan

📌 Format:  
```json
{
  "answer": "Apa itu sampah anorganik?",
  "question": "Sampah anorganik adalah sampah yang berasal dari bahan non-hayati seperti plastik, kaca, dan logam..."
}
```

## 📚 Topik mencakup:
| Topik                  | Contoh Pertanyaan                       |
| :--------------------- | :-------------------------------------- |
| **Klasifikasi Sampah** | Apa itu **sampah organik**?             |
|                        | **Sampah elektronik** termasuk sampah apa? |
| **Pengelolaan & Daur Ulang** | Bagaimana **cara mendaur ulang plastik**? |
|                        | Apa itu **kompos**?                     |
| **Bahaya Limbah B3** | Apakah **baterai** termasuk **limbah B3**? |
| **TPS3R dan Solusi Lokal** | **TPS3R** itu apa?                      |
|                        | Di mana tempat **drop-off e-waste**?    |

## 🗃️ Penjelasan Dataset Chatbot

Dataset chatbot kami siapkan secara manual dengan 4 topik utama:

| Topik                          | Contoh Pertanyaan                                               |
|-------------------------------|-----------------------------------------------------------------|
| **Klasifikasi Sampah**        | “Apa itu sampah organik?”, “Contoh sampah elektronik itu apa?” |
| **Daur Ulang & 3R**           | “Apa bedanya reuse dan recycle?”, “Cara mengolah plastik bekas”|
| **Bahaya Limbah B3**          | “Kenapa baterai tidak boleh dibuang sembarangan?”              |
| **TPS3R & Solusi Lingkungan**| “Apa itu TPS3R?”, “Bagaimana mengurangi sampah rumah tangga?”  |

📌 Format dataset chatbot menggunakan format JSON atau CSV berisi kolom `prompt` dan `response`, lalu diformat ulang untuk fine-tuning model instruksional.

---

## 🔗 Link Penting

| Nama                         | Tautan                                                                 |
|------------------------------|------------------------------------------------------------------------|
| 📁 Dokumentasi Proyek        | [Drive - Progress](https://drive.google.com/drive/folders/1kvIy-2UCWeRVt0TN2YmaN9rRo-9NyZg4?usp=sharing) |
| 📦 Dataset Gambar            | [Kaggle - Garbage Dataset](https://www.kaggle.com/datasets/abutoyibalaziz/garbage-dataset) |
| 💻 GitHub Proyek             | [GitHub - EcoSortify](https://github.com/EcoSortify)                   |
| 📱 Model `.tflite` (besar)   | [Drive - Model TFLite](https://drive.google.com/drive/folders/1BHPZYohq_p2g0ZrCzdPhmTnHAmtFOjBZ?usp=sharing) |

---

## ✅ Penutup

Dokumentasi ini disusun untuk memudahkan pemahaman terhadap sistem klasifikasi gambar dan chatbot edukasi dalam proyek **EcoSortify**.  

Jika Anda ingin menjalankan ulang model atau memperluas sistem ini, semua komponen (dataset, model, script inference, dan dokumentasi) telah disusun secara modular dan transparan.

**Salam lestari,  
Tim EcoSortify ♻️**