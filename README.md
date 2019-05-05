# About smart estate

![alt text](https://github.com/MatusMak/smart-estate/blob/master/design/youtube_banner.png)

## What it does

We have decided to collect various information from available open data providers and public data sets and use them to rank places. This allows us to look at any given area from many different, often unrelated points of view, which results in a very good grading of such regions.

Users can either browse the map, where they can explore any place in the city, or compare to places to see the pros and cons. We have also handpicked several interesting places that we found to be a very nice regions of the city (at least according to our ranking model).

## How we built it

For backend, we have used Django as a webserver. For raking of places, we have created a custom modular detection system, which allows us to seamlessly and quickly add new providers and adjust their weight in the final calculations as necessary.

For frontend, we have used Vue.js with Bootstrap-Vue. Our page is built on top of Vue Argon scaffolding panel. Maps are provided by Open Street Map.

# Try it yourself

## Run frontend

1. First, install dependencies by running `npm install`
2. Run application:
    a) in development: `npm run dev`
    b) to build production files: `npm run build`

## Run backend

1. Create `backend/api_key.txt`, where you must include your `MojaPraha` API key
2. Install Django `pip install Django==2.2`
3. Make migrations `manage.py makemigrations`
4. Apply migrations `manage.py migrate`
5. Create superuser `manage.py createsuperuser`
6. Run server `manage.py runserver`
