# Before/After Image Slider Setup

## How to Add Your Own Images

The before/after slider component currently uses placeholder backgrounds. Here's how to customize it:

### Option 1: Use Two Different Images

1. Save your "before" image (during construction) as:
   `review-analytics-dashboard/public/images/love-park-before.jpg`

2. Save your "after" image (post-renovation) as:
   `review-analytics-dashboard/public/images/love-park-after.jpg`

The component will automatically use these images if they exist!

### Option 2: Use Your Existing Love Park Image

Currently, the "after" side uses: `/images/love-park.jpg.png`

If you want to use a different image for the "before" side:
- Save it as `/images/love-park-during-construction.jpg`

### What Makes Good Before/After Images:

✅ **DO:**
- Use images from the same angle/perspective
- Ensure both images are the same aspect ratio
- Use high-resolution images (at least 1920x1080)
- Show clear visual difference (construction equipment vs. finished park)

❌ **DON'T:**
- Mix portrait and landscape orientations
- Use images from completely different viewpoints
- Use low-resolution or blurry images

### Current Setup:

**BEFORE (left side):** Gray placeholder with "DURING CONSTRUCTION" text
**AFTER (right side):** Your Love Park image with overlay

### To Fully Customize:

Edit the file: `src/components/BeforeAfterComparison.tsx`

Lines to update:
- Line ~80: Before image background
- Line ~95: After image background

### Recommended Image Sources:

1. Google Images (with usage rights filter)
2. Philadelphia city archives
3. Love Park historical photos
4. TripAdvisor review photos from the respective time periods
