# Existing imports
from typing import Dict, Optional

# Existing imports (To Be Phased Out)
import base64
import json
import hmac
import hashlib

class JWT:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def _base64url_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

    def _base64url_decode(self, data: str) -> bytes:
        padding = '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data + padding)

    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            header_b64, payload_b64, signature_b64 = token.split('.')
            header = json.loads(self._base64url_decode(header_b64))
            payload = json.loads(self._base64url_decode(payload_b64))
            
            if header['alg'] != 'HS256':
                return None
            
            expected_signature = hmac.new(
                self.secret_key.encode(),
                f"{header_b64}.{payload_b64}".encode(),
                hashlib.sha256
            ).digest()
            
            if self._base64url_encode(expected_signature) != signature_b64:
                return None
            
            return payload
        except Exception:
            return None

    def get_unverified_header(self, token: str) -> Optional[Dict]:
        try:
            header_b64 = token.split('.')[0]
            header = json.loads(self._base64url_decode(header_b64))
            return header
        except Exception:
            return None
