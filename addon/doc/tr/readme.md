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

### Geçiş Komutları (varsayılan kısayol yoktur – Girdi Hareketleri'nden yapılandırılır)

* Sohbet listesinde telefon numarası filtrelemeyi aç/kapat
* Mesaj listesinde telefon numarası filtrelemeyi aç/kapat
* Otomatik Odak Modunu aç/kapat (gerektiğinde Gözden Geçirme Moduna izin verir)

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
