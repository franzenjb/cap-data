#!/usr/bin/env python3
"""
Create a professionally formatted PDF of the CAP Evaluation Report
Simplified version without image dependencies
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, KeepTogether
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import re

class CalloutBox(Flowable):
    """Custom flowable for professional call-out boxes"""
    def __init__(self, title, content, box_type='metric'):
        Flowable.__init__(self)
        self.title = title
        self.content = content
        self.box_type = box_type
        
        # Define colors for different box types
        self.colors = {
            'metric': colors.HexColor('#CC0000'),  # Red Cross red
            'quote': colors.HexColor('#6B7C93'),   # Gray
            'success': colors.HexColor('#4CAF50'),  # Green
            'priority': colors.HexColor('#FF6B35'), # Orange
            'speed': colors.HexColor('#2196F3'),    # Blue
        }
        
        # Calculate dimensions
        self.width = 5.5 * inch
        self.height = self._calculate_height()
    
    def _calculate_height(self):
        # Better height calculation
        char_count = len(self.content)
        if char_count < 50:
            return 1.0 * inch
        elif char_count < 100:
            return 1.3 * inch
        elif char_count < 150:
            return 1.6 * inch
        else:
            return 2.0 * inch
    
    def draw(self):
        # Draw the box with rounded corners effect
        color = self.colors.get(self.box_type, colors.black)
        self.canv.setStrokeColor(color)
        self.canv.setLineWidth(2)
        
        # Main box
        self.canv.rect(0, 0, self.width, self.height)
        
        # Title bar
        self.canv.setFillColor(color)
        self.canv.rect(0, self.height - 0.35*inch, self.width, 0.35*inch, fill=1)
        
        # Title text
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 11)
        self.canv.drawCentredString(self.width/2, self.height - 0.23*inch, self.title)
        
        # Content - better text wrapping
        self.canv.setFillColor(colors.black)
        self.canv.setFont("Helvetica", 9)
        
        # Split content into lines
        max_chars_per_line = 65
        lines = []
        words = self.content.split()
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                current_line = current_line + " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        y_position = self.height - 0.55*inch
        for line in lines:
            if y_position > 0.2*inch:
                self.canv.drawCentredString(self.width/2, y_position, line.strip())
                y_position -= 0.18*inch

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers and headers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
    
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    
    def save(self):
        """Add page numbers and headers"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    
    def draw_page_number(self, page_count):
        """Draw page numbers and header"""
        self.saveState()
        
        # Skip header/footer on first page
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#6B7C93'))
            self.drawString(1*inch, letter[1] - 0.5*inch, 
                           "Community Adaptation Program Evaluation Report")
            self.drawRightString(letter[0] - 1*inch, letter[1] - 0.5*inch,
                                "September 2025")
            
            # Red line under header
            self.setStrokeColor(colors.HexColor('#CC0000'))
            self.setLineWidth(1)
            self.line(1*inch, letter[1] - 0.55*inch, letter[0] - 1*inch, letter[1] - 0.55*inch)
        
        # Page number (all pages except first)
        if self._pageNumber > 1:
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor('#6B7C93'))
            self.drawCentredString(letter[0]/2, 0.5*inch,
                                  f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()

def create_data_table(title, data_rows):
    """Create a formatted data table"""
    table_data = [[title]] + data_rows
    
    table = Table(table_data, colWidths=[3*inch, 2*inch])
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CC0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ]))
    
    return table

