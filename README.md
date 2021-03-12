# ct200_test
Test for magic key ideas

To run this you need python >= 3.8:

## Prepare
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

CREATE .env file like env.example
```
HOST=""
ACCESS_KEY=""
PASSWORD=""
TO_DECRYPT=""
```

Leave TO_DECRYPT empty for now.
Don't put spaces and `-` in password or access key.

Run in venv:
```
python test.py
```

Find line in output which looks like
```
Decrypting 5OKcIRgBkdCuWrHyz3aD3zmcK/ni+wcQlAT4xvNvhgCfvJkp2tRLMRfHAFvAdwDoDNmhlUet3gueigyNjY9boJQ1j3rm+weq02JnJ8Vuj7nF9VqdPByl0T+AsXBw12dHt
```

Copy this string into your TO_DECRYPT env var.

Re-run `python test.py`
It will try to decrypt it without connecting to XMPP server against 3 different MAGIC.

You can try to find 32 bytes MAGIC (if it is the method XMPP server uses.)

CREATE ISSUE WITH MAGIC IF YOU THINK YOU FOUND IT!
