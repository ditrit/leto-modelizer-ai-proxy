import pytest
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from fastapi import HTTPException
from unittest import TestCase, IsolatedAsyncioTestCase
from src.configuration.configurationManager import ConfigurationManager


def encrypt_test_function(key: str, plain_text: str) -> bytes:
    """
    Encrypts the given plaintext using AES in GCM mode with the given key.
    Creating this method here for testing purposes.
    Its taken from leto-modelizer-api just for testing the decryption, so not used in leto-modelizer-ai-proxy
    :param key: The key to use for encryption.
    :param plain_text: The plaintext to encrypt.
    :return: The encrypted data as bytes.
    :raises Exception: If encryption fails.
    """
    try:
        # Convert plaintext to bytes
        clean = plain_text.encode("utf-8")
        # Generate IV
        IV_SIZE = 12  # Standard size for AES GCM IV
        iv = get_random_bytes(IV_SIZE)
        # Hash the ke
        # y using SHA-256
        KEY_SIZE = 16
        digest = SHA256.new()
        digest.update(key.encode("utf-8"))
        key_bytes = digest.digest()[:KEY_SIZE]
        # Create cipher and encrypt
        cipher = AES.new(key_bytes, AES.MODE_GCM, nonce=iv)
        encrypted, tag = cipher.encrypt_and_digest(clean)
        # Combine IV, encrypted text, and tag
        encrypted_iv_and_text = iv + encrypted + tag
        return encrypted_iv_and_text
    except Exception as e:
        raise Exception("Failed to encrypt: " + str(e))


class TestConfigurationManager(TestCase):

    def tearDown(self) -> None:
        ConfigurationManager().reset()

    def test_configuration_singleton(self):
        """
        Tests the singleton pattern implementation of the ConfigurationManager class.

        This test verifies that only one instance of ConfigurationManager is created
        and used, even when multiple instances are requested.

        Asserts:
            - Both instances retrieved are the same instance.
        """
        config_manager1 = ConfigurationManager()
        config_manager2 = ConfigurationManager()
        self.assertIs(config_manager1, config_manager2)

    def test_decryption(self):
        """
        Tests the decryption functionality of the ConfigurationManager class.

        This test encrypts a sample JSON string using a predefined key and
        verifies that the decrypt method can successfully decrypt it back to
        the original string. It also checks that an exception is raised when
        attempting to decrypt with an incorrect key.

        Asserts:
            - The decrypted text matches the original text.
            - Decryption with a wrong key raises an exception with the message "Failed to decrypt".
        """
        key = "123456789"
        original_config = '{"config1": "my_ai"}'
        encrypted_config = encrypt_test_function(key, original_config)

        decrypted_text = ConfigurationManager().decrypt(key, encrypted_config)
        self.assertEqual(original_config, decrypted_text)

        with pytest.raises(Exception, match="Failed to decrypt"):
            ConfigurationManager().decrypt("wrong_key", encrypted_config)


class TestAsyncConfigurationManager(IsolatedAsyncioTestCase):

    async def test_configuration_get_set_configuration(self):
        """
        Tests the get and set configuration methods of the ConfigurationManager class.

        This test verifies that an exception is raised when attempting to get the configuration when it is not set.
        It also checks that the configuration can be successfully set using the set_configuration method and
        then retrieved using the get_configuration method.

        Asserts:
            - Getting the configuration when it is not set raises an exception.
            - Setting the configuration and then getting it results in the original configuration.
        """
        config_manager = ConfigurationManager()

        ## No configuration
        with pytest.raises(
            HTTPException,
            match="The required configuration is not set. Please set up the configuration and try again.",
        ):
            config_manager.get_configuration()

        ## With configuration
        key = "123456789"
        original_config = '{"config1": "my_ai"}'
        encrypted_config = encrypt_test_function(key, original_config)

        await config_manager.set_configuration(encrypted_config, key)
        config = config_manager.get_configuration()
        self.assertEqual(config, json.loads(original_config))
