# Existing imports
from typing import Dict, Optional
import json

# Custom imports
from sha256 import SHA256

class JWT:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def _base64url_encode(self, data: bytes) -> str:
        # Custom base64url encoding
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        encoded = ""
        padding = 0
        for i in range(0, len(data), 3):
            chunk = data[i:i+3]
            if len(chunk) < 3:
                padding = 3 - len(chunk)
                chunk += b'\x00' * padding
            b = int.from_bytes(chunk, 'big')
            for j in range(18, -1, -6):
                encoded += base64_chars[(b >> j) & 0x3F]
        if padding:
            encoded = encoded[:-padding]
        return encoded

    def _base64url_decode(self, data: str) -> bytes:
        # Custom base64url decoding
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

        # Pad data if necessary
        if len(data) % 4 != 0:
            data += 'A' * (4 - len(data) % 4)

        decoded = bytearray()
        for i in range(0, len(data), 4):
            chunk = data[i:i+4]
            b = 0
            for char in chunk:
                b = (b << 6) + base64_chars.index(char)
            bytes_to_add = b.to_bytes(3, 'big')
            decoded.extend(bytes_to_add)
        decoded_bytes = str(bytes(decoded).rstrip(b'\x00'), 'utf-8')
        return decoded_bytes

    def _hmac_sha256(self, key: bytes, msg: bytes) -> bytes:
        # Custom HMAC-SHA256 implementation
        
        block_size = 64
        if len(key) > block_size:
            key = self._sha256(key)
        key = key.ljust(block_size, b'\x00')
        o_key_pad = bytes((x ^ 0x5C) for x in key)
        i_key_pad = bytes((x ^ 0x36) for x in key)
        return self._sha256(o_key_pad + self._sha256(i_key_pad + msg))

    def _sha256(self, data: bytes) -> bytes:
        hasher = SHA256()
        return hasher.hash(data).encode()

    def verify_token(self, token: str) -> Optional[Dict]:
        try:
            header_b64, payload_b64, signature_b64 = token.split('.')
            header = json.loads(self._base64url_decode(header_b64))
            payload = json.loads(self._base64url_decode(payload_b64))
            
            if header['alg'] != 'HS256':
                return None
            
            expected_signature = self._hmac_sha256(
                self.secret_key.encode(),
                f"{header_b64}.{payload_b64}".encode()
            )
            
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
        
    def encode(self, payload: Dict) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        header_b64 = self._base64url_encode(json.dumps(header).encode())
        payload_b64 = self._base64url_encode(json.dumps(payload).encode())
        signature = self._hmac_sha256(
            self.secret_key.encode(),
            f"{header_b64}.{payload_b64}".encode()
        )
        signature_b64 = self._base64url_encode(signature)
        return f"{header_b64}.{payload_b64}.{signature_b64}"
    
    def decode(self, token: str) -> Optional[Dict]:
        try:
            header_b64, payload_b64, signature_b64 = token.split('.')
            header = json.loads(self._base64url_decode(header_b64))
            payload = json.loads(self._base64url_decode(payload_b64))

            return payload
        except Exception:
            return None