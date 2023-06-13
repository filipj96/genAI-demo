# wine-genai

## running locally
### backend setup
You need a recent Python version, tested with Python 3.9.6

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r backend/requirements.txt
```

Add a `.env` file to `backend` and `emeddings` directories. It shoul have the following content.
```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

### frontend setup
You need a recent Node version, tested with Node v16.19.1
```
npm install
npm run build
```

### run the application
```
python3 backend/app.py
```