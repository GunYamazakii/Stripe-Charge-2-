# Deployment Guide: Telegram Login & Diwas 3D

This guide provides step-by-step instructions for deploying the Telegram Login & Diwas 3D project to Render.

## Prerequisites

- GitHub account with the repository pushed
- Render account (free tier available at https://render.com)
- Database connection string (MySQL/TiDB)
- Environment variables from your Manus dashboard

## Step 1: Prepare Your Repository

Ensure all files are committed and pushed to GitHub:

```bash
cd telegram-login-diwas
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Create a Render Account

1. Visit https://render.com
2. Sign up with GitHub (recommended for automatic deployments)
3. Authorize Render to access your GitHub repositories

## Step 3: Create a New Web Service

1. Click the **"New +"** button in the Render dashboard
2. Select **"Web Service"**
3. Choose **"Connect a repository"**
4. Select your `Stripe-Charge-2-` repository
5. Click **"Connect"**

## Step 4: Configure the Web Service

### Basic Settings

- **Name**: `telegram-login-diwas` (or your preferred name)
- **Environment**: `Node`
- **Region**: Choose the region closest to your users
- **Branch**: `main`
- **Root Directory**: `telegram-login-diwas`

### Build & Start Commands

- **Build Command**: `pnpm install && pnpm build`
- **Start Command**: `pnpm start`

### Instance Type

- **Free Tier**: Suitable for development/testing
- **Paid Tier**: Recommended for production (auto-scaling, custom domains)

## Step 5: Add Environment Variables

In the Render dashboard, scroll to **"Environment"** and add the following variables:

```
DATABASE_URL=your_mysql_connection_string
JWT_SECRET=your_jwt_secret_key
VITE_APP_ID=your_manus_app_id
OAUTH_SERVER_URL=https://api.manus.im
VITE_OAUTH_PORTAL_URL=your_oauth_portal_url
OWNER_OPEN_ID=your_owner_open_id
OWNER_NAME=your_name
VITE_ANALYTICS_ENDPOINT=your_analytics_endpoint
VITE_ANALYTICS_WEBSITE_ID=your_website_id
VITE_APP_TITLE=Telegram Login & Diwas 3D
VITE_APP_LOGO=your_logo_url
```

### Getting Your Environment Variables

1. **From Manus Dashboard**:
   - Log in to your Manus account
   - Navigate to your project settings
   - Copy the provided environment variables

2. **Database Connection**:
   - Use your MySQL/TiDB connection string
   - Format: `mysql://user:password@host:port/database`

3. **JWT Secret**:
   - Generate a secure random string (minimum 32 characters)
   - Example: Use `openssl rand -base64 32`

## Step 6: Deploy

1. Click the **"Create Web Service"** button
2. Render will automatically start the build process
3. Monitor the build logs in the **"Logs"** tab
4. Once deployment is complete, you'll receive a public URL

## Step 7: Verify Deployment

1. Visit your Render URL (e.g., `https://telegram-login-diwas.onrender.com`)
2. Test the Telegram login widget
3. Verify the 3D Diwas animation loads correctly
4. Check that the scanline effects are visible

## Step 8: Custom Domain (Optional)

To use a custom domain:

1. In Render dashboard, go to your service
2. Click **"Settings"** → **"Custom Domain"**
3. Enter your domain name
4. Follow DNS configuration instructions
5. Wait for SSL certificate to be issued (usually 5-10 minutes)

## Troubleshooting

### Build Fails

**Error: `pnpm: command not found`**
- Solution: Render should have pnpm pre-installed. Check Node version is 18+
- Try: Update `package.json` to specify Node version in `engines` field

**Error: Database connection failed**
- Solution: Verify DATABASE_URL is correct and accessible from Render
- Check: Database firewall allows connections from Render's IP ranges

**Error: Missing environment variables**
- Solution: Ensure all required variables are set in Render dashboard
- Check: Variable names match exactly (case-sensitive)

### Deployment Issues

**App crashes after deployment**
- Check logs: Click "Logs" tab in Render dashboard
- Common causes: Missing env vars, database connection, port binding
- Solution: Verify all environment variables are set correctly

**Telegram widget not working**
- Check: Bot username is correct (Gate_ScannerBot)
- Verify: Domain is whitelisted in Telegram bot settings
- Solution: Update bot settings to allow your Render domain

**Animations not smooth**
- Check: Browser hardware acceleration is enabled
- Solution: This is usually a client-side issue, not deployment-related

### Performance Issues

**Slow initial load**
- Solution: Enable auto-scaling on paid tier
- Check: Database query performance
- Optimize: Reduce animation complexity if needed

**High memory usage**
- Solution: Upgrade to a larger instance type
- Check: Memory leaks in React components
- Optimize: Implement proper cleanup in useEffect hooks

## Auto-Deployment from GitHub

Render automatically redeploys when you push to your GitHub repository:

1. Make changes locally
2. Commit and push to GitHub: `git push origin main`
3. Render automatically triggers a new build
4. Monitor deployment in Render dashboard

To disable auto-deployment:
- Go to service settings
- Disable "Auto-Deploy"

## Monitoring & Logs

### View Logs

1. Go to your Render service dashboard
2. Click the **"Logs"** tab
3. View real-time application logs

### Monitor Metrics

1. Click the **"Metrics"** tab
2. View CPU, memory, and request statistics
3. Set up alerts for performance issues

## Scaling

### Free Tier Limitations

- Auto-pauses after 15 minutes of inactivity
- Limited to 0.5 CPU cores
- 512 MB RAM
- Suitable for development/testing

### Paid Tier Benefits

- Always-on service
- Auto-scaling based on load
- Custom domains with SSL
- Priority support
- Upgrade anytime: Go to service settings → "Plan"

## Maintenance

### Regular Updates

1. Keep dependencies updated: `pnpm update`
2. Test locally before pushing
3. Monitor Render logs for errors
4. Update environment variables as needed

### Backup Database

- Ensure your database has regular backups
- Test restore procedures periodically
- Keep backup credentials secure

## Support

- **Render Docs**: https://render.com/docs
- **GitHub Issues**: Report bugs in your repository
- **Community**: Render community forums

---

**Happy deploying! Your Telegram Login & Diwas 3D app is now live on Render.**
