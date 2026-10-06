#!/usr/bin/env python3
"""
regenerar_legado.py -- herramienta interna que el equipo de sistemas
de CITC usaba para el "Sistema Legado", pensada originalmente para
recuperar accesos cuando alguien se olvidaba una clave.

Uso:
    python3 regenerar_legado.py "una frase cualquiera"

Dada una frase de entrada, siempre devuelve el MISMO (n, e) -- es
determinista. Esta herramienta nunca muestra p ni q: solo regenera el
modulo publico n, igual que hacia originalmente con las claves reales
del sistema legado. Factorizar n para llegar a p, q, calcular d y
descifrar sigue siendo responsabilidad de quien la usa.
"""
import hashlib
import random
import sys

import sympy

E = 65537


def keygen_from_phrase(frase: str, bits: int = 34):
    digest = hashlib.sha256(frase.encode("utf-8")).digest()
    seed = int.from_bytes(digest, "big")
    rng = random.Random(seed)
    while True:
        raw_p = rng.getrandbits(bits) | (1 << (bits - 1))
        raw_q = rng.getrandbits(bits) | (1 << (bits - 1))
        p = sympy.nextprime(raw_p)
        q = sympy.nextprime(raw_q)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if sympy.gcd(E, phi) == 1:
            return p, q, p * q, E


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Uso: python3 {sys.argv[0]} "<frase>"')
        sys.exit(1)

    frase = sys.argv[1]
    _, _, n, e = keygen_from_phrase(frase)
    print(f"n = {n}")
    print(f"e = {e}")
