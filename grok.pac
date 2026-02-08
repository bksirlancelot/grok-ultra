function FindProxyForURL(url, host) {
    // Добавляем все возможные вариации доменов Илона
    if (dnsDomainIs(host, "x.ai") || 
        dnsDomainIs(host, "api.x.ai") || 
        dnsDomainIs(host, "x.com") || 
        dnsDomainIs(host, "twitter.com") || 
        shExpMatch(host, "*.x.ai") || 
        shExpMatch(host, "*.x.com")) {
        
        // Попробуй изменить на HTTPS, если просто PROXY не дает логов
        return "HTTPS grok-cert.onrender.com:443; PROXY grok-cert.onrender.com:443; DIRECT";
    }
    return "DIRECT";
}
