class TorProxy:
    def __init__(self, socks_port=9050):
        self.socks_port = socks_port

    def get_proxy(self):
        """Return the proxy settings for requests."""
        return {
            'http': f'socks5://127.0.0.1:{self.socks_port}',
            'https': f'socks5://127.0.0.1:{self.socks_port}'
        }