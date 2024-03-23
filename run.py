from app import create_app
from pyngrok import ngrok

app = create_app()

if __name__ == '__main__':
    port = 5000

    # Start ngrok when app is run, if in development environment
    if app.config['ENV'] == 'dev':
        public_url = ngrok.connect(port)
        print(f'Public URL: {public_url}')

    app.run(port=port, debug=True)
