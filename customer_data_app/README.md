# Customer Data App

This app is used to showcase and edit tabular data live in an app. It links up with a persistent database, such as [Neon](https://neon.tech). 

## Usage 

First clone the repo locally.
```bash
git clone https://github.com/reflex-dev/templates/tree/main/customer_data_app
```
Then set up a virtual environment as outlined in our documentation. After this run `pip install -r requirements.txt`.

Next run the following reflex commands in your terminal:

```bash
reflex init
```

```bash
reflex db migrate
```

```bash
reflex run
```

The `init` command initializes the app. The `db migrate` command migrates your database. The `run` command runs your app.


## Setting an external Database

It is also possibe to set an external database so that your data is not lost every time the app closes and so you can deploy your app and maintain data. 

In the `rxconfig.py` file we accept a `DATABASE_URL` environment variable. 

To set one run the following command in your terminal:

```bash
export DATABASE_URL="<YOUR URL KEY>"
```