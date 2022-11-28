# Amazon CAPTCHA solver

A CNN-based Amazon CAPTCHA solver

## Components
1. Dummy Amazon frontend with CAPTCHA (runs on Flask)
2. Chrome Browser extension that grabs CAPTCHA image and sends it over to backend
3. Extension backend Flask server that interprets CAPTCHA image based on a Convolutional Neural Network Model

## Getting started
1. Launch the Amazon frontend server and captcha solver server in separate terminal instances using

```console
    $  python3 server.py
```

2. Install the extension on Google Chrome by enabling Developer mode
