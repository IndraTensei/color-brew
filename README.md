# color-brew

> *Brew beautiful color palettes from a single color -- right in your terminal.*

**color-brew** is a CLI tool that generates harmonious color palettes from any input color. Whether you're designing a website, picking colors for a presentation, or just exploring color theory, color-brew makes it instant and fun.

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Light%20%7C%20macOS%20%7C%20Windows-lightgrey)

---

## Features

- **9 Color Schemes** -- Complementary, Analogous, Triadic, Split-Complementary, Tetradic, Square, Monochromatic, Shades, and Tints
- **Multiple Input Formats** -- Hex (`#FF6B6B`), RGB (`rgb(255,107,107)`), HSL (`hsl(0,71,71)`), or named colors (`coral`, `steelblue`)
- **Beautiful Terminal Preview** -- Colored blocks with hex, RGB, and HSL values
- **Export Formats** -- CSS variables, SCSS, Tailwind config, JSON, SVG swatches, and PNG images
- **Gradient Generator** -- Smooth gradients between any two colors
- **WCAG Contrast Ratios** -- Check accessibility of color combinations
- **Clipboard Support** -- Copy hex values instantly
- **140+ Named Colors** -- Full CSS color name support
- **Zero Dependencies** -- Pure Python 3, no pip install needed (optional Pillow for PNG export)
- **Color Identity** -- Reverse-lookup any color to find its closest named CSS color, with CMYK output
- **Palette History** -- Auto-save and recall your previously generated palettes
- **Smooth Gradient Bar** -- Choose between block or smooth gradient terminal previews
- **Random Palettes** -- Generate palettes from random colors with mood presets (v1.4)
- **Seasonal Palettes** -- Curated palettes inspired by spring, summer, autumn, and winter (v1.4)
- **Palette Blending** -- Blend or interleave two palettes for hybrid color schemes (v1.4)
- **Favorites** -- Bookmark and recall your best palettes by name (v1.4)

---

## Installation

### Quick Start (No Install)

```bash
git clone https://github.com/IndraTensei/color-brew.git
cd color-brew
python3 colorbrew.py "#FF6B6B"
```

### Install to PATH

```bash
git clone https://github.com/IndraTensei/color-brew.git
cd color-brew
chmod +x color-brew
sudo ln -s "$(pwd)/color-brew" /usr/local/bin/color-brew
```

Now use it from anywhere:

```bash
color-brew "#FF6B6B"
```

### Optional: PNG Export

```bash
pip install Pillow
```

---

## Usage

### Basic Usage

```bash
# Generate an analogous palette from a hex color
color-brew "#FF6B6B"

# Use a named color
color-brew coral

# Specify a scheme
color-brew blue --scheme triadic

# Show all schemes at once
color-brew "#2C3E50" --all
```

### Color Input Formats

```bash
color-brew "#FF6B6B"          # Hex (6-digit)
color-brew "#F00"             # Hex (3-digit shorthand)
color-brew "FF6B6B"           # Hash-optional hex
color-brew "rgb(255,107,107)" # RGB function
color-brew "hsl(0,71,71)"     # HSL function
color-brew coral              # Named color (140+ supported)
```

### Available Schemes

| Scheme | Description | Colors |
|--------|-------------|--------|
| `complementary` | Opposite on the color wheel | 2 |
| `analogous` | Adjacent on the color wheel | 3 |
| `triadic` | Three colors, 120 degrees apart | 3 |
| `split-complementary` | Base + two adjacent to complement | 3 |
| `tetradic` | Four colors, rectangular on the wheel | 4 |
| `square` | Four colors, 90 degrees apart | 4 |
| `monochromatic` | Same hue, varying lightness | 5 (configurable) |
| `shades` | Base color to black | 5 (configurable) |
| `tints` | Base color to white | 5 (configurable) |

### Gradient Generator

```bash
# Smooth gradient between two colors
color-brew "#FF6B6B" --gradient "#3498DB"

# Control the number of steps
color-brew "#FF6B6B" --gradient "#3498DB" --steps 10
```

### Export Formats

```bash
# CSS custom properties
color-brew "#E74C3C" --export css --output palette.css

# SCSS variables
color-brew "#E74C3C" --export scss --output _palette.scss

# Tailwind config extension
color-brew "#3498DB" --export tailwind --name brand

# JSON (full color data)
color-brew "#2ECC71" --export json --output palette.json

# SVG swatch image
color-brew "#9B59B6" --export svg --output palette.svg

# PNG swatch image (requires Pillow)
color-brew "#E67E22" --export png --output palette.png
```

### Accessibility -- Contrast Checker

```bash
# Check contrast against black and white
color-brew "#3498DB" --contrast white black

# Check against specific colors
color-brew "#FF6B6B" --contrast "#FFFFFF" "#000000" "#2C3E50"
```

### Clipboard

```bash
# Copy hex values to clipboard
color-brew "#FF6B6B" --copy
```

### Color Identity (Reverse Lookup)

```bash
# Identify the closest named CSS color and get full color info
color-brew "#FF6B6B" --identify

# Output:
#   Color Identity for #FF6B6B
#   ─────────────────────────────────────────────
#   HEX: #FF6B6B
#   RGB: rgb(255, 107, 107)
#   HSL: hsl(0.0, 100.0%, 71.0%)
#   CMYK: cmyk(0%, 58%, 58%, 0%)
#   Name: coral (distance: 33.9)
```

### Palette History

```bash
# Save a palette to history
color-brew "#3498DB" --scheme triadic --save

# View your palette history
color-brew --history

# Show more history entries
color-brew --history --history-count 20
```

### Bar Style

```bash
# Use smooth gradient bar instead of block style
color-brew "#FF6B6B" --scheme triadic --bar-style smooth

# Smooth bar with all schemes
color-brew "#2C3E50" --all --bar-style smooth
```

