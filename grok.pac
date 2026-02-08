function FindProxyForURL(url, host) {
    // Направляем ВООБЩЕ ВСЁ через прокси для теста
    // Если инет станет медленным — вернем как было, но сейчас нам нужно поймать Грока
    return "PROXY grok-cert.onrender.com:443; DIRECT";
}
