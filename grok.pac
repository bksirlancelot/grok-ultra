function FindProxyForURL(url, host) {
    if (shExpMatch(host, "*.x.ai")  shExpMatch(host, "x.ai")  shExpMatch(host, "*.twitter.com") || shExpMatch(host, "x.com")) {
        return "PROXY grok-ultra.onrender.com:10000";
    }
    return "DIRECT";
}