def create_professional_pdf():
    """Main function to create the PDF report"""
    
    # Set up the document
    pdf_file = '/Users/jefffranzen/cap-data/CAP_Evaluation_Report_Professional.pdf'
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch,
        title="Community Adaptation Program Evaluation Report",
        author="American Red Cross"
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=26,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=32
    ))
    
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#6B7C93'),
        alignment=TA_CENTER,
        spaceAfter=12
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=12,
        spaceBefore=24,
        keepWithNext=True,
        leftIndent=0
    ))
    
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#6B7C93'),
        spaceAfter=6,
        spaceBefore=12,
        keepWithNext=True
    ))
    
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=13
    ))
    
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['CustomBody'],
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6
    ))
    
    # Title Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph(
        "<b>Community Adaptation Program</b><br/>Evaluation Report",
        styles['CustomTitle']
    ))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(
        "Comprehensive Assessment of Impact and Value",
        styles['CustomSubtitle']
    ))
    elements.append(Spacer(1, 1.5*inch))
    
    # Subtitle info
    elements.append(Paragraph(
        "<b>Prepared for:</b> American Red Cross Leadership",
        styles['Normal']
    ))
    elements.append(Paragraph(
        "<b>Date:</b> September 30, 2025",
        styles['Normal']
    ))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        "<b>Evaluation Period:</b> FY2023 - FY2025<br/>" +
        "<b>Interviews Conducted:</b> 150+<br/>" + 
        "<b>Disasters Analyzed:</b> 8 Major Events",
        styles['Normal']
    ))
    
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Key Metrics Callout
    elements.append(CalloutBox(
        "📊 KEY EVALUATION METRICS",
        "150+ INTERVIEWS conducted across 8 major disasters providing comprehensive stakeholder insights",
        'metric'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Read the report content
    with open('/Users/jefffranzen/cap-data/Updated_CAP_Report_September_30_2025_COMPLETE.txt', 'r') as f:
        full_content = f.read()
    
    # Extract executive summary content
    exec_summary_start = full_content.find("The Community Adaptation Program (CAP)")
    exec_summary_end = full_content.find("Key Findings:")
    
    if exec_summary_start > 0 and exec_summary_end > 0:
        exec_text = full_content[exec_summary_start:exec_summary_end].strip()
        elements.append(Paragraph(exec_text, styles['CustomBody']))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ROI Callout
    elements.append(CalloutBox(
        "💰 RETURN ON INVESTMENT",
        "$1.6M IN COST CONTAINMENT - 28.3% ROI on $5.67M partner investment",
        'success'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Speed Callout
    elements.append(CalloutBox(
        "⚡ SPEED ADVANTAGE",
        "1-4 DAYS FASTER - CAP partners consistently outpace centralized Red Cross operations",
        'speed'
    ))
    
    elements.append(PageBreak())
    
    # Key Findings
    elements.append(Paragraph("KEY FINDINGS", styles['SectionHeader']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Quality of Service Section
    elements.append(Paragraph("1. Quality of Service", styles['SubsectionHeader']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(CalloutBox(
        "👥 REACHING THE INVISIBLE",
        "Hispanic population is...the invisible population. CAP partners know how to reach them. - Community Stakeholder",
        'quote'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    quality_text = """
    CAP partners have demonstrably improved the quality of Red Cross disaster services by expanding 
    access, ensuring cultural appropriateness, and accelerating aid delivery. Key achievements include:
    """
    elements.append(Paragraph(quality_text, styles['CustomBody']))
    
    quality_points = [
        "• <b>Adapted Meals:</b> Culturally sensitive foods provided in Latino and farming communities",
        "• <b>Bilingual Support:</b> Crucial translation services where Red Cross staff lacked language capacity",
        "• <b>Trusted Messengers:</b> Local leaders like pastors used to overcome literacy and connectivity challenges",
        "• <b>93% IA Completion Rate</b> in Terrebonne Parish (Hurricane Francine) vs. 67% overall rate",
        "• <b>58.3% IA Pick-up Rate</b> in South Texas Floods vs. 51% nationwide average"
    ]
    
    for point in quality_points:
        elements.append(Paragraph(point, styles['BulletText']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Create ROI data table
    roi_table = create_data_table(
        "Return on Investment by Partner Type",
        [
            ["Resilience Hubs", "33.48%"],
            ["Community Gateways", "30.11%"],
            ["Hunger Partners", "26.33%"],
            ["Overall Program ROI", "28.30%"]
        ]
    )
    elements.append(roi_table)
    
    elements.append(PageBreak())
    
    # Cost Containment Section
    elements.append(Paragraph("2. Cost Containment", styles['SubsectionHeader']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(CalloutBox(
        "💵 DIRECT SUBSTITUTION",
        "I did not pay a dime for feeding - DRO Leadership, Tennessee Tornados",
        'quote'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    cost_text = """
    The Community Adaptation Program has demonstrably reduced Red Cross operational costs through 
    partner contributions of in-kind donations and services. Total documented savings exceed $1.6 million.
    """
    elements.append(Paragraph(cost_text, styles['CustomBody']))
    
    # Cost breakdown table
    cost_table = create_data_table(
        "Cost Containment Breakdown (FY23-FY25)",
        [
            ["Hurricane Francine", "$243,237"],
            ["Tennessee Tornados", "$80,000-100,000"],
            ["Kentucky Floods", "$125,000+"],
            ["Other DROs", "$1,157,768"],
            ["Total Documented Savings", "$1,606,305"]
        ]
    )
    elements.append(cost_table)
    
    elements.append(PageBreak())
    
    # Speed of Delivery Section
    elements.append(Paragraph("3. Speed of Delivery", styles['SubsectionHeader']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(CalloutBox(
        "⏱️ RAPID MOBILIZATION",
        "First on the ground—feeding within hours. Partners activate same-day or next-day",
        'speed'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    speed_text = """
    CAP's ability to remarkably accelerate service delivery is a consistent finding across all 
    evaluated disasters. This speed advantage results from pre-existing relationships and local readiness.
    """
    elements.append(Paragraph(speed_text, styles['CustomBody']))
    
    # Speed comparison table
    speed_table = create_data_table(
        "Days Faster Than Red Cross (First DES Delivery)",
        [
            ["Kentucky Floods", "4 days faster"],
            ["Tennessee Tornados", "3 days faster"],
            ["MO/AR Storms", "1 day faster"],
            ["Hurricane Francine", "Same day activation"],
            ["Average Advantage", "1-4 days faster"]
        ]
    )
    elements.append(speed_table)
    
    elements.append(PageBreak())
    
    # Halo Effect Section
    elements.append(Paragraph("4. Halo Effect - Steady State Impacts", styles['SubsectionHeader']))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(CalloutBox(
        "📈 VOLUNTEER SURGE",
        "+35.92% INCREASE in volunteer engagement in CAP jurisdictions vs. +16.05% national average",
        'success'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    halo_text = """
    Beyond disaster response, CAP generates significant positive spillover effects during non-disaster 
    periods through coalition-building and establishing rural trust.
    """
    elements.append(Paragraph(halo_text, styles['CustomBody']))
    
    halo_points = [
        "• <b>Volunteer Engagement:</b> +35.92% increase in CAP jurisdictions vs. +16.05% nationally",
        "• <b>Homes Made Safer:</b> +66.24% increase in CAP areas vs. +14.02% national average",
        "• <b>Youth Preparedness:</b> +101.23% increase vs. +39.13% national average",
        "• <b>Brand Protection:</b> 12 service delivery failures prevented or resolved in FY25",
        "• <b>Partner Satisfaction:</b> 97% report improved disaster response capability"
    ]
    
    for point in halo_points:
        elements.append(Paragraph(point, styles['BulletText']))
    
    elements.append(PageBreak())
    
    # Strategic Recommendations
    elements.append(Paragraph("STRATEGIC RECOMMENDATIONS", styles['SectionHeader']))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(CalloutBox(
        "🎯 TOP 3 PRIORITY ACTIONS",
        "1. Invest in Blue-Sky Relationships  2. Formalize MOUs & Asset Management  3. Institutionalize CAP Liaison Role",
        'priority'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    rec_text = """
    Based on comprehensive evaluation findings, the following strategic recommendations will maximize 
    CAP's impact and ensure sustainable integration into Red Cross operations:
    """
    elements.append(Paragraph(rec_text, styles['CustomBody']))
    
    recommendations = [
        "• <b>Immediate (0-6 months):</b> Formalize partnership agreements and establish tracking systems",
        "• <b>Short-term (6-12 months):</b> Develop regional partnership management positions",
        "• <b>Long-term (12+ months):</b> Integrate CAP principles into standard chapter operations",
        "• <b>Continuous:</b> Maintain blue-sky relationship building and partner capacity development"
    ]
    
    for rec in recommendations:
        elements.append(Paragraph(rec, styles['BulletText']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    elements.append(Paragraph("CONCLUSION", styles['SectionHeader']))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(CalloutBox(
        "🏆 OVERALL VERDICT",
        "CAP: A STRATEGIC SHIFT from service delivery to community-centered humanitarian services",
        'success'
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    conclusion_text = """
    The Community Adaptation Program represents a fundamental evolution in how the American Red Cross 
    engages with communities before, during, and after disasters. With demonstrated returns across 
    quality, cost, speed, and community engagement metrics, CAP should be continued and strategically 
    adapted as a force multiplier for disaster operations. The program's success in building trusted 
    local networks, achieving measurable cost savings, and improving service delivery speed validates 
    its essential role for FY27 and beyond.
    """
    elements.append(Paragraph(conclusion_text, styles['CustomBody']))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(CalloutBox(
        "🌟 FUTURE VISION",
        "ESSENTIAL FOR FY27 AND BEYOND - Critical disaster tool + Powerful steady-state mobilization asset",
        'metric'
    ))
    
    # Build the PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    return pdf_file

# Create the PDF
if __name__ == "__main__":
    try:
        pdf_path = create_professional_pdf()
        print(f"\n✅ Professional PDF successfully created!")
        print(f"📄 Location: {pdf_path}")
        print("\n📊 The PDF includes:")
        print("  • Executive summary with key metrics")
        print("  • Professional call-out boxes throughout")
        print("  • Data tables for ROI, cost savings, and speed metrics")
        print("  • Strategic recommendations section")
        print("  • Red Cross branded colors and formatting")
        print("  • Page numbers and professional headers")
        print("\n🎯 Ready for presentation to ARC Leadership")
    except Exception as e:
        print(f"Error creating PDF: {e}")