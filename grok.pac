function FindProxyForURL(url, host) {
    // Проверяем, что запрос идет к X.ai или Twitter
    if (shExpMatch(host, "*.x.ai") || shExpMatch(host, "x.ai") || shExpMatch(host, "*.twitter.com") || shExpMatch(host, "x.com") || shExpMatch(host, "*.x.com")) {
        // Замени 'grok-cert.onrender.com' на реальное название твоего сервиса в Render, если оно другое!
        return "PROXY grok-cert.onrender.com:443";
    }
    // Весь остальной трафик пускаем напрямую, чтобы инет не сдох
    return "DIRECT";
}
