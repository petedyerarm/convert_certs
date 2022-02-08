# convert_certs

Generate x509 certificates and convert them into C code.

# Generate from scratch

```generate_self_signed.sh --endpoint <endpoint_name>```

This will generate a private key and a self_signed certificate, and convert them into a C file (credentials.c)

# Convert existing certificate files

```cert_convert.py --public <public_file> --private <private_file> --out <credentials_file>```

