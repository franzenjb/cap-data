#!/usr/bin/env python3
"""
Fortune 500 Quality CAP Evaluation Report Generator
American Red Cross - Community Adaptation Program

Creates a professional, board-ready PDF report with:
- American Red Cross branding
- Integrated visualizations
- Executive-quality layout
- Professional typography and spacing
"""

import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, red
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, Frame, PageTemplate, BaseDocTemplate, NextPageTemplate
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.units import mm
from datetime import datetime
import textwrap
import subprocess

# American Red Cross Brand Colors
ARC_RED = HexColor('#CC0000')
ARC_GRAY = HexColor('#6B7C93')
ARC_LIGHT_GRAY = HexColor('#F5F5F5')
ARC_DARK_GRAY = HexColor('#333333')

class NumberedCanvas(canvas.Canvas):
    """Canvas with page numbering and headers"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.page_num = 0

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, state) in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        """Draw page number and header"""
        if page_num == 1:  # Skip title page
            return
            
        # Header line
        self.setStrokeColor(ARC_RED)
        self.setLineWidth(2)
        self.line(72, letter[1] - 72, letter[0] - 72, letter[1] - 72)
        
        # Page number
        self.setFont("Helvetica", 10)
        self.setFillColor(ARC_GRAY)
        page_text = f"Page {page_num - 1} of {total_pages - 1}"
        self.drawRightString(letter[0] - 72, 36, page_text)
        
        # Document title in header
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(ARC_RED)
        self.drawString(72, letter[1] - 60, "CAP EVALUATION REPORT")

def create_styles():
    """Create custom paragraph styles"""
    from reportlab.lib.styles import StyleSheet1
    
    styles = StyleSheet1()
    
    # Base styles first
    styles.add(ParagraphStyle(
        name='Normal',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
    ))
    
    # Title page styles
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Normal'],
        fontSize=28,
        textColor=ARC_RED,
        alignment=TA_CENTER,
        spaceBefore=30,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=ARC_GRAY,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=30,
        fontName='Helvetica'
    ))
    
    # Section headers
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Normal'],
        fontSize=18,
        textColor=ARC_RED,
        spaceBefore=24,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=ARC_RED,
        borderPadding=8,
        backColor=ARC_LIGHT_GRAY
    ))
    
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Normal'],
        fontSize=14,
        textColor=ARC_DARK_GRAY,
        spaceBefore=18,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    # Body text
    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceBefore=6,
        spaceAfter=6,
        fontName='Helvetica'
    ))
    
    # Executive summary
    styles.add(ParagraphStyle(
        name='ExecutiveSummary',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceBefore=8,
        spaceAfter=8,
        fontName='Helvetica',
        backColor=ARC_LIGHT_GRAY,
        borderWidth=1,
        borderColor=ARC_GRAY,
        borderPadding=12
    ))
    
    # Key findings
    styles.add(ParagraphStyle(
        name='KeyFinding',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        leftIndent=20,
        bulletIndent=10,
        spaceBefore=4,
        spaceAfter=4,
        fontName='Helvetica'
    ))
    
    # Callout boxes
    styles.add(ParagraphStyle(
        name='CalloutBox',
        parent=styles['Normal'],
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        backColor=ARC_RED,
        textColor=white,
        borderWidth=2,
        borderColor=ARC_RED,
        borderPadding=15,
        spaceBefore=12,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='MetricBox',
        parent=styles['Normal'],
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        backColor=ARC_LIGHT_GRAY,
        textColor=ARC_DARK_GRAY,
        borderWidth=1,
        borderColor=ARC_GRAY,
        borderPadding=10,
        spaceBefore=8,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    return styles

def create_title_page(story, styles):
    """Create professional title page"""
    
    # Logo space (placeholder)
    story.append(Spacer(1, 1*inch))
    
    # Main title
    title = Paragraph("Community Adaptation Program<br/>Evaluation Report", styles['MainTitle'])
    story.append(title)
    
    # Subtitle
    subtitle = Paragraph("Lessons for the American Red Cross<br/>Strategic Assessment and Recommendations", styles['Subtitle'])
    story.append(subtitle)
    
    story.append(Spacer(1, 0.5*inch))
    
    # Executive summary box
    exec_summary = """
    <b>EXECUTIVE ASSESSMENT:</b><br/><br/>
    The Community Adaptation Program has delivered measurable value across four critical areas: 
    service quality enhancement, substantial cost containment, accelerated response speed, 
    and proven scalability potential. This comprehensive evaluation provides senior leadership 
    with actionable insights for strategic decisions beyond FY27.
    """
    
    story.append(Paragraph(exec_summary, styles['ExecutiveSummary']))
    
    story.append(Spacer(1, 1*inch))
    
    # Key metrics callout
    metrics_text = """
    <b>KEY PERFORMANCE INDICATORS</b><br/>
    $1.6M+ Cost Containment Achieved | 28.3% Return on Investment<br/>
    93% IA Completion Rate | 1-4 Days Faster Response Time<br/>
    35.9% Increase in Volunteer Engagement | 66.2% Increase in Homes Made Safer
    """
    story.append(Paragraph(metrics_text, styles['CalloutBox']))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Document details
    details = f"""
    <b>Prepared for:</b> American Red Cross Senior Leadership<br/>
    <b>Evaluation Period:</b> 2022 - September 2025<br/>
    <b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>
    <b>Classification:</b> Executive Strategic Assessment
    """
    
    story.append(Paragraph(details, styles['Subtitle']))
    story.append(PageBreak())

def create_toc(story, styles):
    """Create table of contents"""
    
    story.append(Paragraph("Table of Contents", styles['SectionHeader']))
    story.append(Spacer(1, 20))
    
    toc_items = [
        ("Executive Summary", "3"),
        ("Program Overview & Methodology", "5"),
        ("Disaster Relief Operations: Key Findings", "7"),
        ("Steady State Impact: The Halo Effect", "15"),
        ("Financial Analysis & Return on Investment", "18"),
        ("Challenges & Areas for Improvement", "21"),
        ("Strategic Recommendations", "24"),
        ("Implementation Roadmap", "27"),
        ("Conclusion", "29"),
        ("Appendices", "31")
    ]
    
    toc_data = []
    for item, page in toc_items:
        toc_data.append([item, page])
    
    toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, ARC_GRAY),
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())

def add_visualization(story, styles, viz_path, title, description, width=6*inch, height=4*inch):
    """Add a visualization with title and description"""
    
    story.append(Paragraph(title, styles['SubsectionHeader']))
    
    if os.path.exists(viz_path):
        try:
            img = Image(viz_path, width=width, height=height)
            img.hAlign = 'CENTER'
            story.append(img)
        except Exception as e:
            # Fallback if image doesn't load
            story.append(Paragraph(f"[Visualization: {title}]", styles['BodyText']))
    else:
        story.append(Paragraph(f"[Visualization: {title} - File not found: {viz_path}]", styles['BodyText']))
    
    if description:
        story.append(Spacer(1, 6))
        story.append(Paragraph(description, styles['BodyText']))
    
    story.append(Spacer(1, 12))

def create_executive_summary(story, styles):
    """Create executive summary with key graphics"""
    
    story.append(Paragraph("Executive Summary", styles['SectionHeader']))
    
    # Key findings overview
    exec_text = """
    The Community Adaptation Program (CAP) represents a transformative approach to disaster preparedness 
    and response, demonstrating measurable value across quality of service, cost containment, speed of 
    delivery, and scalability potential. Since its inception in 2022, CAP has proven to be a critical 
    force multiplier for American Red Cross operations.
    """
    story.append(Paragraph(exec_text, styles['BodyText']))
    
    story.append(Spacer(1, 12))
    
    # Executive dashboard
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/executive_dashboard.png",
        "CAP Performance Dashboard",
        "Comprehensive overview of CAP's impact across all key performance indicators, demonstrating consistent value delivery across multiple metrics."
    )
    
    # Key metrics in callout boxes
    story.append(Spacer(1, 12))
    
    metrics = [
        ("Quality Enhancement", "93% IA completion rate in CAP parishes vs. 67% overall"),
        ("Cost Containment", "$1.6M+ total savings with 28.3% ROI on investments"),
        ("Response Speed", "1-4 days faster service delivery in most disaster operations"),
        ("Community Impact", "35.9% increase in volunteer engagement, 66.2% increase in homes made safer")
    ]
    
    for metric_title, metric_value in metrics:
        metric_text = f"<b>{metric_title}</b><br/>{metric_value}"
        story.append(Paragraph(metric_text, styles['MetricBox']))
        story.append(Spacer(1, 6))
    
    story.append(PageBreak())

def create_methodology_section(story, styles):
    """Create methodology and program overview section"""
    
    story.append(Paragraph("Program Overview & Methodology", styles['SectionHeader']))
    
    overview_text = """
    The Community Adaptation Program employs a robust mixed-methods evaluation approach, 
    integrating quantitative performance data with qualitative insights from over 150+ 
    key informant interviews. This comprehensive methodology ensures maximum clarity and 
    value for Red Cross leadership decision-making.
    """
    story.append(Paragraph(overview_text, styles['BodyText']))
    
    story.append(Spacer(1, 12))
    
    # Methodology components
    methodology_items = [
        ("Quantitative Analysis", "Disaster Relief Operations data, cost containment reports, service delivery metrics, and steady-state program outcomes"),
        ("Qualitative Assessment", "150+ stakeholder interviews including community partners, Red Cross leadership, and disaster response staff"),
        ("Geographic Scope", "Multiple disaster operations across hurricanes, floods, tornadoes, and wildfires"),
        ("Evaluation Period", "2022 program inception through September 2025")
    ]
    
    for item_title, item_desc in methodology_items:
        story.append(Paragraph(f"<b>{item_title}:</b> {item_desc}", styles['KeyFinding']))
    
    story.append(PageBreak())

def create_dro_findings_section(story, styles):
    """Create disaster relief operations findings section"""
    
    story.append(Paragraph("Disaster Relief Operations: Key Findings", styles['SectionHeader']))
    
    # Quality of Service
    story.append(Paragraph("Quality of Service Enhancement", styles['SubsectionHeader']))
    
    quality_text = """
    CAP significantly improves disaster service quality by expanding access to vulnerable populations, 
    ensuring culturally appropriate aid, and reaching "invisible populations" often overlooked by 
    traditional response channels.
    """
    story.append(Paragraph(quality_text, styles['BodyText']))
    
    # IA Uptake visualization
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/ia_uptake.png",
        "Immediate Assistance Uptake Rates",
        "CAP jurisdictions consistently demonstrate higher IA completion rates, with Terrebonne Parish achieving 93% completion during Hurricane Francine compared to 67% overall."
    )
    
    # Speed of Response
    story.append(Paragraph("Accelerated Response Speed", styles['SubsectionHeader']))
    
    speed_text = """
    A defining characteristic of CAP is its ability to accelerate service delivery during disasters. 
    Partners are frequently "first on the ground—feeding within hours," leveraging pre-existing 
    relationships and local readiness to respond faster than centralized operations.
    """
    story.append(Paragraph(speed_text, styles['BodyText']))
    
    # Speed advantage visualization
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/speed_advantage.png",
        "Response Speed Advantage",
        "CAP partners consistently deliver first services 1-4 days faster than traditional Red Cross responses across multiple disaster operations."
    )
    
    # Key quotations callout
    quote_text = """
    <b>STAKEHOLDER VOICES:</b><br/>
    "Partners were the first on the ground—feeding within hours"<br/>
    "Hispanic population is...the invisible population. CAP partners know how to reach them"<br/>
    "Groundwork was already laid, and we've never had that before"
    """
    story.append(Paragraph(quote_text, styles['CalloutBox']))
    
    story.append(PageBreak())

def create_financial_analysis_section(story, styles):
    """Create financial analysis and ROI section"""
    
    story.append(Paragraph("Financial Analysis & Return on Investment", styles['SectionHeader']))
    
    roi_text = """
    CAP demonstrates exceptional financial value through documented cost containment and return on investment. 
    Partner contributions substantially reduce Red Cross operational costs by providing in-kind donations 
    of facilities, volunteers, meals, and supplies.
    """
    story.append(Paragraph(roi_text, styles['BodyText']))
    
    # Cost containment visualization
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/cost_containment.png",
        "Cost Containment Analysis",
        "Total documented cost containment of $1.6M+ across multiple DROs, demonstrating clear financial value to Red Cross operations."
    )
    
    # ROI by partner type
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/roi_partner_type.png",
        "Return on Investment by Partner Type",
        "Resilience Hub and Community Gateway partners show the highest ROI, with rates exceeding 30% for strategic investments."
    )
    
    # ROI by disaster type
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/roi_disaster_type.png",
        "ROI Analysis by Disaster Type",
        "Hurricane responses demonstrate the highest ROI at 37.3%, followed by flooding events at 25.5%."
    )
    
    # Financial highlights callout
    financial_highlights = """
    <b>FINANCIAL PERFORMANCE HIGHLIGHTS</b><br/>
    • Hurricane Francine: $250,000 in tracked cost containment<br/>
    • Overall Program: 28.3% Return on Investment<br/>
    • Kentucky Storms: $670,000 in feeding cost offsets<br/>
    • Consistent cost reduction across all disaster types
    """
    story.append(Paragraph(financial_highlights, styles['CalloutBox']))
    
    story.append(PageBreak())

def create_halo_effect_section(story, styles):
    """Create steady state impacts section"""
    
    story.append(Paragraph("Steady State Impact: The Halo Effect", styles['SectionHeader']))
    
    halo_text = """
    Beyond immediate disaster response, CAP demonstrates significant "Halo Effect" impacts, 
    contributing to broader community resilience and enhancing American Red Cross mission 
    effectiveness during non-disaster periods.
    """
    story.append(Paragraph(halo_text, styles['BodyText']))
    
    # Volunteer trends
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/volunteer_trends.png",
        "Volunteer Engagement Growth",
        "CAP jurisdictions show 35.92% increase in volunteer engagement compared to 16.05% national average, demonstrating enhanced community mobilization."
    )
    
    # Homes made safer
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/homes_safer.png",
        "Homes Made Safer Initiative Impact",
        "CAP jurisdictions achieved 66.24% increase in homes made safer compared to 14.02% national increase, showing enhanced preparedness outcomes."
    )
    
    # Stakeholder sentiment
    add_visualization(
        story, styles,
        "/Users/jefffranzen/cap-data/graphics/stakeholder_sentiment.png",
        "Stakeholder Sentiment Analysis",
        "Overwhelmingly positive sentiment from community partners and stakeholders, with 97% reporting improved disaster service capability."
    )
    
    story.append(PageBreak())

def create_challenges_section(story, styles):
    """Create challenges and limitations section"""
    
    story.append(Paragraph("Challenges & Areas for Improvement", styles['SectionHeader']))
    
    challenges_text = """
    While CAP demonstrates significant value, the evaluation transparently identifies areas 
    for improvement and potential risks that must be addressed for future success.
    """
    story.append(Paragraph(challenges_text, styles['BodyText']))
    
    challenges = [
        ("Integration Gaps", "CAP often perceived as separate from Disaster Services, leading to confusion and occasional resentment among Red Cross staff"),
        ("Reporting Shortfalls", "Inconsistent documentation of cost savings and activities, with acknowledgment that '100% not everything got reported'"),
        ("Scalability Concerns", "Current dedicated three-person team model not sustainable nationwide due to resource limitations"),
        ("Uneven Engagement", "Hyper-local focus can lead to geographic blind spots and uneven partner engagement across regions")
    ]
    
    for challenge_title, challenge_desc in challenges:
        story.append(Paragraph(f"<b>{challenge_title}:</b> {challenge_desc}", styles['KeyFinding']))
    
    story.append(Spacer(1, 12))
    
    # Transparency callout
    transparency_text = """
    <b>EVALUATION TRANSPARENCY</b><br/>
    This evaluation acknowledges limitations including potential selection bias, 
    confounding factors, and measurement challenges while maintaining confidence 
    in the overall positive impact demonstrated by CAP.
    """
    story.append(Paragraph(transparency_text, styles['MetricBox']))
    
    story.append(PageBreak())

def create_recommendations_section(story, styles):
    """Create strategic recommendations section"""
    
    story.append(Paragraph("Strategic Recommendations", styles['SectionHeader']))
    
    rec_intro = """
    Based on comprehensive evaluation findings, the following strategic recommendations 
    provide actionable pathways for integrating CAP's successful principles into broader 
    Red Cross operations while addressing identified challenges.
    """
    story.append(Paragraph(rec_intro, styles['BodyText']))
    
    recommendations = [
        ("Invest in Blue-Sky Relationships", "Prioritize ongoing relationship-building with hyper-local partners before disasters strike to build trust and accelerate response"),
        ("Leverage Local Credibility", "Use local nonprofits as trusted messengers to reach vulnerable groups and integrate into existing community structures"),
        ("Enhance Cultural Access", "Partner with organizations providing culturally competent services, language translation, and trusted community connections"),
        ("Shift to Network Builder Role", "Reframe Red Cross role to focus on enabling local resilience rather than solely delivering aid"),
        ("Clarify Roles and Train Staff", "Define clear responsibilities and train Red Cross staff in partnership management with early deployment to leadership tables"),
        ("Document Cost Savings", "Implement mandatory cost capture mechanisms and establish streamlined reporting channels"),
        ("Plan for Continuity", "Design exit strategies that enable partners to continue recovery efforts beyond direct Red Cross engagement"),
        ("Expand Community Grants", "Increase investment in modest community grants and equipment enhancements to unlock partner throughput"),
        ("Formalize Asset Management", "Preposition blue-sky assets at resilience hubs under formal MOUs with maintenance schedules"),
        ("Institutionalize Liaison Role", "Ensure CAP liaisons have empowered seats at leadership tables with proper training and system access")
    ]
    
    for i, (rec_title, rec_desc) in enumerate(recommendations, 1):
        story.append(Paragraph(f"<b>{i}. {rec_title}:</b> {rec_desc}", styles['KeyFinding']))
        story.append(Spacer(1, 6))
    
    story.append(PageBreak())

def create_implementation_section(story, styles):
    """Create implementation roadmap section"""
    
    story.append(Paragraph("Implementation Roadmap", styles['SectionHeader']))
    
    implementation_text = """
    The transition from dedicated CAP teams to integrated partnership management requires 
    strategic planning and phased implementation to preserve program benefits while 
    achieving sustainable scalability.
    """
    story.append(Paragraph(implementation_text, styles['BodyText']))
    
    # Implementation phases
    phases = [
        ("Phase 1: Foundation (0-6 months)", "Establish partnership management protocols, develop training materials, and create integration frameworks"),
        ("Phase 2: Pilot Integration (6-12 months)", "Test integrated model in select regions, refine processes, and document lessons learned"),
        ("Phase 3: Scaled Deployment (12-24 months)", "Roll out integrated partnership management across all regions with dedicated liaison support"),
        ("Phase 4: Full Integration (24+ months)", "Complete transition to embedded partnership capabilities within standard Red Cross operations")
    ]
    
    for phase_title, phase_desc in phases:
        story.append(Paragraph(f"<b>{phase_title}:</b> {phase_desc}", styles['KeyFinding']))
        story.append(Spacer(1, 8))
    
    # Success metrics callout
    success_metrics = """
    <b>SUCCESS METRICS FOR IMPLEMENTATION</b><br/>
    • Maintain or improve current ROI performance (>25%)<br/>
    • Sustain response speed advantages (1-4 day improvement)<br/>
    • Preserve quality enhancements (IA uptake rates >90%)<br/>
    • Achieve cost-neutral integration within 18 months
    """
    story.append(Paragraph(success_metrics, styles['CalloutBox']))
    
    story.append(PageBreak())

def create_conclusion_section(story, styles):
    """Create conclusion section"""
    
    story.append(Paragraph("Conclusion", styles['SectionHeader']))
    
    conclusion_text = """
    The Community Adaptation Program evaluation reveals a compelling narrative of success: 
    CAP is a well-loved and widely valued program that delivers measurable operational and 
    strategic benefits to the American Red Cross. Through trusted hyperlocal partnerships, 
    modest pre-event investments, and embedded liaison integration, CAP has demonstrably 
    achieved its core objectives.
    """
    story.append(Paragraph(conclusion_text, styles['BodyText']))
    
    story.append(Spacer(1, 12))
    
    key_achievements = """
    <b>Key Achievements:</b><br/>
    • Significantly accelerated initial aid delivery with partners often first on the ground<br/>
    • Improved service quality by expanding reach to "invisible populations"<br/>
    • Generated meaningful cost containment with 28.3% ROI and $1.6M+ savings<br/>
    • Enhanced Red Cross reputation and steady-state program outcomes<br/>
    • Provided critical buffer against brand risk through localized service delivery
    """
    story.append(Paragraph(key_achievements, styles['BodyText']))
    
    story.append(Spacer(1, 12))
    
    final_recommendation = """
    <b>STRATEGIC RECOMMENDATION</b><br/>
    CAP should be continued and strategically adapted as a force multiplier for 
    disaster operations and community mobilization. The program represents more than 
    an initiative—it embodies a strategic shift towards community-centered humanitarian 
    services essential for the Red Cross's mission in FY27 and beyond.
    """
    story.append(Paragraph(final_recommendation, styles['CalloutBox']))
    
    story.append(PageBreak())

def create_appendices_section(story, styles):
    """Create appendices section"""
    
    story.append(Paragraph("Appendices", styles['SectionHeader']))
    
    appendices = [
        ("Appendix A", "Detailed Financial Analysis", "Complete ROI calculations, cost containment reports, and partner quarterly data"),
        ("Appendix B", "Case Study Vignettes", "In-depth stories from Terrebonne Parish, Madison County, Warren County, and Hurricane responses"),
        ("Appendix C", "Stakeholder Voices", "De-identified quotations organized by themes with sentiment analysis findings"),
        ("Appendix D", "Evaluation Framework", "Detailed methodology, interview process, and analytical tools used"),
        ("Appendix E", "Implementation Tools", "Templates, training materials, and integration guidelines for replication")
    ]
    
    for app_letter, app_title, app_desc in appendices:
        story.append(Paragraph(f"<b>{app_letter}: {app_title}</b>", styles['SubsectionHeader']))
        story.append(Paragraph(app_desc, styles['BodyText']))
        story.append(Spacer(1, 12))

def create_pdf_report():
    """Main function to create the Fortune 500 quality PDF report"""
    
    print("Creating Fortune 500 quality CAP Evaluation Report...")
    
    # Setup document
    output_path = "/Users/jefffranzen/cap-data/CAP_Evaluation_Report_Fortune500.pdf"
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=1*inch,
        bottomMargin=1*inch,
        leftMargin=1*inch,
        rightMargin=1*inch
    )
    
    # Create custom styles
    styles = create_styles()
    
    # Build document content
    story = []
    
    # Title page
    create_title_page(story, styles)
    
    # Table of contents
    create_toc(story, styles)
    
    # Executive summary with key graphics
    create_executive_summary(story, styles)
    
    # Methodology section
    create_methodology_section(story, styles)
    
    # DRO findings with visualizations
    create_dro_findings_section(story, styles)
    
    # Financial analysis with ROI charts
    create_financial_analysis_section(story, styles)
    
    # Halo effect with steady state impacts
    create_halo_effect_section(story, styles)
    
    # Challenges and limitations
    create_challenges_section(story, styles)
    
    # Strategic recommendations
    create_recommendations_section(story, styles)
    
    # Implementation roadmap
    create_implementation_section(story, styles)
    
    # Conclusion
    create_conclusion_section(story, styles)
    
    # Appendices
    create_appendices_section(story, styles)
    
    # Build PDF with custom canvas
    print("Building PDF document...")
    doc.build(story, canvasmaker=NumberedCanvas)
    
    print(f"Fortune 500 quality PDF report created successfully!")
    print(f"Location: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
    
    return output_path

if __name__ == "__main__":
    try:
        pdf_path = create_pdf_report()
        
        # Try to open the PDF (macOS)
        try:
            subprocess.run(['open', pdf_path], check=True)
            print("PDF opened successfully!")
        except subprocess.CalledProcessError:
            print("PDF created but could not auto-open. Please open manually.")
            
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        sys.exit(1)