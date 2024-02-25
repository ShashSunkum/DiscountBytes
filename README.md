# DiscountBytes

## Overview

Welcome to **DiscountBytes**, an advanced web application tailored for restaurants to dynamically adjust their menu pricing based on real-time customer traffic. By harnessing the power of facial recognition technology, our platform not only optimizes pricing strategies but also streamlines staff allocation and enhances security measures for staff authentication. Founded by Aritra, Shash, Sahil and Sam at HackBeanPot 2024!

## Key Features

- **Dynamic Food Pricing**: Leverages live customer count to adjust menu prices, ensuring optimal competitiveness and profitability.
- **Efficient Staff Allocation**: Uses real-time data to recommend staff deployment, improving service quality during peak times.
- **Facial Recognition for Staff**: Facilitates swift staff check-ins and enhances security through facial recognition technology.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8 or later
- Flask
- Pandas
- SQLite3

### Installation

Follow these steps to set up the project environment:

1. Clone the project repository:

    ```bash
    git clone https://github.com/yourusername/dynamicdine.git
    cd dynamicdine
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure the application environment variables for development:

    ```bash
    export FLASK_APP=web_app.py
    export FLASK_ENV=development
    ```    

### Running the Application

To launch the web application, execute:

1. To run the web server:
    ```bash
    flask run
    ```

2. Go to the following link for local hosting on web browser to access application:
    ```hyperlink
    http://127.0.0.1:5000/
    ```

## Usage Instructions

1. **Login Page**: Presents unique login ID for registered restaurants, data stored in SQLite database, and checks if credentials match.
2. **Feature Option**: Shows 3 options for adding items and tracking dynamic prices of food items or clocking-in employees by facial recogintion and finally the number of staff predictor from past data of restaurant traffic and number of staff members.
3. **Function Specifc Site**: Respective web pages for each of these functionalities, and their outputs.  

## Contributing

We encourage contributions to **DiscountBytes**! If you have suggestions or encounter issues, feel free to fork the repository, apply your changes, and submit a pull request.

## License

**Dynamic Dine** is licensed under the [MIT License](LICENSE).

## Contact Information

For questions or additional support, please contact us.

