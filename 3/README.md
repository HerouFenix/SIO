# Lab 3 - SIO 
# Applied Cryptography

# Setup
Install GHex, and the python3 cryptography module. That's basically it.
Also, check out https://cryptography.io/en/latest/


# 3.2  Symmetric Cryptography
_**Symmetric cryptography** is used by creating an object that represents a given **cipher**, with some parameters specifying the mode, as well as a **key**. The cipher object presents an encryption method, that is applied (update) to the text in chunks (may require alignment with the cipher block size). After the text is ciphered, a finalize method may be used. Decryption is done in a similar way. It should be noticed that we will directly use the base cryptographic primitives, which imply that the ciphers are constructed with reasonable parameters._

## 3.2.1 Symmetric key generation
_Before a cipher is used, it is the generation of proper arguments is required.These arguments are the **key**, the **cipher mode**, and potentially the **Initialization Vector** (IV). The cipher mode is chosen at design time, and the IV should always be a large random number (size similar to the block size or key) that is never repeated. This lab will discuss the IVs in the next sections.The key can be obtained from good sources of random numbers, or generated from other primitive material such as a password. When choosing the last source (a password), it is imperative to transform the user text into a key of the correct complexity. While there are many methods, we will consider the **Password Based Key Derivation Function 2** (PKBDF2), which takes a key,a random value named salt, a digest algorithm, and a number of iterations (you should use several thousands). The algorithm will iterate the digest algorithm in a chain starting in the concatenation of the salt and key, for the specified number of iterations. Using Secure Hash Algorithm 2 (SHA-2), the result is at least 256 bits, which can be used as a key._

### Exercise
_Construct a small function that generates and returns a symmetric key from a password. The algorithm name for the symmetric key and the file name should be provided as an argument. For testing purposes, the algorithm should be provided by the user as an argument and you can use the following algorithms: Triple Data Encryption Standard (3DES), Advanced Encryption Standard 128 bits (AES-128) and Salsa20 variant ChaCha20 (ChaCha20)._

See https://nitratine.net/blog/post/encryption-and-decryption-in-python/

### Solution

```


```

# References
https://joao.barraca.pt/teaching/sio/2019/p/guide-Crypto-en.pdf
https://cryptography.io/en/latest/

### Diogo Silva, 2019

