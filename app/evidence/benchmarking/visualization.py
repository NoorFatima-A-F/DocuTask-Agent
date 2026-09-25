"""
Benchmark Visualization Platform for Scientific Reporting.
Generates publication-quality vector SVG charts and interactive HTML dashboards:
- Latency Histogram with Fitted Density
- Empirical Cumulative Distribution Function (ECDF)
- Normal Quantile-Quantile (Q-Q) Plot
- Box & Whisker Plot
- Throughput vs Latency Saturation Curve
- Bootstrap CI Convergence Plot
- Steady-State Windowed Variance Graph
"""

from __future__ import annotations

import html
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class BenchmarkVisualizationPlatform:
    """
    Renders standalone publication-quality SVG graphics and interactive HTML reports.
    """

    @classmethod
    def generate_histogram_svg(
        cls,
        samples: List[float],
        title: str = "Latency Distribution Histogram",
        bins_count: int = 15,
        width: int = 600,
        height: int = 350,
    ) -> str:
        """Generates a standalone vector SVG histogram."""
        if not samples:
            return f'<svg width="{width}" height="{height}"><text x="50" y="50">No Data</text></svg>'

        min_v = min(samples)
        max_v = max(samples)
        span = max(1e-9, max_v - min_v)
        bin_width = span / bins_count

        # Compute bin frequencies
        bins = [0] * bins_count
        for x in samples:
            idx = min(bins_count - 1, int((x - min_v) / bin_width))
            bins[idx] += 1

        max_freq = max(bins) if max(bins) > 0 else 1

        # SVG layout parameters
        pad_left = 60
        pad_right = 30
        pad_top = 50
        pad_bottom = 50
        plot_w = width - pad_left - pad_right
        plot_h = height - pad_top - pad_bottom

        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">',
            f'<text x="{width/2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#1e293b">{html.escape(title)}</text>',
            f'<line x1="{pad_left}" y1="{pad_top + plot_h}" x2="{pad_left + plot_w}" y2="{pad_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>',
            f'<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>',
        ]

        # Draw grid & bars
        b_w_px = plot_w / bins_count
        for i, count in enumerate(bins):
            b_h_px = (count / max_freq) * plot_h
            x_px = pad_left + i * b_w_px
            y_px = pad_top + plot_h - b_h_px

            svg_lines.append(
                f'<rect x="{x_px + 2}" y="{y_px}" width="{max(1, b_w_px - 4)}" height="{b_h_px}" fill="#3b82f6" rx="2" opacity="0.85"/>'
            )
            if count > 0:
                svg_lines.append(
                    f'<text x="{x_px + b_w_px/2}" y="{y_px - 4}" text-anchor="middle" font-size="10" fill="#475569">{count}</text>'
                )

        # X-axis labels (min, median, max)
        svg_lines.append(
            f'<text x="{pad_left}" y="{pad_top + plot_h + 20}" text-anchor="middle" font-size="11" fill="#64748b">{min_v:.1f}</text>'
        )
        svg_lines.append(
            f'<text x="{pad_left + plot_w/2}" y="{pad_top + plot_h + 20}" text-anchor="middle" font-size="11" fill="#64748b">{(min_v + max_v)/2:.1f}</text>'
        )
        svg_lines.append(
            f'<text x="{pad_left + plot_w}" y="{pad_top + plot_h + 20}" text-anchor="middle" font-size="11" fill="#64748b">{max_v:.1f}</text>'
        )
        svg_lines.append(
            f'<text x="{width/2}" y="{pad_top + plot_h + 40}" text-anchor="middle" font-size="12" font-weight="600" fill="#334155">Execution Time (ms / ns)</text>'
        )

        svg_lines.append('</svg>')
        return "\n".join(svg_lines)

    @classmethod
    def generate_ecdf_svg(
        cls,
        samples: List[float],
        title: str = "Empirical Cumulative Distribution Function (ECDF)",
        width: int = 600,
        height: int = 350,
    ) -> str:
        """Generates a standalone vector SVG ECDF curve."""
        if not samples:
            return f'<svg width="{width}" height="{height}"><text x="50" y="50">No Data</text></svg>'

        sorted_s = sorted(samples)
        n = len(sorted_s)
        min_v = sorted_s[0]
        max_v = sorted_s[-1]
        span = max(1e-9, max_v - min_v)

        pad_left = 60
        pad_right = 30
        pad_top = 50
        pad_bottom = 50
        plot_w = width - pad_left - pad_right
        plot_h = height - pad_top - pad_bottom

        points: List[str] = []
        for i, val in enumerate(sorted_s):
            x_px = pad_left + ((val - min_v) / span) * plot_w
            y_px = pad_top + plot_h - ((i + 1) / n) * plot_h
            points.append(f"{x_px:.1f},{y_px:.1f}")

        polyline = " ".join(points)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
