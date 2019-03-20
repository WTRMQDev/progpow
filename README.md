# About
Python progpow wrapper. Avaibale on [PyPI](https://pypi.org/project/progpow).

Currently supports only python3+ and linux.

# Progpow versions 
Currently support 0.9.2 and 0.9.3 progpow versions. BitcoinInterest progpow version is not supported.

# Install
`pip3 install progpow`

# Interface 
```python
import progpow

handler = progpow.ProgPowHandler(max_contexts_num=1, version='0.9.2')
handler.hash(header_height, header_hash, nonce)
```

ProgPowHandler implicitly generates light cache for epochs (once every 30000 blocks) on fly and store it in memory. `max_contexts_num` control how much contexts will be stored simultaneously.

`header_heigh` and `nonce` should be passed as integers

`header_hash` should be passed as bytes

Result is returned as bytes.
