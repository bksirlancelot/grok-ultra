function FindProxyForURL(url, host) {
if (shExpMatch(host, "*.x.ai") || shExpMatch(host, "x.ai") || shExpMatch(host, "*.twitter.com") || shExpMatch(host, "x.com") || shExpMatch(host, "*.x.com")) {
// Убедись, что адрес совпадает с твоим Render (я взял из твоего текста)
return "PROXY grok-cert.onrender.com:443";
}
return "DIRECT";
}
