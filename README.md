﻿# book-address

A fastAPI project demonstrating CRUD operations with a simplle address booking API

## Table of Content

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/PavankumarPattar/address-api.git
    cd address-api
    ```
  <!-- You will get code in master branch  -->

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

## Usage

Once the application is running, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to access the FastAPI interactive documentation. You can test and interact with the API endpoints using this Swagger UI.

## API Endpoints

- **Create Addressess:**
  - **URL:** `/addresses/`
  - **Method:** `POST`
  - **Request Body:**
    ```json
    {
        "name": "Address Name",
        "latitude": "float num",
        "longitude": "float num"
    }

- **Read All The Addressess :**
  - **URL:** `/addresses/get-list`
  - **Method:** `GET`    ```

- **Read Addresses Within The Distance :**
  - **URL:** `/addresses/`
  - **Method:** `GET`
  - **Request Format:**
    ```
        "latitude":"Enter Latitude in float"
        "longitude":"Enter Longitude in float"
        "distance": "float num"
    ```

- **Update Adreess:**
  - **URL:** `/addresses/{address_id}/`
  - **Method:** `PUT`
  - **Request Body:**
    ```json
    {
        "address": "Updated Address Name",
        "latitude": "Updated float number",
        "longitude": "Updated float number"
    }
    ```

- **Delete Address:**
  - **URL:** `/addresses/{address_id}/`
  - **Method:** `DELETE`
