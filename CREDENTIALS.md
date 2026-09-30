# Baidu API credentials

Set both `BAIDU_API_KEY` and `BAIDU_SECRET_KEY` in the environment before running
`test/LLM_generate.py`. The script reports a missing configuration before
making a request and passes credentials in the HTTPS form body.

Revoke or rotate the old credentials in the Baidu console. Removing the
hardcoded values does not remove them from Git history. Keep replacement
values in your local credential manager or environment and out of source and
logs.

The form request is described in Baidu's [Postman authentication guide](https://aca.bce.baidu.com/doc/OCR/s/skruaza7j).
