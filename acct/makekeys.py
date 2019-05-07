# Create a new keypair for data signing

import nacl.encoding
import nacl.signing

# Generate a new random signing key
signing_key = nacl.signing.SigningKey.generate()
print (signing_key.encode(encoder=nacl.encoding.HexEncoder))

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key
print (verify_key.encode(encoder=nacl.encoding.HexEncoder))

