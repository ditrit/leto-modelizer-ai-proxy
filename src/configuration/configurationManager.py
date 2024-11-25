import os
import asyncio
import json
import hashlib
from Crypto.Cipher import AES
from fastapi import HTTPException
from http import HTTPStatus


class ConfigurationManager:
    """
    A Singleton class for managing configuration settings.
    """

    _instance = None
    _configuration = {}
    _lock = asyncio.Lock()

    # Constants for AES decryption
    IV_SIZE = 12  # Adjust according to the Java constant IV_SIZE
    KEY_SIZE = 16  # AES-256 uses a 256-bit (32-byte) key
    GCM_TAG_LENGTH = 16  # Typically 128-bit (16-byte) tag for GCM

    def __new__(cls, *args, **kwargs):
        """
        Create a new instance of the class.

        This method is a special method in Python that is called when a new instance of the class is created.
        It is responsible for creating and returning a new instance of the class.

        Parameters:
            cls (type): The class object.
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.

        Returns:
            object: The newly created instance of the class.

        Note:
            This method is used to implement the Singleton design pattern, where only one instance of the class can exist.
            It ensures that only one instance of the class is created and returned whenever a new instance is requested.
        """

        if not cls._instance:
            cls._instance = super().__new__(cls)
            print(
                f"Creating new ConfigurationManager instance with id: {id(cls._instance)}"
            )
        return cls._instance

    def reset(cls):
        """
        Resets the class by setting the `_instance` attribute to `None` and the `_reset` attribute to `True`.

        Parameters:
            cls (type): The class object.
        """
        cls._instance = None
        cls._configuration = {}

    def decrypt(self, key: str, encrypted_iv_text_bytes: bytes) -> str:
        """
        Decrypts the given encrypted data using AES in GCM mode with the given key.

        :param key: The key to use for decryption.
        :param encrypted_iv_text_bytes: The encrypted data to decrypt.
        :return: The decrypted data as a string.
        :raises Exception: If decryption fails.
        """
        try:
            # Extract IV
            iv = encrypted_iv_text_bytes[: self.IV_SIZE]

            # Extract encrypted part
            encrypted_bytes = encrypted_iv_text_bytes[self.IV_SIZE :]

            # Hash key
            key_bytes = hashlib.sha256(key.encode("utf-8")).digest()[: self.KEY_SIZE]

            # Decrypt using AES in GCM mode
            cipher = AES.new(
                key_bytes, AES.MODE_GCM, nonce=iv, mac_len=self.GCM_TAG_LENGTH
            )
            decrypted_bytes = cipher.decrypt_and_verify(
                encrypted_bytes[: -self.GCM_TAG_LENGTH],
                encrypted_bytes[-self.GCM_TAG_LENGTH :],
            )

            return decrypted_bytes.decode("utf-8")
        except Exception:
            raise Exception("Failed to decrypt")

    def get_configuration(self):
        """
        Gets the remote configuration.

        :return: The remote configuration as a json object.
        :raises Exception: If the remote configuration is not set.
        """

        if not self._configuration:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="The required configuration is not set. Please set up the configuration and try again.",
            )

        return self._configuration

    def __create_nested_dict(self, data):
        """
        Creates a nested dictionary from a dictionary with dotted keys.

        The input dictionary should have keys in the format "key1.key2.key3" and
        the function will create a nested dictionary with the same structure.

        :param data: The input dictionary with dotted keys.
        :return: The nested dictionary.
        :rtype: dict
        """
        nested_dict = {}
        for dotted_key, value in data.items():
            keys = dotted_key.split(".")
            current_dict = nested_dict
            for key in keys[
                :-1
            ]:  # Traverse/create all sub-dictionaries except the last key
                current_dict = current_dict.setdefault(key, {})
            current_dict[keys[-1]] = value  # Set the value at the deepest level
        return nested_dict

    async def set_configuration(
        self, encrypted_configuration: bytes, decryption_key: str = None
    ):
        """
        Sets the remote configuration.
        The configuration is decrypted using the provided key and then converted to a nested dictionary.

        :param encrypted_configuration: The configuration to set encrypted.
        :param decryption_key: The key to use for decryption.
        :raises json.decoder.JSONDecodeError: If the decrypted configuration is not a valid json.
        """
        async with self._lock:
            decryption_key = decryption_key or os.environ.get("DECRYPTION_KEY")
            decrypted_configuration = self.decrypt(
                decryption_key, encrypted_configuration
            )
            try:
                decrypted_configuration = json.loads(decrypted_configuration)
                decrypted_configuration_to_dict = self.__create_nested_dict(
                    decrypted_configuration
                )
            except json.decoder.JSONDecodeError:
                raise json.decoder.JSONDecodeError("Not a valid json")
            self._configuration = decrypted_configuration_to_dict
