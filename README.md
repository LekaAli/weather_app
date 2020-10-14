# Weather App
## App Setup:
1. create virtualenv: virtualenv --python=python3 <virtualenv-dir-name>
2. activate virtualenv: source <virtualenv-dir-name>/bin/activate
3. install app dependencies: pip install -r requirements.txt (i.e. requirements.txt is located inside the app)
4. set up the database: go into weather_app, run python weather_app/manage.py migrate
5. create user: python weather_app/manage.py createsuperuser (N.B: follow the prompts up until a is successfully created).

## Running the app:
python weather_app/manage.py runserver

## Access API View:
Generate token: http://127.0.0.1:8000/weather/api-view/obtain-token/. username and password created in point 5. will be required.
Weather API: http://127.0.0.1:8000/weather/api-view/?city={city-name}period={ccyy-mm-dd} (N.B: auth token is required. use postman or equivalent to access this endpoint).

## Access Web View:
To see a bar graph of the weather forecast: http://127.0.0.1:8000/weather/web-view/?city={city-name}period={ccyy-mm-dd} (N.B: no auth token is required to view the chart).

