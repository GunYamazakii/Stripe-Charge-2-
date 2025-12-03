# Telegram Login & Diwas 3D

A retro-futuristic landing page featuring Telegram login authentication and a striking 3D CSS text animation displaying "Diwas". The design embraces a system failure aesthetic with scanlines, chromatic aberration effects, and terminal-style UI elements.

## Features

- **Telegram Login Widget**: Seamless integration with Telegram's authentication using Gate_ScannerBot
- **3D CSS Animation**: Rotating "Diwas" text with depth, perspective, and neon glow effects
- **Chromatic Aberration**: Cyan and magenta color split effects on text elements
- **Retro-Futuristic Design**: Deep black background with scanline overlays and digital noise
- **Session Management**: Login state persistence using localStorage and Manus OAuth
- **Post-Login Dashboard**: Animated welcome screen with user information display
- **Responsive Design**: Fully responsive layout for desktop, tablet, and mobile devices
- **Terminal UI**: Monospace typography with technical error codes and geometric brackets

## Tech Stack

- **Frontend**: React 19, Tailwind CSS 4, Framer Motion
- **Backend**: Express 4, tRPC 11, Drizzle ORM
- **Database**: MySQL/TiDB
- **Authentication**: Telegram Widget + Manus OAuth
- **Styling**: Custom CSS animations, chromatic aberration effects

## Installation & Setup

### Prerequisites

- Node.js 22.13.0+
- pnpm 10.4.1+
- MySQL/TiDB database connection

### Local Development

1. **Install dependencies**:
   ```bash
   cd telegram-login-diwas
   pnpm install
   ```

2. **Set up environment variables**:
   Create a `.env` file with:
   ```
   DATABASE_URL=your_database_connection_string
   JWT_SECRET=your_jwt_secret
   VITE_APP_ID=your_manus_app_id
   OAUTH_SERVER_URL=https://api.manus.im
   VITE_OAUTH_PORTAL_URL=your_oauth_portal_url
   ```

3. **Push database schema**:
   ```bash
   pnpm db:push
   ```

4. **Start development server**:
   ```bash
   pnpm dev
   ```

   The app will be available at `http://localhost:3000`

## Project Structure

```
telegram-login-diwas/
├── client/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Home.tsx          # Main landing page with login
│   │   ├── App.tsx               # Route configuration
│   │   ├── index.css             # Global styles with animations
│   │   └── main.tsx              # React entry point
│   ├── index.html                # HTML template
│   └── public/                   # Static assets
├── server/
│   ├── routers.ts                # tRPC procedure definitions
│   ├── db.ts                     # Database queries
│   └── _core/                    # Framework internals
├── drizzle/
│   └── schema.ts                 # Database schema
├── shared/                       # Shared types and constants
└── package.json                  # Dependencies
```

## Key Features Explained

### 3D Diwas Animation

The `.diwas-3d` class applies a continuous 3D rotation animation with perspective effects:

```css
@keyframes diwas-rotate {
  0% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
  25% { transform: rotateX(15deg) rotateY(20deg) rotateZ(5deg); }
  50% { transform: rotateX(0deg) rotateY(45deg) rotateZ(0deg); }
  75% { transform: rotateX(-15deg) rotateY(20deg) rotateZ(-5deg); }
  100% { transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }
}
```

### Chromatic Aberration

The `.chromatic-text` class creates a split cyan/magenta effect using clip-path and animation:

```css
.chromatic-text::before {
  animation: chromatic-shift-cyan 0.15s infinite;
  color: #00ffff;
  clip-path: polygon(0 0, 49% 0, 49% 100%, 0 100%);
}

.chromatic-text::after {
  animation: chromatic-shift-magenta 0.15s infinite;
  color: #ff00ff;
  clip-path: polygon(51% 0, 100% 0, 100% 100%, 51% 100%);
}
```

### Scanline Overlay

A fixed overlay creates authentic CRT monitor scanlines:

```css
body::before {
  background-image: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.15) 0px,
    rgba(0, 0, 0, 0.15) 1px,
    transparent 1px,
    transparent 2px
  );
}
```

## Telegram Login Integration

The Telegram login widget is configured with:
- **Bot Username**: Gate_ScannerBot
- **Size**: Large
- **Access**: Write permission requested
- **Callback**: `onTelegramAuth(user)` function

User data is stored in localStorage for session persistence.

## Deployment to Render

### Steps:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add telegram-login-diwas project"
   git push origin main
   ```

2. **Create Render Service**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `telegram-login-diwas` directory as the root directory
   - Set build command: `pnpm install && pnpm build`
   - Set start command: `pnpm start`

3. **Configure Environment Variables**:
   Add all required `.env` variables in Render's environment settings

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

## Build & Production

### Build for production:
```bash
pnpm build
```

### Start production server:
```bash
pnpm start
```

## Testing

Run tests with:
```bash
pnpm test
```

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Considerations

- Scanline and noise overlays use CSS, not images, for minimal file size
- 3D animations use GPU acceleration via `transform` properties
- Lazy loading for Telegram widget script
- Optimized font loading with Google Fonts

## Customization

### Change Colors

Edit CSS variables in `client/src/index.css`:

```css
:root {
  --accent: oklch(1 0.3 180);  /* Cyan */
  --destructive: oklch(0.6 0.3 30);  /* Red */
}
```

### Modify Animation Speed

Adjust animation duration in keyframes:

```css
.diwas-3d {
  animation: diwas-rotate 8s infinite linear;  /* Change 8s to desired duration */
}
```

### Customize Telegram Bot

Replace `Gate_ScannerBot` with your own bot username in `Home.tsx`:

```tsx
data-telegram-login="YOUR_BOT_USERNAME"
```

## Troubleshooting

**Telegram widget not showing?**
- Verify bot username is correct
- Check browser console for script loading errors
- Ensure domain is whitelisted in Telegram bot settings

**3D animation not smooth?**
- Check browser hardware acceleration is enabled
- Reduce animation complexity for lower-end devices
- Use `will-change: transform` for performance

**Session not persisting?**
- Verify localStorage is enabled in browser
- Check browser privacy settings
- Clear browser cache and try again

## License

MIT

## Support

For issues or questions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ using React, Tailwind CSS, and retro-futuristic vibes**
