# Take-Home Project

## 🌟 Features

- **Quote Management**: Create, read, and list quotes with persistent storage
- **AI Integration**: Generate inspirational quotes using OpenRouter AI models
- **RESTful Design**: Clean, consistent API endpoints with proper HTTP status codes
- **Auto Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Production Ready**: CORS support, error handling, and structured logging
- **Async Support**: Built with async/await for high performance

### Installation

1. **Clone or download this project**
   ```bash
   # If you have the project files, navigate to the directory
   cd quotecrafter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with the following content:
   ```env
   # OpenRouter API Key (required for AI quote generation)
   OPENROUTER_API_KEY=your_openrouter_api_key_here

4. **Get your OpenRouter API Key (Optional)**
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Add it to your `.env` file

   > **Note**: The API works without an OpenRouter key, but AI quote generation will be disabled.

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at: `http://127.0.0.1:8000`

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔗 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `GET` | `/` | Welcome message | 200 |
| `GET` | `/health` | Health check | 200 |
| `GET` | `/quotes/health` | Quotes service health | 200 |

### Quote Management

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `POST` | `/quotes/` | Create a new quote | 201 |
| `GET` | `/quotes/` | List all quotes | 200 |
| `GET` | `/quotes/{id}` | Get quote by ID | 200/404 |
| `POST` | `/quotes/generate` | Generate AI quote | 201 |

## 💡 Usage Examples

### 1. Create a Quote

```bash
curl -X POST "http://127.0.0.1:8000/quotes/" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "Albert Einstein",
    "content": "Imagination is more important than knowledge."
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "author": "Albert Einstein",
    "content": "Imagination is more important than knowledge.",
    "created_at": "2024-01-15T10:30:00.123456"
  },
  "message": "Quote created successfully"
}
```

### 2. Get All Quotes

```bash
curl -X GET "http://127.0.0.1:8000/quotes/"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "author": "Albert Einstein",
      "content": "Imagination is more important than knowledge.",
      "created_at": "2024-01-15T10:30:00.123456"
    }
  ],
  "message": "Quotes retrieved successfully",
  "count": 1
}
```

### 3. Get Quote by ID

```bash
curl -X GET "http://127.0.0.1:8000/quotes/1"
```

### 4. Generate AI Quote (Requires OpenRouter API Key)

```bash
curl -X POST "http://127.0.0.1:8000/quotes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "perseverance"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "author": "Anonymous",
    "content": "Perseverance is not a long race; it is many short races one after the other.",
    "created_at": "2024-01-15T10:35:00.123456"
  },
  "message": "Quote generated successfully for topic 'perseverance'"
}
```

## 🏗️ Project Structure

```
quotecrafter/
├── main.py                 # FastAPI app entry point
├── routers/
│   └── quotes.py          # Quote-related endpoints
├── schemas/
│   └── quote.py           # Pydantic models
├── services/
│   └── ai_service.py      # OpenRouter integration
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | None | OpenRouter API key for AI generation |
| `API_HOST` | `127.0.0.1` | Server host address |
| `API_PORT` | `8000` | Server port |
| `DEBUG` | `False` | Enable debug mode |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:8080` | Allowed CORS origins |

## 🚨 Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Quote not found
- **429 Too Many Requests**: Rate limit exceeded (AI generation)
- **500 Internal Server Error**: Server errors
- **502 Bad Gateway**: External API errors
- **503 Service Unavailable**: AI service not configured
- **504 Gateway Timeout**: Request timeout

## 📋 Known Limitations

1. **In-Memory Storage**: Quotes are stored in memory and will be lost when the server restarts
2. **Single Instance**: No database persistence or clustering support