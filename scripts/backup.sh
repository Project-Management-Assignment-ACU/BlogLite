#!/bin/bash

# BlogLite SQLite Veritabanı Yedekleme Betiği

# Yapılandırma
DB_PATH="db.sqlite3"
BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/bloglite_${DATE}.sqlite3"

# Hata mesajları için renk tanımlamaları
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Yedekleme dizinini kontrol et ve oluştur
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo -e "${GREEN}Yedekleme dizini oluşturuldu: $BACKUP_DIR${NC}"
fi

# Veritabanı dosyasının varlığını kontrol et
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}Hata: Veritabanı dosyası bulunamadı: $DB_PATH${NC}"
    exit 1
fi

# Veritabanını yedekle
echo "Veritabanı yedekleniyor..."
if cp "$DB_PATH" "$BACKUP_PATH"; then
    echo -e "${GREEN}Yedekleme başarılı: $BACKUP_PATH${NC}"

    # Yedek dosyasının boyutunu kontrol et
    BACKUP_SIZE=$(ls -lh "$BACKUP_PATH" | awk '{print $5}')
    echo "Yedek dosyası boyutu: $BACKUP_SIZE"

    # Toplam yedek sayısını göster
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.sqlite3 2>/dev/null | wc -l)
    echo "Toplam yedek sayısı: $BACKUP_COUNT"
else
    echo -e "${RED}Hata: Yedekleme başarısız${NC}"
    exit 1
fi

# Eski yedekleri temizle (30 günden eski)
find "$BACKUP_DIR" -name "*.sqlite3" -type f -mtime +30 -delete 2>/dev/null
if [ $? -eq 0 ]; then
    echo "30 günden eski yedekler temizlendi"
fi

exit 0
