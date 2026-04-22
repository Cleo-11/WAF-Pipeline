# Frontend (Next.js)

## Run locally

1. Install dependencies:
   ```bash
   npm install
   ```
2. Set API base URL (optional if backend runs on `http://localhost:5000`):
   ```powershell
   Copy-Item .env.example .env.local
   ```
   Then edit `.env.local` if needed:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
   ```
3. Start development server:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:3000`.

## Notes

- This frontend only consumes backend APIs and does not include authentication.
- Ensure your Flask backend is running separately on port `5000` (or update `NEXT_PUBLIC_API_BASE_URL`).
