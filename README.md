# TOPSIS Backend API

A production-ready REST API service for performing TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) analysis on multi-criteria decision-making datasets. The service processes user-uploaded data, performs advanced analytical computations, and delivers results via email.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [API Documentation](#api-documentation)
7. [Usage Examples](#usage-examples)
8. [Input Format Specifications](#input-format-specifications)
9. [Email Delivery](#email-delivery)
10. [Deployment](#deployment)
11. [Contributing](#contributing)

---

## Overview

The TOPSIS Backend API is a FastAPI-based service designed to perform TOPSIS analysis on multi-criteria decision problems. It provides a RESTful interface for uploading datasets, specifying evaluation criteria, and receiving ranked alternatives with detailed scoring information. All results are automatically generated as CSV files and delivered to users via email.

**Key Use Case:** Organizations can use this API to objectively rank and compare alternatives (products, vendors, strategies) based on multiple weighted criteria.

---

## Features

- **TOPSIS Algorithm Implementation:** Full implementation of the TOPSIS methodology for multi-criteria decision analysis
- **CSV Processing:** Robust file upload with built-in validation and error handling
- **Flexible Weighting:** Support for custom weights assigned to each criterion
- **Impact Direction:** Ability to specify whether criteria should be maximized or minimized
- **Automatic Ranking:** Generates sorted results with similarity scores to ideal solutions
- **CSV Export:** Results are generated in CSV format for easy integration and further analysis
- **Asynchronous Email Delivery:** Non-blocking email transmission using SendGrid for enhanced performance
- **Cloud Deployment:** Production-ready deployment on Render with automatic scaling
- **API Documentation:** Interactive Swagger UI for API exploration and testing

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Web Framework** | FastAPI |
| **Data Processing** | Pandas, NumPy |
| **Email Service** | SendGrid |
| **Application Server** | Uvicorn |
| **Cloud Platform** | Render |

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application initialization
│   ├── api.py                  # Route handlers and endpoints
│   ├── services/
│   │   └── email_service.py    # Email sending logic using SendGrid
│   └── __init__.py
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SendGrid API key (for email functionality)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/AnshulKaushal27/topsis-backend]
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your SendGrid API key and other configurations
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

---

## API Documentation

### Endpoint: POST `/api/topsis/run`

**Description:** Executes TOPSIS analysis on uploaded CSV data and emails the results to the specified recipient.

**Request Method:** `POST`

**Request Headers:**
```
Content-Type: multipart/form-data
```

**Request Body Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File (CSV) | Yes | The input dataset in CSV format containing alternatives and criteria |
| `weights` | String | Yes | Comma-separated numeric weights for each criterion (e.g., `0.4,0.3,0.2,0.1`) |
| `impacts` | String | Yes | Comma-separated impact direction for each criterion (e.g., `+,+,-,+`) where `+` means maximize and `-` means minimize |
| `email` | String | Yes | Recipient email address where results will be sent |

**Response Status:** `200 OK`

**Response Body:**
```json
{
  "message": "TOPSIS analysis completed successfully",
  "status": "completed",
  "timestamp": "2025-02-03T10:30:45.123456"
}
```

**Error Responses:**

| Status Code | Scenario |
|------------|----------|
| `400` | Invalid file format, missing parameters, or mismatched weights/impacts count |
| `422` | Validation error in input data |
| `500` | Server error during analysis or email delivery |

---

## Usage Examples

### cURL Request

```bash
curl -X POST "https://topsis-backend-1o38.onrender.com/api/topsis/run" \
  -F "file=@data.csv" \
  -F "weights=0.4,0.3,0.2,0.1" \
  -F "impacts=+,+,-,+" \
  -F "email=user@example.com"
```

### Python Request (using requests library)

```python
import requests

url = "https://topsis-backend-1o38.onrender.com/api/topsis/run"

with open("data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "weights": "0.4,0.3,0.2,0.1",
        "impacts": "+,+,-,+",
        "email": "user@example.com"
    }
    
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

### JavaScript/Fetch Request

```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);
formData.append("weights", "0.4,0.3,0.2,0.1");
formData.append("impacts", "+,+,-,+");
formData.append("email", "user@example.com");

fetch("https://topsis-backend-1o38.onrender.com/api/topsis/run", {
  method: "POST",
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Input Format Specifications

### CSV File Requirements

**Structure:**
- **First Column:** Alternative names (non-numeric values)
- **Remaining Columns:** Numeric criteria values only
- **Header Row:** Required (first row contains column names)
- **Data Type:** All criteria values must be numeric

**Example Input (data.csv):**
```csv
Model,Storage,Camera,Price,Rating
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,64,20,400,5
M5,128,16,500,4
```

### Parameters Specification

**Weights:**
- Comma-separated numeric values (decimal or integer)
- Must match the number of criteria columns
- Typically normalized (sum to 1) but not strictly required
- Example: `0.4,0.3,0.2,0.1` or `4,3,2,1`

**Impacts:**
- Comma-separated `+` or `-` symbols
- `+` indicates criterion should be maximized
- `-` indicates criterion should be minimized
- Must match the number of criteria columns
- Example: `+,+,-,+` means Storage, Camera, Rating are to maximize; Price is to minimize

---

## Email Delivery

### SendGrid Integration

Results are delivered asynchronously using SendGrid's email service, ensuring non-blocking operation and reliable delivery.

**Email Contents:**
- Results CSV file as attachment
- Summary of analysis parameters
- TOPSIS scores and rankings for all alternatives

**Configuration:**

1. Obtain SendGrid API key from [sendgrid.com](https://sendgrid.com)
2. Set the `SENDGRID_API_KEY` environment variable
3. Optionally configure sender email via `SENDER_EMAIL` environment variable

**Delivery Assurance:**

- Emails are sent asynchronously to prevent blocking the main API response
- Delivery status can be tracked via SendGrid's Email Activity dashboard
- Actual inbox placement depends on recipient email provider's spam filters and authentication protocols (SPF, DKIM, DMARC)

**Troubleshooting Email Issues:**

- Verify SendGrid API key is correctly set
- Check email validity and domain reputation
- Review SendGrid bounce logs for permanent failures
- Implement sender authentication (SPF, DKIM) for improved deliverability

---

## Deployment

### Live Environment

**Backend API Base URL:** `https://topsis-backend-1o38.onrender.com`

**Interactive API Documentation:** `https://topsis-backend-1o38.onrender.com/docs`

**Alternative API Documentation:** `https://topsis-backend-1o38.onrender.com/redoc`

### Deployment Platform: Render

The application is deployed on Render, a modern cloud platform offering:

- **Automatic Scaling:** Handles traffic spikes seamlessly
- **Zero Downtime Deployments:** Updates without service interruption
- **Environment Management:** Secure handling of API keys and secrets
- **Built-in Monitoring:** Performance tracking and error alerting
- **SSL/TLS Encryption:** Automatic HTTPS for all endpoints

### Deploying to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service pointing to the `backend` directory
3. Set environment variables (SENDGRID_API_KEY, etc.)
4. Configure the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy and monitor from Render dashboard

---

## Contributing

We welcome contributions to improve the TOPSIS Backend API. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Submit a pull request with detailed description

**Guidelines:**
- Follow PEP 8 style conventions
- Include docstrings for new functions
- Add tests for new features
- Update documentation accordingly

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support & Contact

For questions, issues, or feature requests, please open an issue on the GitHub repository or contact the development team.

**Useful Links:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Render Deployment Guide](https://render.com/docs)
- [TOPSIS Method Overview](https://en.wikipedia.org/wiki/TOPSIS)

---

**Last Updated:** February 2025
