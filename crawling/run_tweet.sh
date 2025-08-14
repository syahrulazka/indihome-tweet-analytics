#!/bin/bash

# === Konfigurasi Parameter ===
TWITTER_AUTH_TOKEN="auth_token"  # Ganti dengan token kamu
FILENAME="juni3.csv"
SEARCH_KEYWORD="indihome since:2025-06-01 until:2025-06-17 lang:id"
LIMIT=100000

# Jalankan tweet-harvest
echo "🐦 Mengambil data Twitter untuk keyword: $SEARCH_KEYWORD"
npx -y tweet-harvest@2.6.1 -o "$FILENAME" -s "$SEARCH_KEYWORD" --tab "LATEST" -l "$LIMIT" --token "$TWITTER_AUTH_TOKEN"

echo "✅ Selesai. Data disimpan di: $FILENAME"
