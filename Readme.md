# Automation Tools Suite

A comprehensive Django-based automation platform featuring data management, email marketing, image processing, and stock analysis capabilities.

## Overview

This project provides a collection of powerful automation tools designed to streamline common business operations including data import/export, bulk email campaigns with tracking, image optimization, and financial market analysis.

## Features

### 1. **Import Data**

Import data from CSV files directly into your database with ease.

### 2. **Export Data**

Export database records to CSV format for backup or analysis purposes.

### 3. **Bulk Email Campaigns**

Send mass emails to multiple recipients simultaneously. Utilizes Celery for background task processing to handle large-scale email operations efficiently.

### 4. **Email Tracking**

Monitor email campaign performance with built-in tracking for:

- Open rates
- Click-through rates

### 5. **Image Compressor**

Optimize and compress images to reduce file sizes while maintaining quality.

### 6. **Stock Analysis**

Analyze stock market data for:

- NASDAQ stocks
- NSE (National Stock Exchange) stocks

## Technology Stack

- **Backend Framework:** Django
- **Task Queue:** Celery
- **Message Broker:** Redis
- **Email Service:** Brevo (formerly Sendinblue)
- **Tunneling:** Ngrok
- **Environment Manager:** UV
- **Configuration Management:** python-decouple

## Prerequisites

- Python 3.8+
- Redis Server
- UV (for virtual environment management)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/mayank698/AutonomIQ
cd automation_main
```

2. **Create and activate virtual environment using UV**

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
uv pip install -r requirements.txt
```

4. **Set up Redis**
   Ensure Redis is installed and running on your system:

```bash
redis-server
```

5. **Configure environment variables**
   Create a `.env` file in the project root and add the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
SENDINBLUE_API_KEY=your-brevo-api-key
```

6. **Run database migrations**

```bash
python manage.py migrate
```

7. **Create a superuser**

```bash
python manage.py createsuperuser
```

## Usage

### Starting the Application

1. **Start Django development server**

```bash
python manage.py runserver
```

2. **Start Celery worker** (in a separate terminal)

```bash
celery -A automation_main worker -l info --pool=solo
```

4. **Expose local server using Ngrok** (optional, for webhooks)

```bash
ngrok http 8000
```

## Environment Variables

| Variable              | Description                      | Required |
| --------------------- | -------------------------------- | -------- |
| `DJANGO_SECRET_KEY`   | Django secret key for security   | Yes      |
| `DEBUG`               | Enable/disable debug mode        | Yes      |
| `EMAIL_HOST`          | SMTP server hostname             | Yes      |
| `EMAIL_PORT`          | SMTP server port                 | Yes      |
| `EMAIL_HOST_USER`     | Email account username           | Yes      |
| `EMAIL_HOST_PASSWORD` | Email account password           | Yes      |
| `SENDINBLUE_API_KEY`  | Brevo API key for email services | Yes      |

## Project Structure

```
project/
├── manage.py
├── requirements.txt
├── .env
├── automation_main/
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
└── apps/
    ├── data_management/
    ├── email_campaigns/
    ├── image_processing/
    └── stock_analysis/
```

## Features in Detail

### Data Import/Export

- Support for CSV file format
- Bulk data operations
- Data validation and error handling

### Bulk Email System

- Asynchronous email sending using Celery
- Queue management with Redis
- Email template support
- Batch processing for large recipient lists

### Email Tracking

- Pixel-based open tracking
- Link click tracking
- Real-time analytics dashboard

### Image Compressor

- Multiple format support
- Configurable compression levels
- Batch processing capability

### Stock Analysis

- Real-time stock data retrieval
- Support for NASDAQ and NSE markets
- Technical analysis tools

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue in the repository.

## Acknowledgments

- Django community for the excellent framework
- Celery for robust task queue management
- Brevo for reliable email delivery services
