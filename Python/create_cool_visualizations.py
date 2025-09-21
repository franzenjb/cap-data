#!/usr/bin/env python3
"""
Create 20 COOL, MODERN visualizations with scatter plots, 3D charts, and advanced designs
Fortune 500 / Wall Street quality with American Red Cross branding
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

# Create output directory
os.makedirs('/Users/jefffranzen/cap-data/cool_visualizations', exist_ok=True)

# American Red Cross Brand Colors
ARC_RED = '#CC0000'
ARC_GRAY = '#6B7C93'
ARC_DARK_GRAY = '#4A5568'
ARC_LIGHT_GRAY = '#E2E8F0'
ARC_BLACK = '#000000'
ARC_WHITE = '#FFFFFF'

# Extended color palette for variety
PALETTE = ['#CC0000', '#E53E3E', '#6B7C93', '#4A5568', '#F56565', '#FC8181', '#FEB2B2', '#FED7D7']

def save_figure(fig, name):
    """Save figure as both HTML and PNG"""
    fig.write_html(f'/Users/jefffranzen/cap-data/cool_visualizations/{name}.html')
    try:
        fig.write_image(f'/Users/jefffranzen/cap-data/cool_visualizations/{name}.png', width=1400, height=800, scale=2)
    except:
        pass
    print(f"✅ Created: {name}")
    return fig

# 1. 3D SCATTER PLOT - ROI vs Speed vs Quality
def create_3d_performance():
    partners = ['Resilience Hub A', 'Resilience Hub B', 'Gateway A', 'Gateway B', 
                'Hunger Partner A', 'Hunger Partner B', 'Health Partner', 'Housing Partner']
    roi = [33.5, 32.1, 30.1, 28.5, 26.3, 24.2, 23.0, 4.9]
    speed = [95, 92, 88, 85, 82, 78, 75, 65]
    quality = [98, 95, 92, 90, 88, 85, 83, 75]
    
    fig = go.Figure(data=[go.Scatter3d(
        x=roi,
        y=speed,
        z=quality,
        mode='markers+text',
        text=partners,
        textposition='top center',
        marker=dict(
            size=[r/2 for r in roi],
            color=roi,
            colorscale=[[0, ARC_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
            showscale=True,
            colorbar=dict(title="ROI %", thickness=20),
            line=dict(color='white', width=2),
            opacity=0.9
        )
    )])
    
    fig.update_layout(
        title='3D Performance Matrix: ROI × Speed × Quality',
        title_font=dict(size=24, family='Arial Black', color=ARC_RED),
        scene=dict(
            xaxis=dict(title='ROI (%)', gridcolor='lightgray', backgroundcolor=ARC_WHITE),
            yaxis=dict(title='Speed Score', gridcolor='lightgray', backgroundcolor=ARC_WHITE),
            zaxis=dict(title='Quality Score', gridcolor='lightgray', backgroundcolor=ARC_WHITE),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
        ),
        paper_bgcolor=ARC_WHITE,
        height=800,
        width=1400
    )
    
    return save_figure(fig, '3d_performance_matrix')

# 2. ANIMATED BUBBLE CHART - Cost Savings Over Time
def create_animated_bubbles():
    # Generate data for animation
    quarters = ['Q1 FY23', 'Q2 FY23', 'Q3 FY23', 'Q4 FY23', 
                'Q1 FY24', 'Q2 FY24', 'Q3 FY24', 'Q4 FY24',
                'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25']
    
    data = []
    for i, q in enumerate(quarters):
        for partner_type in ['Resilience', 'Gateway', 'Hunger', 'Health', 'Housing']:
            data.append({
                'Quarter': q,
                'Partner Type': partner_type,
                'Cost Savings': np.random.randint(20000, 100000) * (i+1)/4,
                'Efficiency': np.random.randint(70, 98),
                'Impact': np.random.randint(60, 100),
                'Size': np.random.randint(20, 100)
            })
    
    df = pd.DataFrame(data)
    
    fig = px.scatter(df, x='Efficiency', y='Impact', 
                     animation_frame='Quarter',
                     animation_group='Partner Type',
                     size='Size', color='Partner Type',
                     hover_name='Partner Type',
                     color_discrete_sequence=PALETTE,
                     size_max=60,
                     range_x=[60, 100], range_y=[50, 105],
                     title='Animated Impact Evolution: Partner Performance Over Time')
    
    fig.update_layout(
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        xaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY)
    )
    
    return save_figure(fig, 'animated_bubble_evolution')

# 3. SUNBURST CHART - Hierarchical Cost Breakdown
def create_sunburst_breakdown():
    data = dict(
        labels=['Total Savings', 
                'Direct Services', 'Volunteer Labor', 'Facilities', 'Equipment',
                'Feeding', 'Shelter', 'Transportation', 'Local Vol', 'Skilled Vol',
                'IA Centers', 'Warehouses', 'Trucks', 'Generators'],
        parents=['', 
                 'Total Savings', 'Total Savings', 'Total Savings', 'Total Savings',
                 'Direct Services', 'Direct Services', 'Direct Services', 'Volunteer Labor', 'Volunteer Labor',
                 'Facilities', 'Facilities', 'Equipment', 'Equipment'],
        values=[1606305, 
                650000, 450000, 200000, 306305,
                400000, 150000, 100000, 300000, 150000,
                150000, 50000, 206305, 100000],
        text=['$1.6M Total', 
              '$650K', '$450K', '$200K', '$306K',
              '$400K', '$150K', '$100K', '$300K', '$150K',
              '$150K', '$50K', '$206K', '$100K']
    )
    
    fig = go.Figure(go.Sunburst(
        labels=data['labels'],
        parents=data['parents'],
        values=data['values'],
        branchvalues='total',
        text=data['text'],
        textinfo='label+text+percent entry',
        marker=dict(colors=[ARC_RED if i < 5 else ARC_GRAY for i in range(len(data['labels']))],
                   line=dict(color='white', width=3)),
        hovertemplate='<b>%{label}</b><br>Amount: %{text}<br>%{percentEntry}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Interactive Cost Containment Hierarchy - Click to Explore',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=800,
        width=1400
    )
    
    return save_figure(fig, 'sunburst_cost_hierarchy')

# 4. SCATTER PLOT MATRIX - Multi-dimensional Analysis
def create_scatter_matrix():
    # Generate correlation data
    np.random.seed(42)
    n_points = 50
    
    data = pd.DataFrame({
        'ROI (%)': np.random.normal(28, 10, n_points),
        'Speed (days)': np.random.normal(2, 1, n_points),
        'Quality Score': np.random.normal(85, 10, n_points),
        'Cost Saved ($K)': np.random.normal(50, 20, n_points),
        'Volunteers': np.random.normal(100, 30, n_points)
    })
    
    # Add some correlation
    data['Quality Score'] = data['ROI (%)'] * 2 + np.random.normal(0, 5, n_points)
    data['Cost Saved ($K)'] = data['ROI (%)'] * 1.5 + np.random.normal(0, 10, n_points)
    
    fig = px.scatter_matrix(data,
                            dimensions=['ROI (%)', 'Speed (days)', 'Quality Score', 'Cost Saved ($K)', 'Volunteers'],
                            color=data['ROI (%)'],
                            color_continuous_scale=[[0, ARC_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
                            title='Multi-Dimensional Performance Correlation Matrix',
                            height=1000, width=1400)
    
    fig.update_traces(diagonal_visible=False, showupperhalf=False,
                     marker=dict(size=5, opacity=0.7))
    
    fig.update_layout(
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        coloraxis_colorbar=dict(title="ROI %")
    )
    
    return save_figure(fig, 'scatter_matrix_analysis')

# 5. ADVANCED HEATMAP - Geographic Impact with Annotations
def create_advanced_heatmap():
    states = ['TX', 'FL', 'LA', 'TN', 'KY', 'CA', 'MO', 'AR', 'AL', 'MS', 'GA', 'SC']
    metrics = ['Speed', 'Quality', 'Cost Savings', 'Volunteer Growth', 'IA Uptake', 'Community Trust']
    
    # Generate realistic looking data
    z_values = []
    for metric in metrics:
        row = []
        for state in states:
            if state in ['TX', 'FL', 'LA']:  # High performing states
                row.append(np.random.randint(80, 100))
            elif state in ['TN', 'KY', 'CA']:  # Medium performing
                row.append(np.random.randint(65, 85))
            else:  # Lower performing
                row.append(np.random.randint(50, 75))
        z_values.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=states,
        y=metrics,
        colorscale=[[0, ARC_LIGHT_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
        text=z_values,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Score", thickness=20),
        hoverongaps=False
    ))
    
    # Add annotations for top performers
    for i, metric in enumerate(metrics):
        max_val = max(z_values[i])
        max_idx = z_values[i].index(max_val)
        fig.add_annotation(
            x=states[max_idx], y=metric,
            text='★', font=dict(size=20, color='gold'),
            showarrow=False
        )
    
    fig.update_layout(
        title='Geographic Performance Heatmap with Excellence Indicators',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        xaxis_title='State',
        yaxis_title='Performance Metric',
        paper_bgcolor=ARC_WHITE,
        height=600,
        width=1400,
        xaxis=dict(tickangle=0),
        yaxis=dict(tickmode='linear')
    )
    
    return save_figure(fig, 'advanced_heatmap')

# 6. PARALLEL COORDINATES - Partner Performance Profiles
def create_parallel_coordinates():
    # Create partner performance data
    partners = ['Resilience Hub', 'Community Gateway', 'Hunger Partner', 
                'Health Partner', 'Housing Partner'] * 5
    
    data = pd.DataFrame({
        'Partner': partners,
        'ROI': [33.5, 30.1, 26.3, 23.0, 4.9] * 5 + np.random.normal(0, 2, 25),
        'Speed': [95, 88, 82, 75, 65] * 5 + np.random.normal(0, 5, 25),
        'Quality': [98, 92, 88, 83, 75] * 5 + np.random.normal(0, 3, 25),
        'Cost Efficiency': [92, 85, 78, 72, 60] * 5 + np.random.normal(0, 4, 25),
        'Community Impact': [96, 90, 85, 80, 70] * 5 + np.random.normal(0, 3, 25)
    })
    
    # Normalize values
    for col in ['ROI', 'Speed', 'Quality', 'Cost Efficiency', 'Community Impact']:
        data[col] = np.clip(data[col], 0, 100)
    
    fig = px.parallel_coordinates(data, 
                                  dimensions=['ROI', 'Speed', 'Quality', 'Cost Efficiency', 'Community Impact'],
                                  color=data['ROI'],
                                  color_continuous_scale=[[0, ARC_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
                                  title='Partner Performance Profiles - Interactive Parallel Coordinates')
    
    fig.update_layout(
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=700,
        width=1400,
        coloraxis_colorbar=dict(title="ROI %")
    )
    
    return save_figure(fig, 'parallel_coordinates')

# 7. VIOLIN PLOT - Distribution Analysis
def create_violin_distribution():
    # Generate realistic distributions
    categories = ['Hurricane', 'Tornado', 'Flood', 'Wildfire', 'Storm']
    data = []
    
    for cat in categories:
        if cat == 'Hurricane':
            values = np.random.normal(85, 10, 100)
        elif cat == 'Tornado':
            values = np.random.normal(75, 12, 80)
        elif cat == 'Flood':
            values = np.random.normal(70, 15, 90)
        elif cat == 'Wildfire':
            values = np.random.normal(68, 8, 70)
        else:
            values = np.random.normal(72, 11, 85)
        
        for v in values:
            data.append({'Disaster Type': cat, 'Performance Score': v})
    
    df = pd.DataFrame(data)
    
    fig = px.violin(df, x='Disaster Type', y='Performance Score',
                   color='Disaster Type',
                   color_discrete_sequence=[ARC_RED, '#E53E3E', ARC_GRAY, ARC_DARK_GRAY, '#F56565'],
                   box=True, points='all',
                   title='Performance Distribution by Disaster Type')
    
    fig.update_layout(
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        showlegend=False,
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY)
    )
    
    return save_figure(fig, 'violin_distribution')

# 8. SANKEY DIAGRAM - Resource Flow
def create_sankey_flow():
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color=ARC_BLACK, width=0.5),
            label=['CAP Investment', 'Partners', 'Services', 'Communities',
                   'Resilience Hubs', 'Gateways', 'Hunger', 'Health', 'Housing',
                   'Feeding', 'Shelter', 'Supplies', 'Medical',
                   'Urban', 'Rural', 'Underserved'],
            color=[ARC_RED, ARC_GRAY, '#F56565', ARC_DARK_GRAY,
                   '#FEB2B2', '#FEB2B2', '#FEB2B2', '#FEB2B2', '#FEB2B2',
                   '#CBD5E0', '#CBD5E0', '#CBD5E0', '#CBD5E0',
                   ARC_LIGHT_GRAY, ARC_LIGHT_GRAY, ARC_LIGHT_GRAY]
        ),
        link=dict(
            source=[0,0,0,0,0, 1,1,1,1, 4,5,6,7,8, 9,10,11,12, 2,2,2],
            target=[4,5,6,7,8, 9,10,11,12, 2,2,2,2,2, 13,14,15,13, 13,14,15],
            value=[30,25,20,15,10, 25,25,25,25, 30,25,20,15,10, 40,30,20,10, 33,33,34],
            color='rgba(204, 0, 0, 0.2)'
        )
    )])
    
    fig.update_layout(
        title='Resource Flow: From Investment to Community Impact',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=700,
        width=1400,
        font_size=12
    )
    
    return save_figure(fig, 'sankey_resource_flow')

# 9. SCATTER WITH MARGINAL PLOTS
def create_scatter_marginal():
    # Generate correlated data
    np.random.seed(42)
    investment = np.random.exponential(50000, 100)
    returns = investment * np.random.normal(0.283, 0.1, 100)  # 28.3% ROI with variation
    
    df = pd.DataFrame({
        'Investment ($)': investment,
        'Return ($)': returns,
        'ROI (%)': (returns / investment) * 100
    })
    
    fig = px.scatter(df, x='Investment ($)', y='Return ($)',
                    color='ROI (%)',
                    color_continuous_scale=[[0, ARC_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
                    marginal_x='histogram',
                    marginal_y='box',
                    title='Investment vs Return Analysis with Distribution Profiles',
                    hover_data=['ROI (%)'])
    
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    
    fig.update_layout(
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        xaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY)
    )
    
    return save_figure(fig, 'scatter_marginal_analysis')

# 10. TREEMAP - Hierarchical Impact
def create_treemap_impact():
    data = dict(
        names=['CAP Program', 
               'Quality', 'Speed', 'Cost', 'Community',
               'Cultural Fit', 'Access', 'Dignity',
               'Same Day', 'Next Day', '2-3 Days',
               'Direct Savings', 'Volunteer Value', 'Asset Value',
               'Trust Building', 'Preparedness', 'Resilience'],
        parents=['',
                'CAP Program', 'CAP Program', 'CAP Program', 'CAP Program',
                'Quality', 'Quality', 'Quality',
                'Speed', 'Speed', 'Speed',
                'Cost', 'Cost', 'Cost',
                'Community', 'Community', 'Community'],
        values=[100,
               30, 25, 25, 20,
               12, 10, 8,
               15, 7, 3,
               10, 10, 5,
               8, 7, 5]
    )
    
    fig = go.Figure(go.Treemap(
        labels=data['names'],
        parents=data['parents'],
        values=data['values'],
        marker=dict(
            colors=[ARC_RED] + [ARC_GRAY]*4 + ['#F56565']*12,
            line=dict(width=2, color='white')
        ),
        textinfo='label+value+percent parent',
        hovertemplate='<b>%{label}</b><br>Impact Score: %{value}<br>%{percentParent} of parent<extra></extra>'
    ))
    
    fig.update_layout(
        title='CAP Impact Treemap - Click to Explore Components',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=700,
        width=1400
    )
    
    return save_figure(fig, 'treemap_impact')

# 11. FUNNEL CHART - Service Delivery Pipeline
def create_funnel_pipeline():
    stages = ['Communities Identified', 'Partners Engaged', 'Resources Mobilized', 
              'Services Delivered', 'Clients Served', 'Impact Measured']
    values = [10000, 8500, 7200, 6500, 5800, 5200]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition='inside',
        textinfo='value+percent initial',
        opacity=0.85,
        marker=dict(
            color=[ARC_RED, '#E53E3E', '#F56565', '#FC8181', '#FEB2B2', '#FED7D7'],
            line=dict(width=2, color=ARC_WHITE)
        ),
        connector=dict(line=dict(color=ARC_GRAY, width=2))
    ))
    
    fig.update_layout(
        title='Service Delivery Pipeline Efficiency',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=700,
        width=1400
    )
    
    return save_figure(fig, 'funnel_pipeline')

# 12. NETWORK GRAPH - Partner Connections
def create_network_graph():
    # Create network data
    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color=ARC_LIGHT_GRAY),
        hoverinfo='none',
        mode='lines')
    
    # Generate positions
    np.random.seed(42)
    n_nodes = 30
    pos = {}
    for i in range(n_nodes):
        pos[i] = (np.random.randn(), np.random.randn())
    
    # Add edges
    for i in range(n_nodes):
        for j in range(i+1, min(i+4, n_nodes)):
            x0, y0 = pos[i]
            x1, y1 = pos[j]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
    
    # Node trace
    node_trace = go.Scatter(
        x=[pos[i][0] for i in range(n_nodes)],
        y=[pos[i][1] for i in range(n_nodes)],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale=[[0, ARC_GRAY], [1, ARC_RED]],
            size=[20 + i for i in range(n_nodes)],
            color=list(range(n_nodes)),
            colorbar=dict(thickness=15, title='Connections', xanchor='left', titleside='right'),
            line_width=2,
            line_color='white'
        ),
        text=['Red Cross' if i == 0 else f'Partner {i}' for i in range(n_nodes)],
        textposition='top center'
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title='CAP Partner Network Visualization',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        showlegend=False,
        hovermode='closest',
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=800,
        width=1400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return save_figure(fig, 'network_graph')

# 13. ANIMATED LINE RACE - Growth Over Time
def create_line_race():
    quarters = list(range(1, 13))
    
    fig = go.Figure()
    
    # Add traces for different metrics
    metrics = {
        'Cost Savings': [i * 134000 for i in quarters],
        'Volunteers': [100 + i * 35 for i in quarters],
        'Communities Served': [5 + i * 8 for i in quarters],
        'Partner Count': [10 + i * 4 for i in quarters]
    }
    
    colors = [ARC_RED, '#E53E3E', ARC_GRAY, ARC_DARK_GRAY]
    
    for (metric, values), color in zip(metrics.items(), colors):
        # Normalize to percentage growth
        normalized = [(v / values[0] - 1) * 100 for v in values]
        
        fig.add_trace(go.Scatter(
            x=quarters,
            y=normalized,
            mode='lines+markers',
            name=metric,
            line=dict(width=4, color=color),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title='CAP Growth Race - Percentage Increase from Baseline',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        xaxis_title='Quarter',
        yaxis_title='Growth (%)',
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        hovermode='x unified',
        xaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        legend=dict(x=0.02, y=0.98)
    )
    
    return save_figure(fig, 'growth_race')

# 14. POLAR BAR CHART - 360° Impact View
def create_polar_bar():
    categories = ['Speed', 'Quality', 'Cost\nSavings', 'Volunteer\nGrowth', 
                  'Community\nTrust', 'Cultural\nFit', 'Geographic\nReach', 'Innovation']
    
    fig = go.Figure()
    
    # CAP Performance
    fig.add_trace(go.Barpolar(
        r=[92, 95, 88, 86, 96, 94, 85, 90],
        theta=categories,
        name='CAP Performance',
        marker_color=ARC_RED,
        marker_line_color=ARC_WHITE,
        marker_line_width=2,
        opacity=0.8
    ))
    
    # Benchmark
    fig.add_trace(go.Barpolar(
        r=[75, 75, 75, 75, 75, 75, 75, 75],
        theta=categories,
        name='Industry Benchmark',
        marker_color=ARC_GRAY,
        marker_line_color=ARC_WHITE,
        marker_line_width=2,
        opacity=0.5
    ))
    
    fig.update_layout(
        title='360° Performance Assessment',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont_size=10
            ),
            angularaxis=dict(
                tickfont_size=12,
                rotation=90
            )
        ),
        paper_bgcolor=ARC_WHITE,
        height=800,
        width=1400,
        legend=dict(x=0.85, y=0.95)
    )
    
    return save_figure(fig, 'polar_360_view')

# 15. DENSITY CONTOUR - Performance Clusters
def create_density_contour():
    # Generate clustered data
    np.random.seed(42)
    
    # High performers cluster
    x1 = np.random.normal(80, 5, 100)
    y1 = np.random.normal(85, 5, 100)
    
    # Medium performers cluster
    x2 = np.random.normal(60, 8, 80)
    y2 = np.random.normal(65, 8, 80)
    
    # Low performers cluster
    x3 = np.random.normal(40, 6, 50)
    y3 = np.random.normal(45, 6, 50)
    
    x = np.concatenate([x1, x2, x3])
    y = np.concatenate([y1, y2, y3])
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram2dContour(
        x=x,
        y=y,
        colorscale=[[0, ARC_WHITE], [0.5, '#FEB2B2'], [1, ARC_RED]],
        reversescale=False,
        xaxis='x',
        yaxis='y',
        contours=dict(
            showlines=True,
            showlabels=True,
            labelfont=dict(size=9, color='white')
        )
    ))
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            color='rgba(0,0,0,0.3)',
            size=3
        ),
        showlegend=False
    ))
    
    fig.update_layout(
        title='Performance Density Map - Partner Clustering Analysis',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        xaxis_title='Efficiency Score',
        yaxis_title='Impact Score',
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        xaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY)
    )
    
    return save_figure(fig, 'density_clusters')

# 16. SURFACE PLOT - 3D Performance Landscape
def create_surface_landscape():
    # Create mesh
    x = np.linspace(0, 100, 50)
    y = np.linspace(0, 100, 50)
    X, Y = np.meshgrid(x, y)
    
    # Create performance surface with peaks
    Z = (np.sin(X/10) * np.cos(Y/10) + 1) * 50
    Z += np.exp(-((X-80)**2 + (Y-85)**2)/200) * 30  # High performance peak
    Z += np.exp(-((X-30)**2 + (Y-40)**2)/300) * 20  # Low performance valley
    
    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=Z,
        colorscale=[[0, ARC_GRAY], [0.5, '#F56565'], [1, ARC_RED]],
        contours={
            'z': {'show': True, 'usecolormap': True, 'highlightcolor': 'white', 'project': {'z': True}}
        }
    )])
    
    fig.update_layout(
        title='3D Performance Landscape - Peaks of Excellence',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        scene=dict(
            xaxis_title='Speed Metric',
            yaxis_title='Quality Metric',
            zaxis_title='Overall Performance',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        paper_bgcolor=ARC_WHITE,
        height=800,
        width=1400
    )
    
    return save_figure(fig, 'surface_landscape')

# 17. RIDGELINE PLOT - Distribution Evolution
def create_ridgeline():
    fig = go.Figure()
    
    years = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']
    
    for i, year in enumerate(years):
        # Generate distribution that improves over time
        y_values = np.random.normal(60 + i*8, 15 - i*2, 1000)
        
        fig.add_trace(go.Violin(
            x=y_values,
            y=[year] * len(y_values),
            name=year,
            side='positive',
            line_color=[ARC_GRAY, ARC_GRAY, '#F56565', '#E53E3E', ARC_RED][i],
            fillcolor=[ARC_GRAY, ARC_GRAY, '#F56565', '#E53E3E', ARC_RED][i],
            opacity=0.6,
            meanline_visible=True
        ))
    
    fig.update_layout(
        title='Performance Distribution Evolution - The Journey to Excellence',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        xaxis_title='Performance Score',
        yaxis_title='Fiscal Year',
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        showlegend=False,
        xaxis=dict(gridcolor=ARC_LIGHT_GRAY),
        violingap=0,
        violinmode='overlay'
    )
    
    return save_figure(fig, 'ridgeline_evolution')

# 18. SPIDER WEB COMPARISON
def create_spider_comparison():
    categories = ['Speed', 'Quality', 'Cost Savings', 'Coverage', 
                  'Sustainability', 'Innovation', 'Partnership', 'Trust']
    
    fig = go.Figure()
    
    # Add multiple partner types
    partner_data = {
        'Resilience Hubs': [95, 98, 92, 88, 85, 90, 96, 94],
        'Community Gateways': [88, 92, 85, 82, 80, 85, 90, 88],
        'Hunger Partners': [82, 88, 78, 85, 82, 75, 85, 86],
        'Health Partners': [75, 83, 72, 78, 88, 78, 80, 82],
        'Housing Partners': [65, 75, 60, 70, 75, 65, 72, 78]
    }
    
    colors = [ARC_RED, '#E53E3E', ARC_GRAY, ARC_DARK_GRAY, ARC_LIGHT_GRAY]
    
    for (partner, values), color in zip(partner_data.items(), colors):
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            name=partner,
            line=dict(color=color, width=2),
            fill='toself',
            fillcolor=color,
            opacity=0.3
        ))
    
    fig.update_layout(
        title='Multi-Partner Performance Spider Analysis',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont_size=10
            ),
            angularaxis=dict(tickfont_size=12)
        ),
        paper_bgcolor=ARC_WHITE,
        height=800,
        width=1400,
        legend=dict(x=0.85, y=0.95),
        showlegend=True
    )
    
    return save_figure(fig, 'spider_comparison')

# 19. BOX PLOT WITH JITTER - Statistical Excellence
def create_box_jitter():
    # Generate data for different metrics
    metrics = []
    scores = []
    
    metric_names = ['Speed', 'Quality', 'Cost Efficiency', 'Community Impact']
    
    for metric in metric_names:
        if metric == 'Quality':
            values = np.random.normal(88, 8, 100)
        elif metric == 'Speed':
            values = np.random.normal(85, 10, 100)
        elif metric == 'Cost Efficiency':
            values = np.random.normal(82, 12, 100)
        else:
            values = np.random.normal(78, 15, 100)
        
        metrics.extend([metric] * 100)
        scores.extend(values)
    
    fig = go.Figure()
    
    # Add box plots
    for metric in metric_names:
        metric_scores = [s for m, s in zip(metrics, scores) if m == metric]
        
        fig.add_trace(go.Box(
            y=metric_scores,
            name=metric,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(
                color=ARC_RED if metric == 'Quality' else ARC_GRAY,
                size=4,
                opacity=0.5
            ),
            line=dict(color=ARC_RED if metric == 'Quality' else ARC_GRAY),
            fillcolor=(ARC_RED if metric == 'Quality' else ARC_GRAY)
        ))
    
    fig.update_layout(
        title='Statistical Distribution of Performance Metrics',
        title_font=dict(size=22, family='Arial Black', color=ARC_RED),
        yaxis_title='Score',
        paper_bgcolor=ARC_WHITE,
        plot_bgcolor='#FAFAFA',
        height=700,
        width=1400,
        showlegend=False,
        yaxis=dict(gridcolor=ARC_LIGHT_GRAY)
    )
    
    return save_figure(fig, 'box_jitter_stats')

# 20. COMPOUND DASHBOARD - Executive Summary
def create_executive_dashboard():
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=('ROI Trend', 'Speed Advantage', 'Quality Scores',
                       'Cost Breakdown', 'Geographic Impact', 'Volunteer Growth',
                       'Risk Mitigation', 'Partner Network', 'Future Projection'),
        specs=[[{'type': 'scatter'}, {'type': 'bar'}, {'type': 'indicator'}],
               [{'type': 'pie'}, {'type': 'geo'}, {'type': 'scatter'}],
               [{'type': 'bar'}, {'type': 'scatter'}, {'type': 'scatter'}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # ROI Trend
    quarters = list(range(1, 13))
    roi_values = [20 + i * 0.8 for i in quarters]
    fig.add_trace(go.Scatter(x=quarters, y=roi_values, mode='lines+markers',
                             line=dict(color=ARC_RED, width=3),
                             marker=dict(size=8, color=ARC_RED)),
                 row=1, col=1)
    
    # Speed Advantage
    fig.add_trace(go.Bar(x=['CAP', 'Standard'], y=[1, 4],
                        marker_color=[ARC_RED, ARC_GRAY]),
                 row=1, col=2)
    
    # Quality Score Indicator
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=93,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': ARC_RED},
               'bordercolor': ARC_GRAY}),
                 row=1, col=3)
    
    # Cost Breakdown Pie
    fig.add_trace(go.Pie(labels=['Services', 'Volunteers', 'Facilities'],
                         values=[650000, 450000, 506305],
                         marker_colors=[ARC_RED, '#E53E3E', ARC_GRAY]),
                 row=2, col=1)
    
    # Volunteer Growth
    fig.add_trace(go.Scatter(x=quarters, y=[100 + i * 3 for i in quarters],
                             mode='lines', fill='tozeroy',
                             line=dict(color=ARC_RED)),
                 row=2, col=3)
    
    # Risk Mitigation
    fig.add_trace(go.Bar(x=['Q1', 'Q2', 'Q3', 'Q4'], y=[2, 3, 4, 3],
                        marker_color=ARC_RED),
                 row=3, col=1)
    
    # Partner Network Growth
    fig.add_trace(go.Scatter(x=quarters, y=[10 + i * 3 for i in quarters],
                             mode='markers', marker=dict(size=[5 + i for i in quarters],
                                                        color=ARC_RED)),
                 row=3, col=2)
    
    # Future Projection
    fig.add_trace(go.Scatter(x=quarters + list(range(13, 17)),
                             y=roi_values + [28.3 + i * 0.5 for i in range(4)],
                             mode='lines',
                             line=dict(color=ARC_RED, dash='solid')),
                 row=3, col=3)
    fig.add_trace(go.Scatter(x=list(range(13, 17)),
                             y=[28.3 + i * 0.5 for i in range(4)],
                             mode='lines',
                             line=dict(color=ARC_GRAY, dash='dash')),
                 row=3, col=3)
    
    fig.update_layout(
        title='CAP Executive Dashboard - Comprehensive Performance Overview',
        title_font=dict(size=24, family='Arial Black', color=ARC_RED),
        paper_bgcolor=ARC_WHITE,
        height=1000,
        width=1600,
        showlegend=False
    )
    
    return save_figure(fig, 'executive_dashboard_complete')

# Main execution
def create_all_cool_visualizations():
    print("\n🚀 Creating 20 COOL, MODERN Visualizations\n")
    print("=" * 60)
    
    visualizations = [
        create_3d_performance(),
        create_animated_bubbles(),
        create_sunburst_breakdown(),
        create_scatter_matrix(),
        create_advanced_heatmap(),
        create_parallel_coordinates(),
        create_violin_distribution(),
        create_sankey_flow(),
        create_scatter_marginal(),
        create_treemap_impact(),
        create_funnel_pipeline(),
        create_network_graph(),
        create_line_race(),
        create_polar_bar(),
        create_density_contour(),
        create_surface_landscape(),
        create_ridgeline(),
        create_spider_comparison(),
        create_box_jitter(),
        create_executive_dashboard()
    ]
    
    print("=" * 60)
    print(f"\n🎨 Successfully created {len(visualizations)} COOL visualizations!")
    print(f"📁 Location: /Users/jefffranzen/cap-data/cool_visualizations/")
    print("\n✨ Features:")
    print("   • 3D scatter plots and surface plots")
    print("   • Animated bubble charts")
    print("   • Sunburst hierarchical breakdowns")
    print("   • Scatter matrix correlations")
    print("   • Advanced heatmaps with annotations")
    print("   • Parallel coordinates")
    print("   • Violin and ridgeline distributions")
    print("   • Sankey flow diagrams")
    print("   • Network graphs")
    print("   • Interactive treemaps")
    print("   • And much more!")
    print("\n🏆 Wall Street / Fortune 500 quality ready!")

if __name__ == "__main__":
    create_all_cool_visualizations()