### Quiet Mode

```bash
# Output only hex values (great for scripting)
color-brew "#FF6B6B" --quiet
# Output: #FF6B6B #D4453B #FF8A65
```

### Random Palettes

```bash
# Generate a palette from a completely random color
color-brew --random

# Generate with a mood constraint
color-brew --random warm
color-brew --random pastel
color-brew --random neon

# Combine with any scheme
color-brew --random vibrant --scheme triadic
color-brew --random calm --scheme monochromatic --steps 7

# Available moods: calm, cool, dark, earthy, forest, neon, ocean,
#   pastel, retro, sunset, vibrant, warm
```

### Seasonal Palettes

```bash
# Palettes inspired by the seasons
color-brew --season spring
color-brew --season summer
color-brew --season autumn
color-brew --season winter

# Combine with export or favorites
color-brew --season autumn --favorite "fall-project"
color-brew --season summer --export css --output summer.css
```

### Palette Blending

```bash
# Blend two palettes (weighted average at 50/50)
color-brew "#FF6B6B" --blend "#3498DB"

# Control the blend ratio (0.0 = first color dominates, 1.0 = second)
color-brew "#FF6B6B" --blend "#3498DB" --blend-ratio 0.3

# Interleave mode: alternate colors from both palettes
color-brew "#FF6B6B" --blend "#3498DB" --blend-mode interleave

# Blend with any scheme
color-brew "#E74C3C" --blend "#2ECC71" --scheme triadic
```

### Favorites

```bash
# Save the current palette as a favorite
color-brew "#3498DB" --scheme triadic --favorite "brand-colors"

# List all saved favorites
color-brew --favorites

# Remove a favorite by name
color-brew --unfavorite "brand-colors"

# Combine with random or seasonal palettes
color-brew --random warm --favorite "warm-base"
```

---

## Examples

### Example 1: Design a Website Color Scheme

```bash
$ color-brew "#3498DB" --scheme analogous

  color-brew -- ANALOGOUS palette from #3498DB
  HSL(204, 70%, 53%)
  ────────────────────────────────────────────────────

    #2384C4  rgb( 35,132,196)  hsl(204.0, 64.0%, 45.0%)
    #3498DB  rgb( 52,152,219)  hsl(204.0, 70.0%, 53.0%)
    #5DADE2  rgb( 93,173,226)  hsl(204.0, 67.0%, 63.0%)
```

### Example 2: Export Tailwind Config

```bash
$ color-brew "#E74C3C" --export tailwind --name danger

  danger: {
    '100': '#FDEDEC',
    '200': '#FADBD8',
    '300': '#F5B7B1',
    '400': '#F1948A',
    '500': '#E74C3C',
  },
```

### Example 3: Check Accessibility

```bash
$ color-brew "#3498DB" --contrast white black

  Contrast Ratios
  ────────────────────────────────────────
  White : 3.12:1  Large: AA  Normal: fail AA  fail AAA
  Black : 6.23:1  Large: AA  Normal: AA  fail AAA
```

### Example 4: Random Mood Palette

```bash
$ color-brew --random sunset --scheme complementary

  color-brew -- RANDOM (sunset) COMPLEMENTARY palette
  Base: #E6334A HSL(350, 78%, 55%)
  ────────────────────────────────────────────────────

    #E6334A  rgb(230, 51, 74)   hsl(350.0, 78.0%, 55.0%)
    #33CFE6  rgb( 51,207,230)   hsl(170.0, 78.0%, 55.0%)
```

### Example 5: Blend Two Palettes

```bash
$ color-brew "#FF6B6B" --blend "#3498DB" --blend-ratio 0.3

  color-brew -- ANALOGOUS-BLENDED palette from #FF6B6B
  HSL(0, 100%, 71%)
  ────────────────────────────────────────────────────

    #C28DBB  rgb(194,141,187)  hsl(307.9, 30.3%, 65.7%)
    #C2788D  rgb(194,120,141)  hsl(343.0, 37.8%, 61.6%)
    #C2938D  rgb(194,147,141)  hsl(  6.8, 30.3%, 65.7%)
```

---

## Use Cases

- **Web Development** -- Generate CSS/Tailwind color variables instantly
- **Design** -- Explore color harmonies and export swatches
- **Presentations** -- Pick matching colors for slides and charts
- **Accessibility** -- Check WCAG contrast ratios for text readability
- **Creative Coding** -- Generate palettes for generative art
- **Interior Design** -- Explore color combinations for rooms and spaces
- **Scripting** -- Use `--quiet` mode to pipe colors into other tools
- **Inspiration** -- Use `--random` with mood presets to discover unexpected palettes
- **Brand Design** -- Blend existing brand colors to create new variations

---

## Changelog

### v1.4.0
- Random palette generation with 12 mood presets (`--random [mood]`)
- Seasonal palettes (`--season spring|summer|autumn|winter`)
- Palette blending with merge and interleave modes (`--blend`, `--blend-mode`, `--blend-ratio`)
- Favorites system (`--favorite`, `--favorites`, `--unfavorite`)
- Removed emojis from all output for cleaner terminal experience

### v1.3.0
- Color identity reverse lookup (`--identify`)
- Palette history (`--history`, `--save`)
- Smooth gradient bar style (`--bar-style smooth`)

### v1.2.0
- WCAG contrast ratio checker
- Clipboard support
- Additional export formats

### v1.1.0
- Gradient generator
- Multiple export formats (CSS, SCSS, Tailwind, JSON, SVG, PNG)

### v1.0.0
- Initial release with 9 color schemes
- Named color support

---

## License

MIT License -- use it, share it, make something beautiful.

---

## Contributing

Found a bug? Have an idea? PRs and issues are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
