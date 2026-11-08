import cv2
import datetime
import os

# --- KONFİGÜRASYON VE PARAMETRELER ---
# Güvenli bölgenin koordinatları (x, y, genişlik, yükseklik)
# Gerçek bir projede bu değerler kullanıcı arayüzünden (GUI) dinamik olarak alınır.
SECURE_ZONE = (150, 100, 400, 300) 
MIN_CONTOUR_AREA = 500 # Algılanacak hedefin minimum piksel alanı (Kuş, böcek engellemek için)
LOG_FILE = "intrusion_logs.txt"

def check_intersection(box1, box2):
    """
    İki dikdörtgenin (AABB) kesişip kesişmediğini kontrol eden matematiksel fonksiyon.
    box formatı: (x, y, w, h)
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    
    # Eğer bir kutu diğerinin tamamen sağında, solunda, üstünde veya altındaysa kesişim YOKTUR.
    if x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2:
        return False
    return True

def log_intrusion():
    """İhlal durumunda zaman damgası ile log tutan fonksiyon."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[WARNING] İhlal Tespit Edildi! Zaman: {timestamp}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_message)
    print(log_message.strip())

def main():
    # Video kaynağını başlat (0: Dahili web kamerası, veya "video.mp4" gibi bir dosya yolu)
    cap = cv2.VideoCapture(0)
    
    # Arka plan çıkarma algoritmasını (MOG2) başlat
    # history: Geçmiş frame sayısı, varThreshold: Mahalanobis mesafesi eşiği (yanlış alarm duyarlılığı)
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
    
    # İhlal durumu takibi için bayrak (Flag)
    # Aynı ihlalin saniyede 30 kez loglanmasını engellemek için kullanacağız.
    is_intrusion_active = False 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Görüntü okunamadı veya video bitti.")
            break
            
        # Görüntüyü yeniden boyutlandır (İşlem yükünü azaltmak için)
        frame = cv2.resize(frame, (640, 480))
        
        # 1. ÖN İŞLEME (Pre-processing)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 2. HAREKET TESPİTİ (Background Subtraction)
        fg_mask = back_sub.apply(blur)
        
        # Gölgeleri (MOG2'de gri renktir) ve küçük gürültüleri temizle
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)
        
        # 3. KONTUR (Hedef) ÇIKARMA
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        current_frame_intrusion = False
        
        # Her bir tespit edilen nesne için döngü
        for contour in contours:
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue # Çok küçük nesneleri (gürültü) yoksay
                
            # Hedefin koordinatlarını al
            (x, y, w, h) = cv2.boundingRect(contour)
            target_box = (x, y, w, h)
            
            # Hedefi yeşil kutu içine al (Normal durum)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 4. İHLAL (Kesişim) KONTROLÜ
            if check_intersection(target_box, SECURE_ZONE):
                current_frame_intrusion = True
                # İhlal yapan hedefi kırmızı kutu ile işaretle
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
        # 5. GÜVENLİ BÖLGEYİ ÇİZME VE DURUM GÜNCELLEMESİ
        zx, zy, zw, zh = SECURE_ZONE
        zone_color = (0, 255, 0) # Varsayılan: Yeşil (Güvenli)
        
        if current_frame_intrusion:
            zone_color = (0, 0, 255) # İhlal anında: Kırmızı (Tehlike)
            cv2.putText(frame, "!!! INTRUSION DETECTED !!!", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
            # State machine mantığı: Sadece ilk ihlal anında log at, sürekli log spam'i yapma
            if not is_intrusion_active:
                log_intrusion()
                is_intrusion_active = True
        else:
            # Hedef bölgeden çıkınca durumu sıfırla
            is_intrusion_active = False
            
        # Güvenli bölge sınırlarını ekrana çiz
        cv2.rectangle(frame, (zx, zy), (zx + zw, zy + zh), zone_color, 2)
        cv2.putText(frame, "SECURE ZONE", (zx, zy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, zone_color, 2)

        # Görüntüleri ekrana ver
        cv2.imshow("SecureZone - Tactical Display", frame)
        cv2.imshow("Foreground Mask (Debug)", fg_mask) # Mülakatta maskeyi göstermek puan kazandırır
        
        # Çıkış koşulu: 'q' tuşu
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()