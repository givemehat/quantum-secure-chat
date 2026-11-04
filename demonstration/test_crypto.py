import pytest

from crypto import decrypt, encrypt


def test_round_trip_unicode_message():
    key = "01001101"
    message = "Confidential ✅"

    ciphertext = encrypt(message, key)

    assert ciphertext != message
    assert decrypt(ciphertext, key) == message


def test_wrong_key_is_rejected():
    ciphertext = encrypt("secret", "0101")

    with pytest.raises(ValueError):
        decrypt(ciphertext, "1010")


def test_invalid_key_is_rejected():
    with pytest.raises(ValueError):
        encrypt("secret", "not-bits")