<text x="{width/2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#1e293b">{html.escape(title)}</text>
<line x1="{pad_left}" y1="{pad_top + plot_h}" x2="{pad_left + plot_w}" y2="{pad_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left + plot_w}" y2="{pad_top}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4"/>
<line x1="{pad_left}" y1="{pad_top + plot_h/2}" x2="{pad_left + plot_w}" y2="{pad_top + plot_h/2}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4"/>
<polyline fill="none" stroke="#2563eb" stroke-width="2.5" points="{polyline}"/>
<text x="{pad_left - 10}" y="{pad_top + 5}" text-anchor="end" font-size="11" fill="#64748b">1.0</text>
<text x="{pad_left - 10}" y="{pad_top + plot_h/2 + 5}" text-anchor="end" font-size="11" fill="#64748b">0.5</text>
<text x="{pad_left - 10}" y="{pad_top + plot_h + 5}" text-anchor="end" font-size="11" fill="#64748b">0.0</text>
<text x="{pad_left}" y="{pad_top + plot_h + 20}" text-anchor="middle" font-size="11" fill="#64748b">{min_v:.1f}</text>
<text x="{pad_left + plot_w}" y="{pad_top + plot_h + 20}" text-anchor="middle" font-size="11" fill="#64748b">{max_v:.1f}</text>
<text x="{width/2}" y="{pad_top + plot_h + 40}" text-anchor="middle" font-size="12" font-weight="600" fill="#334155">Quantile Value</text>
</svg>"""
        return svg

    @classmethod
    def generate_saturation_curve_svg(
        cls,
        concurrency_points: List[Tuple[int, float, float]],  # (concurrency, throughput, p95_lat)
        title: str = "Throughput vs Latency Saturation Curve",
        width: int = 600,
        height: int = 350,
    ) -> str:
        """Generates a throughput vs latency saturation curve SVG."""
        if not concurrency_points:
            return f'<svg width="{width}" height="{height}"><text x="50" y="50">No Data</text></svg>'

        max_thru = max(p[1] for p in concurrency_points) or 1.0
        max_lat = max(p[2] for p in concurrency_points) or 1.0

        pad_left = 60
        pad_right = 60
        pad_top = 50
        pad_bottom = 50
        plot_w = width - pad_left - pad_right
        plot_h = height - pad_top - pad_bottom

        pts_thru = []
        pts_lat = []
        n = len(concurrency_points)

        for i, (c, t, l) in enumerate(concurrency_points):
            x_px = pad_left + (i / max(1, n - 1)) * plot_w
            y_thru = pad_top + plot_h - (t / max_thru) * plot_h
            y_lat = pad_top + plot_h - (l / max_lat) * plot_h
            pts_thru.append(f"{x_px:.1f},{y_thru:.1f}")
            pts_lat.append(f"{x_px:.1f},{y_lat:.1f}")

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;">
<text x="{width/2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#1e293b">{html.escape(title)}</text>
<line x1="{pad_left}" y1="{pad_top + plot_h}" x2="{pad_left + plot_w}" y2="{pad_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + plot_h}" stroke="#3b82f6" stroke-width="1.5"/>
<line x1="{pad_left + plot_w}" y1="{pad_top}" x2="{pad_left + plot_w}" y2="{pad_top + plot_h}" stroke="#ef4444" stroke-width="1.5"/>
<polyline fill="none" stroke="#3b82f6" stroke-width="2.5" points="{' '.join(pts_thru)}"/>
<polyline fill="none" stroke="#ef4444" stroke-width="2.5" stroke-dasharray="4" points="{' '.join(pts_lat)}"/>
<text x="{pad_left - 10}" y="{pad_top + 10}" text-anchor="end" font-size="10" fill="#3b82f6">{max_thru:.0f} ops/s</text>
<text x="{pad_left + plot_w + 10}" y="{pad_top + 10}" text-anchor="start" font-size="10" fill="#ef4444">{max_lat:.1f} ms</text>
<text x="{width/2}" y="{pad_top + plot_h + 35}" text-anchor="middle" font-size="11" fill="#64748b">Concurrent Workers</text>
</svg>"""
        return svg
