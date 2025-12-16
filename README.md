# FP-Vtuber-PCV
# Real-Time VTuber Tracking (Unity + Python)

## Deskripsi
Project ini merupakan sistem **real-time VTuber tracking** yang mengintegrasikan  
**Python (Computer Vision)** dengan **Unity + Live2D Cubism SDK**.

Python digunakan untuk melakukan tracking pergerakan pengguna melalui webcam,  
sedangkan Unity digunakan untuk menampilkan dan menggerakkan karakter Live2D  
secara real-time berdasarkan data tracking yang diterima.


---

## Fitur
- Head tracking (rotasi kepala X & Y)
- Eye tracking (arah mata & buka/tutup mata)
- Mouth tracking (bukaan mulut)
- Body movement (rotasi badan mengikuti kepala)
- Hand tracking (tangan kiri & kanan)
- Komunikasi real-time menggunakan UDP

---

## Yang Dibutuhkan
### Python
- Python 3.8 
- OpenCV
- MediaPipe
- UDP Socket

### Unity
- Unity Engine
- Live2D Cubism SDK
- C# Scripting

---

Struktur Folder
``` bash
ProjectRoot/
│
├── Model/
│   ├── Scripts/
│   ├── runtime/
│   ├── mao_pro_t06.can3
│   └── ReadMe.txt
│
├── Python/
│   ├── Body_tracking.py
│   ├── Eye_tracking.py
│   ├── Hand_tracking.py
│   ├── Head_tracking.py
│   ├── Mouth_tracking.py
│   ├── UDPSender.py
│   ├── main.py
│   └── requirement.txt
│
└── README.md
```

---
\
## Cara Menjalankan
### Python
1. Pastikan webcam aktif
2. Install dependency:
```bash
pip install -r requirement.txt
```
---

### Unity
1. Buka project di Unity Hub  
2. Pastikan Live2D Cubism SDK sudah terpasang  
3. Pastikan model Live2D tersedia  
4. Buka scene utama  
5. Klik **Play**

### Demo
Saat Python dan Unity berjalan bersamaan, karakter Live2D akan mengikuti:
- Gerakan kepala dan badan  
- Kedipan mata real-time  
- Bukaan mulut  
- Gerakan tangan kiri dan kanan  

Bagian ini merupakan demo langsung dari sistem tracking yang dibuat.

