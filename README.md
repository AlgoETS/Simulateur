# Simulateur

![Django](https://img.shields.io/badge/Django-4.2.13-blue)
![Python](https://img.shields.io/badge/Python-3.12-blue)

## Project Overview

Simulateur is a stock market simulation platform built using Django. The platform allows users to create and manage scenarios to simulate stock market events and track their outcomes. 
It includes an admin interface to manage the simulation settings and control the flow of the simulation.



![Diagram](https://www.plantuml.com/plantuml/dpng/ZPF1JW8n48Rl-nGJxhm3oabZ8h5mDkCoMHgxBMcd6j_URTawsoq7JvJl_oQPC3-xmEWvZgR3dfs7Ko0_Fn_EexRp-zKFQ7NAkXYenq2mIIgyk47R3M20q_uzaGn4UdRQmf5mB4u2wRieZ_475Bl-CnHd8ZSWaY9ZLbP2ioPUNhhUAgFLMdjFo0Ig9ujUkwBUSA4B_O9sc7HYrdO8HR_XGfUwSzFdKO_aGJ5TuSao-IyqCfcCBAHSHW_nm-XmQJQRURkQIlS3fSTeaBMpPI1pmTt_9yGyuFIyOsPUcOhTzOwOSErTtFV2WpSAqR2ST8gdTAPTbokstTRT4YXb4YRb4LXt9VTXvj8DmMqF96fkBb5xLCcQ-rLPSwg_VzjAM0ToY7R2NHlU_i0xikSucby0)

![Diagram](https://www.plantuml.com/plantuml/dpng/ZLJBRjim4BppAmYVOWW9qgjEATe6BOgc0QoU1PfQEOJv4CXb0hVeltTfsHJLo80lfYNkpimEXte8A3n6erdOApi8BmoNMeJm4T6hRKJu9ftTgD_0xnaxxl1FpWp27lWVLbbXeEORAhKxLcs5t0Tq_f1V_JtrqBEJ-zGXn-QQFpeFQcU_m-7c1BXc5Igv1pyX3bv9e5hj1BAAaB2DGoSGkff_fgLH1YQI1eHvhyg0sO8FDVz178rBluyAT7VpAu1_zgvN6jOJIF4sOSMGzFoqq3ZwcHhNQLmjR24FYNusLz9J86-KYLgW8Zy1aRI5H80qWcy3mb3pfvYaighNKM8ybhPUu4G1hs2nvbzeIOHUxNP9NZF-AQWaME6LU-z61q5wDIJenOFBTQhlbOmQ3wqcLbtiH7zKbkLcrcVdiNTwf7LlTj6vRAxpV3Ie2YaS2mTq34rXOEE53K8cyg_gg3SH3MVMcVTPIqhLrDVYOIZS4CP5YzdUUTnIpfPYzWHlfvD3NM19Pn4i5k6DMwt22tJj76b-Z1btVBpon9GPQA1vBcQpNPH_3ijLH3bZ9NRnzbNek9pEfTYJ5a6qj7F-XAm-hFZjBL_TtzsjJj-8cbDo0YkJKbJHlnGQgXglDNSzos5F1GNUcQJcoaeTQRoBfGbpgIvJqx9mVOkEXTrokEpwzIsZZqN3eYUqvAXJxOi8B3_dAKk32y3BbGithUOUfFDTOAEk_phIfIYXp_EMPSLCfm05Da_7LJfY8Fm7i5qq-Xy0)

![Diagram](https://www.plantuml.com/plantuml/dpng/TP9BJiCm48RtFiMeArXmWInG9K2A40kBE0UOsXDgI3oH7nAzFOwJaYQ8xV-O-VmuXeW-fg4Ng2DxQ0DvCMR9QZkYYt2O5EcvipqT00EqSkihmg4OQgjBzh7Ztd8nTwKcilugHhERvj65Z6BPrJPaeiiyknPY0e67nmnGmHj_M7TtBrfPbEnKy6p3sEC5qfGp6CudHc-slQSpSo28cNdfgWfUsRfPKhyvTftrGr7XC_kRJUggaW4z9t4YNdSr5JI4Nf-XOmzXEgre_g8M0mn5j7rOst9gzwJZ4eWCftGHyhy1OygRC13mkCLOJx9B2hbGldoJJf7sTc5LTGNlfDaRYEkp25KlezKgWYyvCWjaTjlHOAJvDSRhNzXSexnYtzuXe3EGIjVSz8xaJ1hw7m00)

![Diagram](https://www.plantuml.com/plantuml/dpng/ZP9FYzj03CNl_XHYU-wXrnpAPdUzfR09WGdqhFKeZbXRuyx8IV_GxzxOeaFikg7a5FtUazv8la-AKVksAT8RIuSHMtZ5wgsEeHV_69eGuTq76dvNYYEAFqTM9G6D_JLAH_JXp5B30Piq8VIr9wa8VXO00EiOmza6V3coaXKh3V4XH4zn4Jq7qJdOOLIkk4DHSzuGBFbV-40lBBHipdHvAVC1jsGFuTjyHWQtVCuMHqzyOa_BwvcB_gVVfmllRdSpoJzw_IeA78u2Qz-o51tcBS3TMDgXK7C7c62zcs9NaM3ai471ckAeSPkPXjk-GUKWZbHPwcGojzpAu9IL9n8TGJa5MpfRj-sqlezS_ycpBuhn5V3-uoN_2bv2pLAiT-F_0QpWYLFNu7Vmc8wl0QEVMHuZeH88dI5Pp60Dm6rMy5bO6Hl-GPbclobAKOePWYT5RbBXDbSP7eCSEBOPJZeOhVj8a6o94u5RWIC5vNOOezJzpGvDNsa_dW4YAitiQ--1XYqNpWsrylfPHinWq5vazPou7DZsic2MDz0mh2iLMpFavpKNQ4hdSjKQBKHIkwE5WlrrgCpCPDXY6OavsDuov60shJJFDDb-bYnF6IFOBHoU5ivWx9d5qbMHncNRaS7bZoX_8iuyUTJSijvbb4tBdsrbAZFVa_Y-RNu3)

![image](https://github.com/user-attachments/assets/edcb1cc7-f5f1-4c5d-97b6-f8d52a06fd03)

![image](https://github.com/user-attachments/assets/0dac0d06-3d52-4c05-a7ef-b76295d47ab9)

![image](https://github.com/user-attachments/assets/db61c4af-c866-4263-a9d0-cead3a9cc710)

![image](https://github.com/user-attachments/assets/67864417-b77b-4070-bb10-92d545d542ed)

![image](https://github.com/user-attachments/assets/d3e94f65-5062-4c5c-a2ee-76c1fa611e05)

![image](https://github.com/user-attachments/assets/4459d78c-7007-4e9a-8d4c-d4c4ba0063ae)



## Features

- Create and manage companies with detailed backstories and stock information.
- Simulate stock market events and scenarios.
- Manage teams and user profiles with financial details.
- Admin dashboard to control simulation parameters and monitor progress.
- Secure access and operations restricted to superadmins.

## Requirements

- Python 3.10
- Django 4.2.13

## Installation

Use pycharm professional or community

![img.png](img.png)

### Backend (Django)

## Run the Complete System

To run the complete system, you can use Docker Compose for setting up the entire environment with one command:

```bash
docker compose --profile all down
docker compose --profile all up -d --build
```


1. **Install Dependencies**:

    ```bash
    cd simulateur
    python3 -m run.py --install
    ```

2. **Run the Server**:

    ```bash
    python3 -m run.py --start-simulation 1
    ```

## Usage

### Superadmin Commands

To create a superadmin, use the Django management command:

```bash
python3 manage.py createsuperadmin --username=admin --password=admin --email=admin@admin.com
```

Follow the prompts to set up the superadmin credentials.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License

## Data

The project includes the following CSV files for initial data setup:

```plaintext
.
├── data
│   ├── scenarios.csv
│   ├── simulation_settings.csv
│   ├── companies.csv
│   ├── events.csv
│   ├── triggers.csv
│   ├── portfolios.csv
│   ├── stocks.csv
│   ├── teams.csv
│   └── users.csv
```

## File Structure

Here is a brief overview of the project file structure:

```plaintext
.
├── Dockerfile
├── data
├── db.sqlite3 # db
├── docker-compose.yml
├── manage.py
├── requirements.txt # packages
├── simulateur
│   ├── asgi.py # websocket and http
│   ├── settings.py
│   ├── urls.py
├── simulation
│   ├── admin.py
│   ├── apps.py
│   ├── channels # websocket
│   ├── logic # simulation logic
│   ├── models.py
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views
```
