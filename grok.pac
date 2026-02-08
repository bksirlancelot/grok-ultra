function FindProxyForURL(url, host) {
    // Направляем всё, что связано с X, принудительно
    if (shExpMatch(host, "*.x.ai") || shExpMatch(host, "x.ai") || shExpMatch(host, "api.x.ai") || shExpMatch(host, "*.x.com") || shExpMatch(host, "x.com")) {
        return "PROXY grok-cert.onrender.com:443; PROXY grok-cert.onrender.com:80; DIRECT";
    }
    return "DIRECT";
}
