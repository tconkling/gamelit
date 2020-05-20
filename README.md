# gamelit

Start the frontend:
```
$ cd frontend
$ yarn install
$ yarn start
```

Run the game:
```
$ python -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run app.py
```

## Issues

* I want to pass an image to my component.
    - Alternately, I want to pass a URL to a self-hosted image.
* I want to pass more data to my component _without rerunning my app_. But this is not currently possible; Streamlit thinks you're trying to register the component twice.
