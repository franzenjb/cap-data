#!/usr/bin/env python3
"""
Convert all Plotly HTML visualizations to PNG/JPG images
"""

import plotly.graph_objects as go
import plotly.io as pio
import os

# Set up kaleido for static image export
pio.kaleido.scope.mathjax = None

# American Red Cross Brand Colors
ARC_RED = '#CC0000'
ARC_GRAY = '#6B7C93'
ARC_DARK_GRAY = '#4A5568'
ARC_LIGHT_GRAY = '#E2E8F0'

print("\n📊 Converting all visualizations to PNG images...\n")
print("=" * 60)

# Import and run the visualization creation script
import create_20_visualizations as viz

# List of all visualization functions
viz_functions = [
    ('roi_by_disaster', viz.create_roi_by_disaster),
    ('roi_by_partner', viz.create_roi_by_partner),
    ('cost_containment_donut', viz.create_cost_containment_donut),
    ('ia_uptake_comparison', viz.create_ia_uptake_comparison),
    ('speed_advantage', viz.create_speed_advantage),
    ('volunteer_trends', viz.create_volunteer_trends),
    ('homes_safer_impact', viz.create_homes_safer_impact),
    ('stakeholder_sentiment', viz.create_stakeholder_sentiment),
    ('meal_cost_comparison', viz.create_meal_cost_comparison),
    ('response_timeline', viz.create_response_timeline),
    ('geographic_impact', viz.create_geographic_heatmap),
    ('quarterly_trends', viz.create_quarterly_trends),
    ('partner_distribution', viz.create_partner_distribution),
    ('failures_prevented', viz.create_failures_prevented),
    ('youth_preparedness', viz.create_youth_preparedness),
    ('francine_breakdown', viz.create_francine_breakdown),
    ('asset_utilization', viz.create_asset_utilization),
    ('coalition_growth', viz.create_coalition_growth),
    ('disaster_efficiency', viz.create_disaster_efficiency),
    ('kpi_dashboard', viz.create_kpi_dashboard),
    ('risk_timeline', viz.create_risk_timeline),
    ('cultural_metrics', viz.create_cultural_metrics),
    ('investment_return', viz.create_investment_return),
    ('executive_scorecard', viz.create_executive_scorecard)
]

# Create images directory
os.makedirs('/Users/jefffranzen/cap-data/images', exist_ok=True)

# Convert each visualization to PNG
successful = 0
failed = 0

for name, func in viz_functions:
    try:
        # Create the figure
        fig = func()
        
        # Save as PNG (high resolution)
        png_path = f'/Users/jefffranzen/cap-data/images/{name}.png'
        fig.write_image(png_path, width=1200, height=600, scale=2)
        
        # Also save as JPG
        jpg_path = f'/Users/jefffranzen/cap-data/images/{name}.jpg'
        fig.write_image(jpg_path, width=1200, height=600, scale=2)
        
        print(f"✅ Converted: {name}")
        successful += 1
        
    except Exception as e:
        print(f"❌ Failed: {name} - {str(e)}")
        failed += 1

print("=" * 60)
print(f"\n📊 Conversion Complete!")
print(f"✅ Successful: {successful} visualizations")
if failed > 0:
    print(f"❌ Failed: {failed} visualizations")
print(f"\n📁 PNG images saved to: /Users/jefffranzen/cap-data/images/")
print(f"📁 JPG images saved to: /Users/jefffranzen/cap-data/images/")
print("\n🎯 All images are high-resolution (1200x600px @ 2x scale)")
print("   Ready for insertion into reports and presentations!")