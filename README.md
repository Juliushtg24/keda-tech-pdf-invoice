# Invoice PDF Generator Microservice

A cloud-native microservice that generates professional PDF invoices for Guide Booker booking confirmations. Built with FastAPI and deployed on AWS Lambda using container images.

---

## 📋 Context & Scenario

Booking confirmation emails are critical. For Guide Booker, we need a microservice dedicated solely to generating professional PDF invoices for customers after they pay.

**The Task:** Create a standalone API endpoint that accepts JSON booking data and returns a downloadable PDF invoice.

**The Constraint:** Using specific cloud-native technologies to keep costs low and scalability high.

---

## 🛠️ Tech Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| Python 3.9+ | Runtime               |
| FastAPI     | Web Framework         |
| Mangum      | AWS Lambda Adapter    |
| ReportLab   | PDF Generation        |
| Docker      | Containerization      |
| AWS Lambda  | Serverless Deployment |
| AWS ECR     | Container Registry    |

---

## 📁 Project Structure

```
keda-tech/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & Lambda handler
│   ├── models.py        # Pydantic request models
│   └── pdf.py           # PDF generation logic
├── Dockerfile           # Lambda container configuration
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker Desktop
- AWS CLI (for deployment)
- Git

### Local Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/keda-tech-invoice.git
   cd keda-tech-invoice
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server locally**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

## 📡 API Endpoints

### Health Check

```
GET /
```

**Response:**

```json
{
  "status": "ok",
  "message": "Invoice API is running"
}
```

---

### Generate Invoice (Download)

```
POST /generate-invoice
```

Generates and downloads a PDF invoice.

**Request Body:**

```json
{
  "customer_name": "Julius Martin",
  "guide_name": "Budi Rudianto",
  "date": "2026-04-05",
  "price": 100000000,
  "currency": "IDR"
}
```

**Response:** PDF file download (`invoice.pdf`)

---

### Preview Invoice (View in Browser)

```
POST /preview-invoice
```

Generates and displays the PDF invoice inline in the browser.

**Request Body:** Same as `/generate-invoice`

**Response:** PDF displayed in browser

---

## 🧪 Testing

### Using cURL

**Health Check:**

```bash
curl http://localhost:8000/
```

**Generate Invoice:**

```bash
curl -X POST http://localhost:8000/generate-invoice \
  -H "Content-Type: application/json" \
  -d "{\"customer_name\": \"Julius Martin\", \"guide_name\": \"Bali Explorer\", \"date\": \"2026-04-05\", \"price\": 150, \"currency\": \"IDR\"}" \
  --output invoice.pdf
```

### Using Postman

1. Create a new **POST** request
2. URL: `http://localhost:8000/generate-invoice`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "customer_name": "Julius Martin",
     "guide_name": "Bali Explorer",
     "date": "2026-04-05",
     "price": 100000000,
     "currency": "IDR"
   }
   ```
5. Click **Send** and save the response as PDF

### Using FastAPI Docs

Navigate to `http://localhost:8000/docs` for interactive Swagger API documentation.

---

## 🐳 Docker

### Build Docker Image

```bash
docker build -t invoice-service .
```

### Run Container Locally (Lambda Runtime)

```bash
docker run -p 9000:8080 invoice-service
```

### Test Lambda Container Locally

```bash
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "2.0",
    "requestContext": {
      "http": {
        "method": "POST",
        "path": "/generate-invoice"
      }
    },
    "headers": {
      "content-type": "application/json"
    },
    "body": "{\"customer_name\": \"Julius Martin\", \"guide_name\": \"Bali Explorer\", \"date\": \"2026-04-05\", \"price\": 150, \"currency\": \"IDR\"}",
    "isBase64Encoded": false
  }'
```

---

## ☁️ AWS Deployment

### Step 1: Authenticate with ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 2: Create ECR Repository

```bash
aws ecr create-repository --repository-name invoice-service --region us-east-1
```

### Step 3: Tag and Push Image

```bash
docker tag invoice-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/invoice-service:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/invoice-service:latest
```

### Step 4: Create Lambda Function

1. Go to **AWS Lambda Console**
2. Click **Create function**
3. Select **Container image**
4. Enter function name: `invoice-service`
5. Browse and select your ECR image
6. Click **Create function**

### Step 5: Configure Function URL

1. Go to **Configuration** → **Function URL**
2. Click **Create function URL**
3. Auth type: **NONE** (for testing) or **AWS_IAM** (for production)
4. Click **Save**

---

## 🌐 Live Demo

The API is deployed and accessible at:

**Base URL:** `https://p5piwwphrvb5vkb4tgqci3mwfi0mrtuf.lambda-url.us-east-1.on.aws`

### Test Live Endpoints

**Health Check:**

```bash
curl https://p5piwwphrvb5vkb4tgqci3mwfi0mrtuf.lambda-url.us-east-1.on.aws/
```

**Generate Invoice:**

```bash
curl -X POST https://p5piwwphrvb5vkb4tgqci3mwfi0mrtuf.lambda-url.us-east-1.on.aws/generate-invoice \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Julius Martin", "guide_name": "Bali Explorer", "date": "2026-04-05", "price": 150, "currency": "IDR"}' \
  --output invoice.pdf
```

**Preview Invoice:**

```bash
curl -X POST https://p5piwwphrvb5vkb4tgqci3mwfi0mrtuf.lambda-url.us-east-1.on.aws/preview-invoice \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Julius Martin", "guide_name": "Bali Explorer", "date": "2026-04-05", "price": 150, "currency": "IDR"}' \
  --output invoice.pdf
```

---

## 📄 Sample Invoice Output

The generated PDF includes:

- **Header:** KEDA TECH branding with professional green/white theme
- **Invoice Details:** Auto-generated invoice number, date
- **Bill To:** Customer name
- **Service Table:** Description, guide name, amount with borders
- **Total Section:** Total amount with currency (white/black theme)
- **Footer:** Thank you message

---

## 📦 Dependencies

```
fastapi
mangum
uvicorn
reportlab
```

---

## 📝 License

This project was created as part of a technical assessment for **PT. Citra Kreasi Teknologi Indonesia (KEDA TECH)**.

---

## 🙏 Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Mangum - AWS Lambda Adapter](https://mangum.io/)
- [ReportLab PDF Library](https://www.reportlab.com/)
- [AWS Lambda Container Support](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
