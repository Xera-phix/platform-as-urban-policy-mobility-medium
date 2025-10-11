# Review Analytics Dashboard

A beautiful, modern frontend for analyzing review data from Google Maps, Yelp, and TripAdvisor.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd review-analytics-dashboard
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Open your browser to `http://localhost:5173`

## 🎨 Features

✨ **Wow Factors:**
- Animated gradient hero with floating icons
- Smooth drag-and-drop file upload
- Dark mode toggle
- Beautiful transitions and animations
- Responsive design (mobile-friendly)
- Professional UI with Tailwind CSS

📊 **Functionality:**
- Upload JSON or CSV review files
- Select data source (Google Maps, Yelp, TripAdvisor)
- Beautiful loading states and error handling
- Ready to connect to backend API

## 🛠️ Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **react-dropzone** - File upload functionality

## 📁 Project Structure

```
src/
├── components/
│   ├── Hero.tsx              # Animated hero section
│   ├── FileUpload.tsx        # Drag-and-drop upload
│   ├── DataSourceSelector.tsx # Platform selector
│   ├── AnalyzeButton.tsx     # Action button
│   └── DarkModeToggle.tsx    # Dark/light mode toggle
├── App.tsx                   # Main app component
├── main.tsx                  # Entry point
└── index.css                 # Global styles
```

## 🎯 Next Steps

1. **Add Results Page** - Display generated charts
2. **Connect to Backend** - Integrate with Python FastAPI
3. **Add More Charts** - Display your matplotlib visualizations
4. **Deploy** - Push to Vercel for free hosting

## 📸 Screenshots

(Add screenshots after running the app!)

## 🚢 Deployment

Deploy to Vercel in one command:

```bash
npm run build
# Then connect your GitHub repo to Vercel
```

## 💡 Tips

- Press the **moon/sun icon** to toggle dark mode
- Try dragging files onto the upload area
- The app is fully responsive - try it on mobile!

## 🐛 Troubleshooting

If you see TypeScript errors, run:
```bash
npm install
```

If the dev server won't start:
```bash
rm -rf node_modules
npm install
npm run dev
```

---

Built with ❤️ using React, TypeScript, and Framer Motion
