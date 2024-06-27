# Simulateur

![Django](https://img.shields.io/badge/Django-3.2-blue)
![React](https://img.shields.io/badge/React-18.3.1-blue)
![Vite](https://img.shields.io/badge/Vite-2.9.9-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue)

## Project Overview

Simulateur is a stock market simulation platform built using Django for the backend and React with Vite for the frontend. The platform allows users to create and manage companies, stocks, and scenarios to simulate stock market events and track their outcomes. It includes an admin interface to manage the simulation settings and control the flow of the simulation.

![Diagram](https://www.plantuml.com/plantuml/dpng/ZPF1JW8n48Rl-nGJxhm3oabZ8h5mDkCoMHgxBMcd6j_URTawsoq7JvJl_oQPC3-xmEWvZgR3dfs7Ko0_Fn_EexRp-zKFQ7NAkXYenq2mIIgyk47R3M20q_uzaGn4UdRQmf5mB4u2wRieZ_475Bl-CnHd8ZSWaY9ZLbP2ioPUNhhUAgFLMdjFo0Ig9ujUkwBUSA4B_O9sc7HYrdO8HR_XGfUwSzFdKO_aGJ5TuSao-IyqCfcCBAHSHW_nm-XmQJQRURkQIlS3fSTeaBMpPI1pmTt_9yGyuFIyOsPUcOhTzOwOSErTtFV2WpSAqR2ST8gdTAPTbokstTRT4YXb4YRb4LXt9VTXvj8DmMqF96fkBb5xLCcQ-rLPSwg_VzjAM0ToY7R2NHlU_i0xikSucby0)

![Diagram](https://www.plantuml.com/plantuml/dpng/ZLJBRjim4BppAmYVOWW9qgjEATe6BOgc0QoU1PfQEOJv4CXb0hVeltTfsHJLo80lfYNkpimEXte8A3n6erdOApi8BmoNMeJm4T6hRKJu9ftTgD_0xnaxxl1FpWp27lWVLbbXeEORAhKxLcs5t0Tq_f1V_JtrqBEJ-zGXn-QQFpeFQcU_m-7c1BXc5Igv1pyX3bv9e5hj1BAAaB2DGoSGkff_fgLH1YQI1eHvhyg0sO8FDVz178rBluyAT7VpAu1_zgvN6jOJIF4sOSMGzFoqq3ZwcHhNQLmjR24FYNusLz9J86-KYLgW8Zy1aRI5H80qWcy3mb3pfvYaighNKM8ybhPUu4G1hs2nvbzeIOHUxNP9NZF-AQWaME6LU-z61q5wDIJenOFBTQhlbOmQ3wqcLbtiH7zKbkLcrcVdiNTwf7LlTj6vRAxpV3Ie2YaS2mTq34rXOEE53K8cyg_gg3SH3MVMcVTPIqhLrDVYOIZS4CP5YzdUUTnIpfPYzWHlfvD3NM19Pn4i5k6DMwt22tJj76b-Z1btVBpon9GPQA1vBcQpNPH_3ijLH3bZ9NRnzbNek9pEfTYJ5a6qj7F-XAm-hFZjBL_TtzsjJj-8cbDo0YkJKbJHlnGQgXglDNSzos5F1GNUcQJcoaeTQRoBfGbpgIvJqx9mVOkEXTrokEpwzIsZZqN3eYUqvAXJxOi8B3_dAKk32y3BbGithUOUfFDTOAEk_phIfIYXp_EMPSLCfm05Da_7LJfY8Fm7i5qq-Xy0)

![Diagram](https://www.plantuml.com/plantuml/dpng/TPBFxjGW4CVlFCLaJthm1NemcwmcZV50B7s0MPXQb38DK6FVNbgwMrdzNRz_PZvakCQ48IsJ4wWJ1-WZ1J5doMexeqzmsHGPUB2EBe0HUbdxYd3Q3LNhaaCQs5dUpPTIbrZ_t8tkPLf07pEAPT_Qc3YiPNOhn0O27pvcW0Q-ydVhtxqNlToLx3JmoSRPuGhBbZCOnpjZC7NlDZ97WfIPZwvgu0jRNoJrpB4VR9Xs5Nvalzga7YePq2M96_6vgskW8mnwX843nEsreli7jHXWAA5ryMpBhUr8foEG6ExBAkGn-JPI5ek5lt8LxzRPj9OD9_t_8l8jY7d9j1W9UAwUKishaa-Upxz9BubUx4AZsWQ-aUPW89sd5QezHgjJXB3do1oGsUrdWudAHUV7VwfE8OzjrHq0lO5bxvg_UbVoPfdS7m00)

![Diagram](https://www.plantuml.com/plantuml/dpng/ZP9FYzj03CNl_XHYU-wXrnpAPdUzfR09WGdqhFKeZbXRuyx8IV_GxzxOeaFikg7a5FtUazv8la-AKVksAT8RIuSHMtZ5wgsEeHV_69eGuTq76dvNYYEAFqTM9G6D_JLAH_JXp5B30Piq8VIr9wa8VXO00EiOmza6V3coaXKh3V4XH4zn4Jq7qJdOOLIkk4DHSzuGBFbV-40lBBHipdHvAVC1jsGFuTjyHWQtVCuMHqzyOa_BwvcB_gVVfmllRdSpoJzw_IeA78u2Qz-o51tcBS3TMDgXK7C7c62zcs9NaM3ai471ckAeSPkPXjk-GUKWZbHPwcGojzpAu9IL9n8TGJa5MpfRj-sqlezS_ycpBuhn5V3-uoN_2bv2pLAiT-F_0QpWYLFNu7Vmc8wl0QEVMHuZeH88dI5Pp60Dm6rMy5bO6Hl-GPbclobAKOePWYT5RbBXDbSP7eCSEBOPJZeOhVj8a6o94u5RWIC5vNOOezJzpGvDNsa_dW4YAitiQ--1XYqNpWsrylfPHinWq5vazPou7DZsic2MDz0mh2iLMpFavpKNQ4hdSjKQBKHIkwE5WlrrgCpCPDXY6OavsDuov60shJJFDDb-bYnF6IFOBHoU5ivWx9d5qbMHncNRaS7bZoX_8iuyUTJSijvbb4tBdsrbAZFVa_Y-RNu3)

## Features

- Create and manage companies with detailed backstories and stock information.
- Simulate stock market events and scenarios.
- Manage teams and user profiles with financial details.
- Admin dashboard to control simulation parameters and monitor progress.
- Secure access and operations restricted to superadmins.

## Requirements

- Python 3.10
- Node.js and npm
- Django 3.2
- React 18.3.1
- Vite 2.9.9

## Installation

### Backend (Django)

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Apply Migrations**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a Superuser**:

    ```bash
    python manage.py createsuperuser
    ```

4. **Run the Server**:

    ```bash
    daphne simulateur.asgi:application
    ```

## Usage

### Superadmin Commands

To create a superadmin, use the Django management command:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the superadmin credentials.

### Running the Project

1. **Start the Django Server**:

    ```bash
    python manage.py runserver
    ```

2. **Start the Vite Development Server**:

    ```bash
    npm run dev
    ```

### Running the Daphne Server for ASGI

To run the Daphne server with the ASGI application, use the following command:

```bash
daphne -p 8000 simulateur.asgi:application
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License

## Data

The project includes the following CSV files for initial data setup:

```plaintext
.
├── data
│   ├── companies.csv
│   ├── cryptocurrencies.csv
│   ├── custom_stats.csv
│   ├── events.csv
│   ├── portfolios.csv
│   ├── scenarios.csv
│   ├── simulation_settings.csv
│   ├── stocks.csv
│   ├── teams.csv
│   ├── transaction_history.csv
│   ├── triggers.csv
│   └── users.csv
```

## File Structure

Here is a brief overview of the project file structure:

```plaintext
.
├── Dockerfile
├── data
├── db.sqlite3
├── docker-compose.yml
├── manage.py
├── package-lock.json
├── package.json
├── requirements.txt
├── simulateur
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── simulation
│   ├── admin.py
│   ├── apps.py
│   ├── channels
│   │   ├── consumers.py
│   │   └── routing.py
│   ├── decorators.py
│   ├── logic
│   │   ├── event_handlers.py
│   │   ├── price_update.py
│   │   ├── queue.py
│   │   ├── simulation_manager.py
│   │   ├── transactions.py
│   │   └── utils.py
│   ├── management
│   │   ├── commands
│   │   │   ├── clean_database.py
│   │   │   ├── seed_database.py
│   │   │   ├── start_simulation.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   └── simulation
│   │       ├── admin_dashboard.html
│   │       ├── buy_sell.html
│   │       ├── graph.html
│   │       ├── home.html
│   │       ├── market_overview.html
│   │       ├── team_dashboard.html
│   │       └── user_dashboard.html
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── auth_views.py
│       ├── company_views.py
│       ├── dashboard_views.py
│       ├── event_views.py
│       ├── portfolio_views.py
│       ├── scenario_views.py
│       ├── simulation_graph_views.py
│       └── simulation_views.py
├── staticfiles
└── staticfiles.json
```

## Run the Complete System

To run the complete system, you can use Docker Compose for setting up the entire environment with one command:

```bash
docker-compose up --build
```

This command will build and start the Django and Vite servers along with any other required services defined in the `docker-compose.yml` file.
