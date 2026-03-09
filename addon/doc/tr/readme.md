# WhatsApp NG

Web tabanlı WhatsApp Masaüstü için erişilebilirlik iyileştirmeleri sağlayan bir NVDA eklentisi.

## Özellikler

* **Alt+1**: WhatsApp sohbet listesine git
* **Alt+2**: WhatsApp mesaj listesine git
* **Alt+D**: Mesaj yazma alanına odaklan
* **Enter**: Sesli mesajı oynat (bireysel sohbetlerde ve gruplarda çalışır)
* **Shift+Enter**: Mesaj bağlam menüsünü aç
* **Control+C**: Geçerli mesajı panoya kopyala
* **Control+R**: Mesajın tamamını oku (gerekirse "devamını oku" düğmesine tıklar)
* **Control+Shift+Enter**: Mesajı tepki ver

### Geçiş Komutları (varsayılan kısayol yoktur – Girdi Hareketleri'nden yapılandırılır)

* Sohbet listesinde telefon numarası filtrelemeyi aç/kapat
* Mesaj listesinde telefon numarası filtrelemeyi aç/kapat
* Otomatik Odak Modunu aç/kapat (gerektiğinde Gözden Geçirme Moduna izin verir)

## WhatsApp Masaüstü yerel klavye kısayolları

