function FindProxyForURL(url, host) {
    // Направляем все запросы, связанные с Гроком и X, на твой новый Render
    if (shExpMatch(host, "*.x.ai") || shExpMatch(host, "x.ai") || shExpMatch(host, "*.twitter.com") || shExpMatch(host, "x.com")) {
        return "PROXY grok-ultra.onrender.com:10000";
    }
    // Весь остальной интернет пускаем напрямую
    return "DIRECT";
}
