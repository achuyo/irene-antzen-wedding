#!/usr/bin/env python3
"""
Builds planner.html from planner-source/panels.html + planner-source/shell_template.html,
encrypting the panel content with a password so it can be committed to a public repo
without exposing the plaintext.

This is a deterrent against casual snooping (family with the link poking around),
NOT real security. Anyone who really wants to could brute-force an offline copy of
planner.html given enough guesses, since PBKDF2/AES-GCM parameters are visible in
the file. Don't put anything here you'd be in real trouble for if it leaked.

Usage:
    python3 scripts/encrypt_planner.py

Run from the repo root. Prompts for a password (not echoed, not stored anywhere).
Regenerates ../planner.html at the repo root. Re-run any time panels.html changes.
"""
import base64
import getpass
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITERATIONS = 300_000
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
SOURCE_DIR = os.path.join(REPO_ROOT, "planner-source")


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def main():
    panels_path = os.path.join(SOURCE_DIR, "panels.html")
    template_path = os.path.join(SOURCE_DIR, "shell_template.html")
    output_path = os.path.join(REPO_ROOT, "planner.html")

    with open(panels_path, "r", encoding="utf-8") as f:
        plaintext = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    password = getpass.getpass("Planner password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("Passwords didn't match. Nothing was written.")
        return
    if len(password) < 8:
        print("Warning: that's a short password for something world-readable-encrypted. Consider something longer.")

    salt = os.urandom(16)
    iv = os.urandom(12)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)

    out = template
    out = out.replace("{{SALT}}", base64.b64encode(salt).decode("ascii"))
    out = out.replace("{{IV}}", base64.b64encode(iv).decode("ascii"))
    out = out.replace("{{ITERATIONS}}", str(ITERATIONS))
    out = out.replace("{{CIPHERTEXT}}", base64.b64encode(ciphertext).decode("ascii"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"Wrote {output_path}")
    print("Commit planner.html. Never commit anything in planner-source/ — it's gitignored on purpose.")


if __name__ == "__main__":
    main()
