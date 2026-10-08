# Banking AI – Frontend

React + Vite (JavaScript) dashboard for the Multi-Agent Banking MVP. It sends
natural-language banking questions to the FastAPI backend and shows both the
answer and the multi-agent execution trace.

All banking data is **simulated** by the backend. The frontend holds no API keys
and performs no real banking or payment operations.

## Features

- Chat interface with 5 suggested prompts: balance, recent transactions,
  suspicious transaction, loan eligibility, EMI calculation
- Formatted results for each intent (with a "Show raw JSON" toggle)
- Agent trace panel: Gemini intent + confidence → Supervisor Agent → selected
  specialised agent → tool/result
- Loading, backend-offline and error states; live backend health indicator
- Responsive layout, light/dark following the system theme

## Prerequisites

- Node.js 20+
- The backend running at `http://127.0.0.1:8000`

## Run

Start the backend from the project root (with the virtual environment active):

```bash
uvicorn backend.app.main:app --reload
```

Then start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

Other scripts: `npm run lint`, `npm run build`, `npm run preview`.

## API proxy

`vite.config.js` proxies `/api` and `/health` to `http://127.0.0.1:8000`, so the
backend needs no CORS configuration. The proxy applies to the dev server only.

## Demo context

Requests always include fixed simulated IDs (see `src/data/demoContext.js`):

| Field          | Value    |
| -------------- | -------- |
| `customer_id`  | CUST001  |
| `account_id`   | ACC001   |
| `transaction_id` | TXN1005 |

Loan amount, EMI principal, interest rate (`8.5%`) and tenure (`5 years`) default
to demo values and are read from the message when present, e.g.
"Calculate EMI for 800000 at 9% for 3 years".

## Structure

```
src/
  App.jsx                  state, request handling, layout
  api/bankingApi.js        POST /api/chat, /health check
  data/                    demo IDs and suggested prompts
  components/
    Header, DemoContextBar, ChatPanel, MessageBubble, SuggestedPrompts,
    ResultView, TracePanel, TraceStep
  styles/app.css           component styles (tokens live in index.css)
```
