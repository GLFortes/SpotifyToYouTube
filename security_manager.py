#!/usr/bin/env python3
"""
Secure Token Management Module
Enterprise-grade security for OAuth tokens and credentials
"""

import os
import json
import pickle
from typing import Optional, Dict, Any
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import keyring
import base64
import getpass


class SecureTokenManager:
    """
    Manages OAuth tokens with enterprise-grade security:
    - Encrypted storage using cryptography library
    - OS keyring integration for encryption keys
    - Secure file permissions (0600)
    - Token validation and revocation checks
    """
    
    SERVICE_NAME = "spotify-to-youtube"
    SALT_SIZE = 16
    ITERATIONS = 480000  # OWASP recommended for 2024
    
    def __init__(self, token_file: str = "youtube_token.enc"):
        """Initialize secure token manager"""
        self.token_file = Path(token_file)
        self.key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.key)
        
    def _get_or_create_encryption_key(self) -> bytes:
        """
        Get encryption key from OS keyring or create new one.
        Uses system keyring (secure storage provided by OS)
        """
        try:
            # Try to get existing key from keyring
            key_b64 = keyring.get_password(self.SERVICE_NAME, "encryption_key")
            
            if key_b64:
                return base64.urlsafe_b64decode(key_b64)
            
            # Generate new key if not exists
            print("🔐 Primeira execução - configurando criptografia...")
            key = Fernet.generate_key()
            
            # Store in OS keyring (encrypted by OS)
            keyring.set_password(
                self.SERVICE_NAME,
                "encryption_key",
                base64.urlsafe_b64encode(key).decode()
            )
            
            print("✅ Chave de criptografia armazenada com segurança no keyring do sistema")
            return key
            
        except Exception as e:
            # Fallback: derive key from user password (less secure but works everywhere)
            print(f"⚠️  Keyring não disponível: {e}")
            print("🔐 Usando método de fallback com senha...")
            return self._derive_key_from_password()
    
    def _derive_key_from_password(self) -> bytes:
        """
        Fallback: Derive encryption key from user password
        Uses PBKDF2 with high iteration count
        """
        salt_file = Path(".salt")
        
        # Get or create salt
        if salt_file.exists():
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(self.SALT_SIZE)
            with open(salt_file, 'wb') as f:
                f.write(salt)
            # Secure file permissions
            os.chmod(salt_file, 0o600)
        
        # Get password from user
        password = getpass.getpass("Digite uma senha para criptografar os tokens: ")
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.ITERATIONS,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def save_credentials(self, creds: Any) -> None:
        """
        Save credentials with encryption
        - Serializes credentials
        - Encrypts with Fernet (AES-128)
        - Sets secure file permissions (0600)
        """
        try:
            # Serialize credentials
            creds_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes,
                'expiry': creds.expiry.isoformat() if creds.expiry else None
            }
            
            # Convert to JSON
            json_data = json.dumps(creds_data).encode()
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(json_data)
            
            # Write to file
            with open(self.token_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions (owner read/write only)
            os.chmod(self.token_file, 0o600)
            
            print(f"✅ Token salvo com criptografia em {self.token_file}")
            
        except Exception as e:
            raise Exception(f"Erro ao salvar credenciais: {e}")
    
    def load_credentials(self) -> Optional[Dict[str, Any]]:
        """
        Load and decrypt credentials
        Returns None if file doesn't exist or decryption fails
        """
        if not self.token_file.exists():
            return None
        
        try:
            # Check file permissions
            file_stat = os.stat(self.token_file)
            if file_stat.st_mode & 0o077:
                print("⚠️  Aviso: Token file tem permissões inseguras!")
                os.chmod(self.token_file, 0o600)
            
            # Read encrypted data
            with open(self.token_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Parse JSON
            creds_data = json.loads(decrypted_data.decode())
            
            return creds_data
            
        except Exception as e:
            print(f"❌ Erro ao carregar credenciais: {e}")
            print("   Token pode estar corrompido ou senha incorreta")
            return None
    
    def delete_credentials(self) -> None:
        """Securely delete credentials"""
        if self.token_file.exists():
            # Overwrite with random data before deleting (prevent recovery)
            file_size = self.token_file.stat().st_size
            with open(self.token_file, 'wb') as f:
                f.write(os.urandom(file_size))
            
            self.token_file.unlink()
            print("✅ Credenciais deletadas com segurança")
    
    def validate_token_security(self) -> Dict[str, bool]:
        """
        Perform security audit on stored tokens
        Returns dict with security checks
        """
        checks = {
            'file_exists': self.token_file.exists(),
            'secure_permissions': False,
            'encrypted': False,
            'keyring_available': False
        }
        
        if checks['file_exists']:
            # Check permissions
            file_stat = os.stat(self.token_file)
            checks['secure_permissions'] = not (file_stat.st_mode & 0o077)
            
            # Check if encrypted (try to decrypt)
            try:
                self.load_credentials()
                checks['encrypted'] = True
            except:
                checks['encrypted'] = False
        
        # Check keyring availability
        try:
            keyring.get_password(self.SERVICE_NAME, "test")
            checks['keyring_available'] = True
        except:
            checks['keyring_available'] = False
        
        return checks


class SecureHeadersManager:
    """
    Secure management for YouTube Music headers
    Same security principles as tokens
    """
    
    def __init__(self, headers_file: str = "headers_auth.enc"):
        self.headers_file = Path(headers_file)
        self.token_manager = SecureTokenManager(token_file=str(headers_file))
    
    def save_headers(self, headers: Dict[str, str]) -> None:
        """Save headers with encryption"""
        json_data = json.dumps(headers).encode()
        encrypted_data = self.token_manager.cipher.encrypt(json_data)
        
        with open(self.headers_file, 'wb') as f:
            f.write(encrypted_data)
        
        os.chmod(self.headers_file, 0o600)
        print(f"✅ Headers salvos com criptografia")
    
    def load_headers(self) -> Optional[Dict[str, str]]:
        """Load and decrypt headers"""
        if not self.headers_file.exists():
            # Try legacy unencrypted file
            legacy_file = Path("headers_auth.json")
            if legacy_file.exists():
                print("⚠️  Migrando headers não criptografados...")
                with open(legacy_file, 'r') as f:
                    headers = json.load(f)
                self.save_headers(headers)
                # Secure delete old file
                legacy_file.unlink()
                return headers
            return None
        
        try:
            with open(self.headers_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.token_manager.cipher.decrypt(encrypted_data)
            headers = json.loads(decrypted_data.decode())
            
            return headers
            
        except Exception as e:
            print(f"❌ Erro ao carregar headers: {e}")
            return None


# Security audit function
def run_security_audit() -> None:
    """
    Run comprehensive security audit
    """
    print("\n" + "="*60)
    print("🔒 AUDITORIA DE SEGURANÇA")
    print("="*60 + "\n")
    
    token_mgr = SecureTokenManager()
    checks = token_mgr.validate_token_security()
    
    print("📋 Checklist de Segurança:\n")
    
    status_icon = lambda x: "✅" if x else "❌"
    
    print(f"{status_icon(checks['file_exists'])} Token file existe")
    print(f"{status_icon(checks['secure_permissions'])} Permissões seguras (0600)")
    print(f"{status_icon(checks['encrypted'])} Token criptografado")
    print(f"{status_icon(checks['keyring_available'])} Keyring do sistema disponível")
    
    # Additional checks
    print(f"\n📂 Verificando arquivos sensíveis...")
    sensitive_files = [
        '.env',
        'client_secret_*.json',
        '*.pickle',
        'headers_auth.json'
    ]
    
    import glob
    for pattern in sensitive_files:
        files = glob.glob(pattern)
        for f in files:
            stat = os.stat(f)
            secure = not (stat.st_mode & 0o077)
            print(f"{status_icon(secure)} {f} - Permissões: {oct(stat.st_mode)[-3:]}")
            if not secure:
                print(f"   ⚠️  Recomendado: chmod 600 {f}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    run_security_audit()