* Okunmadı olarak işaretle: Ctrl+Shift+U
* Bildirimleri sessize al: Ctrl+Shift+M
* Sohbeti arşivle: Ctrl+Shift+A
* Sohbeti sabitle: Ctrl+Alt+Shift+P
* Ara: Ctrl+Alt+/
* Sohbet içinde ara: Ctrl+Shift+F
* Yeni sohbet: Ctrl+Alt+N
* Sonraki sohbet: Ctrl+]
* Önceki sohbet: Ctrl+[
* Sohbete etiket ekle: Ctrl+Cmd+Shift+L
* Sohbeti kapat: Escape
* Yeni grup: Ctrl+Shift+N
* Profil ve Hakkında: Ctrl+Alt+P
* Seçili sesli mesaj hızını artır: Shift+.
* Seçili sesli mesaj hızını azalt: Shift+,
* Ayarlar: Alt+S
* Emoji paneli: Ctrl+Alt+E
* GIF paneli: Ctrl+Alt+G
* Çıkartma paneli: Ctrl+Alt+S
* Genişletilmiş arama: Alt+K
* Uygulamayı kilitle: Alt+L
* Sohbet ayrıntılarını aç: Alt+I
* Sohbeti engelle: Ctrl+Shift+B
* Yanıtla: Alt+R
* Özelden yanıtla: Ctrl+Alt+R
* Yönlendir: Ctrl+Alt+D
* Mesajı yıldızla işaretle: Alt+8
* Ek dropdown menüsünü aç: Alt+A
* PTT kaydı başlat: Ctrl+Alt+Shift+R
* PTT kaydını duraklat: Alt+P
* PTT gönder: Ctrl+Enter
* Son mesajı düzenle: Ctrl+Ok Üst
* Kamerayı Aç/Kapat: Ctrl+Alt+V
* Sessize Al/Sesi Aç: Ctrl+Alt+M
* Tepkiler: Ctrl+Alt+R
* El kaldır: Ctrl+Alt+H
* Ekran paylaşımı: Ctrl+Alt+S
* Aramayı sonlandır: Ctrl+Alt+W
* Yakınlaştır: Ctrl++
* Uzaklaştır: Ctrl+-
* Yakınlaştırmayı sıfırla: Ctrl+0
* Sohbet aç: Ctrl+1..9

## Gereksinimler

* NVDA 2021.1 veya daha yeni
* WhatsApp Desktop (web tabanlı sürüm)

## Kurulum

1. `whatsAppNG.nvda-addon` dosyasını indirin
2. NVDA’da **Araçlar → Eklenti Mağazası** yolunu izleyin
3. **Dış Kaynaktan Kur**’a tıklayın ve dosyayı seçin
4. NVDA’yı yeniden başlatın

## Yapılandırma

Telefon numarası filtreleri açılıp kapatılabilir:

* Sohbet listesinde: Girdi Hareketleri’nde bir kısayol yapılandırın
* Mesaj listesinde: Girdi Hareketleri’nde bir kısayol yapılandırın

Kısayolları şuradan yapılandırın:
**NVDA menüsü → Tercihler → Girdi Hareketleri → WhatsApp NG**

## Değişiklik Günlüğü

### Sürüm 1.5.0 (2026-03-05)

**Eklenen:**
- Ctrl+Shift+Enter: Mesaja tepki ver (reaksiyon menüsünü açar)
- Alt+Enter: Tamamı modunda tam mesajı oku
- WhatsApp Masaüstü yerel klavye kısayolları belgelere eklendi

**Değiştirildi:**
- Performans önemli ölçüde optimize edildi: Navigasyon artık daha akıcı ve duyarlı
- Alt+2 navigasyonda daha güvenilir ve hassas
- Ctrl+C artık sadece mesaj listesinde çalışıyor

**Düzeltildi:**
- Ctrl+R artık uzun mesajları genişletirken tam metni doğru okuyor

### Sürüm 1.4.0 (2026-02-23)

**Eklenenler:**
- Tam dil desteği: Arapça, Almanca, İspanyolca, İtalyanca ve Rusça
- Ukraynca çevirisi en recent dizgilerle güncellendi

**Düzeltilenler:**
- "Devamını oku" düğmesine tıklandıktan sonra Control+R'de "Metin bulunamadı" hatası
- Control+R artık sadece metin mesajlarında çalışıyor (ses/görseller için "Metin mesajı değil" gösterir)

**Değiştirilenler:**
- Depo bağlantıları yeni depoya güncellendi (nunotfc/WhatsAppNG)
- Belgeleme: Tüm yerelleştirilmiş README'ler artık 1.3.0 sürümüne kadar tam değişiklik günlüğünü içeriyor

### Sürüm 1.3.0 (2026-02-07)

**Eklenenler:**
* Türkçe çeviri desteği
* Otomatik Odak Modunu aç/kapat seçeneği (Girdi Hareketleri'nde hareket yapılandırın)

**Değiştirilenler:**
* İyileştirilmiş performans: Gezinme komutları artık tekrarlı kullanımda daha hızlı
* Escape tuhu artık doğru şekilde WhatsApp'a iletiliyor

**Düzeltilenler:**
* Enter artık video mesajlarını oynatıyor (önceden sadece ses için çalışıyordu)

### Sürüm 1.1.1 (2025-01-31)

**Eklenenler:**

* Control+R: Mesajın tamamını oku (otomatik olarak “devamını oku” düğmesine tıklar)
* Control+C: Geçerli mesajı panoya kopyala
* Tarama kipinin otomatik devre dışı bırakılması (WhatsApp deneyimi için odak kipini etkin tutar)

**Değiştirilenler:**

* Geliştirilmiş hata iletileri: Tüm komutlar artık başarısızlık durumunda net geri bildirim verir
* Gezinme komutları (Alt+1, Alt+2, Alt+D) artık başarı durumunda sessizdir
* Enter: Düğme sayma yerine kaydırıcı tabanlı algılama (daha güvenilir)

**Düzeltilenler:**

* Alt+1 ve Alt+2, tüm yollar başarısız olduğunda hataları doğru şekilde bildirir
* Girdi gecikmesini azaltmak için nesne filtreleme optimize edildi

### Sürüm 1.1.0 (2025-01-30)

**Eklenenler:**

* Control+R: Mesajın tamamını oku
* Kaydırıcı algılama kullanan akıllı sesli mesaj oynatma

**Değiştirilenler:**

* Enter: Düğme sayma yerine kaydırıcı algılamayı kullanan geliştirilmiş mantık

**Düzeltilenler:**

* Alt+2, ilk deneme başarısız olursa artık tüm gezinme yollarını doğru şekilde dener

### Sürüm 1.0.0 (2025-01-29)

**İlk sürüm:**

* Sohbet listesi, mesaj listesi ve mesaj yazma alanı için gezinme kısayolları
* Bireysel sohbetler ve gruplar için destekli sesli mesaj oynatma
* Mesaj işlemleri için bağlam menüsüne erişim
* Sohbetler ve mesajlar için telefon numarası filtreleme geçişi
* WhatsApp Desktop’ta odak kipinin otomatik etkinleştirilmesi

## Katkıda Bulunanlar

Modern WhatsApp Desktop deneyimi için erişilebilirlik iyileştirmeleri sağlamak amacıyla Nuno Costa tarafından geliştirilmiştir.

## Destek

Sorunlar veya öneriler için lütfen şurayı ziyaret edin:
https://github.com/nunotfc/whatsAppNG/issues

## Çeviri Derlemesi

Çevirileri güncellemek veya derlemek için:
```bash
scons pot
```

Bu işlem için GNU Gettext araçlarının yüklü olması gerekir.
