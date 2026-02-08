function FindProxyForURL(url, host) {
    // Исправленный синтаксис с логическим ИЛИ (||)
    if (shExpMatch(host, "*.x.ai") || shExpMatch(host, "x.ai") || shExpMatch(host, "*.twitter.com") || shExpMatch(host, "x.com") || shExpMatch(host, "*.x.com")) {
        // Обязательно проверь, что адрес Render правильный!
        return "PROXY grok-cert.onrender.com:443";
    }
    return "DIRECT";
}
