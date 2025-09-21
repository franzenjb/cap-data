#!/usr/bin/env python3
"""
Create a professionally formatted PDF of the CAP Evaluation Report
with integrated graphics and call-out boxes
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, KeepTogether, Image
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
import plotly.graph_objects as go
import plotly.io as pio
import os
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
        }
        
        # Calculate dimensions
        self.width = 5 * inch
        self.height = self._calculate_height()
    
    def _calculate_height(self):
        # Estimate height based on content length
        lines = len(self.content) / 50  # Rough estimate
        return max(1.5 * inch, (0.5 + lines * 0.2) * inch)
    
    def draw(self):
        # Draw the box
        self.canv.setStrokeColor(self.colors.get(self.box_type, colors.black))
        self.canv.setLineWidth(2)
        self.canv.rect(0, 0, self.width, self.height)
        
        # Draw the title background
        self.canv.setFillColor(self.colors.get(self.box_type, colors.black))
        self.canv.rect(0, self.height - 0.35*inch, self.width, 0.35*inch, fill=1)
        
        # Draw the title text
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawCentredString(self.width/2, self.height - 0.25*inch, self.title)
        
        # Draw the content
        self.canv.setFillColor(colors.black)
        self.canv.setFont("Helvetica", 10)
        
        # Wrap text manually
        y_position = self.height - 0.6*inch
        words = self.content.split()
        line = ""
        line_width = 0
        max_width = self.width - 0.4*inch
        
        for word in words:
            test_line = line + " " + word if line else word
            test_width = self.canv.stringWidth(test_line, "Helvetica", 10)
            
            if test_width < max_width:
                line = test_line
                line_width = test_width
            else:
                if line:
                    self.canv.drawCentredString(self.width/2, y_position, line)
                    y_position -= 0.2*inch
                line = word
                line_width = self.canv.stringWidth(word, "Helvetica", 10)
        
        if line:
            self.canv.drawCentredString(self.width/2, y_position, line)

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
        
        # Header
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor('#6B7C93'))
        self.drawString(1*inch, letter[1] - 0.5*inch, 
                       "Community Adaptation Program Evaluation Report")
        self.drawRightString(letter[0] - 1*inch, letter[1] - 0.5*inch,
                            datetime.now().strftime("%B %Y"))
        
        # Page number
        self.drawCentredString(letter[0]/2, 0.5*inch,
                              f"Page {self._pageNumber} of {page_count}")
        
        # Red line under header
        self.setStrokeColor(colors.HexColor('#CC0000'))
        self.setLineWidth(2)
        self.line(1*inch, letter[1] - 0.6*inch, letter[0] - 1*inch, letter[1] - 0.6*inch)
        
        self.restoreState()

def create_professional_pdf():
    """Main function to create the PDF report"""
    
    # Create output directory
    os.makedirs('/Users/jefffranzen/cap-data/output', exist_ok=True)
    
    # Set up the document
    pdf_file = '/Users/jefffranzen/cap-data/output/CAP_Evaluation_Report_Professional.pdf'
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
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
        fontSize=24,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=30,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=12,
        spaceBefore=24,
        keepWithNext=True
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
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['CustomBody'],
        leftIndent=20,
        bulletIndent=10
    ))
    
    # Title Page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph(
        "Community Adaptation Program (CAP)<br/>Evaluation Report",
        styles['CustomTitle']
    ))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(
        "Lessons for the American Red Cross",
        styles['Heading2']
    ))
    elements.append(Spacer(1, 1*inch))
    
    # Subtitle info
    elements.append(Paragraph(
        "Prepared for American Red Cross Leadership<br/>September 30, 2025",
        styles['Normal']
    ))
    
    elements.append(PageBreak())
    
    # Executive Summary with Call-out Boxes
    elements.append(Paragraph("Executive Summary", styles['SectionHeader']))
    
    # Add key metric callout
    elements.append(CalloutBox(
        "KEY METRIC",
        "150+ INTERVIEWS - Comprehensive evaluation based on extensive stakeholder engagement across 8 major disasters",
        'metric'
    ))
    elements.append(Spacer(1, 0.25*inch))
    
    # Read the report content
    with open('/Users/jefffranzen/cap-data/Updated_CAP_Report_September_30_2025_COMPLETE.txt', 'r') as f:
        content = f.read()
    
    # Parse sections
    sections = content.split('\n\n')
    
    # Process executive summary
    exec_summary_found = False
    for section in sections:
        if 'Executive Summary' in section and not exec_summary_found:
            exec_summary_found = True
            # Skip the title line
            lines = section.split('\n')[1:]
            for line in lines[:10]:  # First part of exec summary
                if line.strip():
                    elements.append(Paragraph(line, styles['CustomBody']))
    
    # Add ROI callout
    elements.append(Spacer(1, 0.25*inch))
    elements.append(CalloutBox(
        "RETURN ON INVESTMENT",
        "$1.6M IN COST CONTAINMENT - 28.3% ROI on $5.67M partner investment",
        'success'
    ))
    elements.append(Spacer(1, 0.25*inch))
    
    # Convert and add first graphic
    elements.append(Paragraph("Figure 1: Return on Investment Analysis", styles['Normal']))
    
    # Create ROI comparison chart as PNG
    import create_cap_graphics
    fig = create_cap_graphics.create_roi_comparison()
    img_path = '/Users/jefffranzen/cap-data/output/roi_comparison.png'
    pio.write_image(fig, img_path, width=600, height=400, scale=2)
    
    if os.path.exists(img_path):
        img = Image(img_path, width=5*inch, height=3.33*inch)
        elements.append(img)
    
    elements.append(PageBreak())
    
    # Key Findings Section
    elements.append(Paragraph("Key Findings", styles['SectionHeader']))
    
    # Quality of Service
    elements.append(Paragraph("Quality of Service", styles['SubsectionHeader']))
    elements.append(CalloutBox(
        "REACHING THE INVISIBLE",
        "Hispanic population is...the invisible population. CAP partners know how to reach them. - Community Stakeholder",
        'quote'
    ))
    elements.append(Spacer(1, 0.25*inch))
    
    # Find and add quality section content
    for section in sections:
        if 'Quality of Service:' in section:
            lines = section.split('\n')
            for line in lines[1:8]:  # Get key points
                if line.strip() and '•' in line:
                    elements.append(Paragraph(line, styles['BulletText']))
                elif line.strip():
                    elements.append(Paragraph(line, styles['CustomBody']))
    
    # Add Speed Comparison graphic
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph("Figure 2: Speed of Service Delivery", styles['Normal']))
    fig2 = create_cap_graphics.create_speed_comparison()
    img_path2 = '/Users/jefffranzen/cap-data/output/speed_comparison.png'
    pio.write_image(fig2, img_path2, width=600, height=400, scale=2)
    
    if os.path.exists(img_path2):
        img2 = Image(img_path2, width=5*inch, height=3.33*inch)
        elements.append(img2)
    
    elements.append(PageBreak())
    
    # Cost Containment Section
    elements.append(Paragraph("Cost Containment", styles['SubsectionHeader']))
    elements.append(CalloutBox(
        "DIRECT SUBSTITUTION",
        "I did not pay a dime for feeding - DRO Leadership, Tennessee Tornados",
        'quote'
    ))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add cost breakdown graphic
    elements.append(Paragraph("Figure 3: Cost Containment Breakdown", styles['Normal']))
    fig3 = create_cap_graphics.create_cost_breakdown()
    img_path3 = '/Users/jefffranzen/cap-data/output/cost_breakdown.png'
    pio.write_image(fig3, img_path3, width=600, height=400, scale=2)
    
    if os.path.exists(img_path3):
        img3 = Image(img_path3, width=5*inch, height=3.33*inch)
        elements.append(img3)
    
    elements.append(PageBreak())
    
    # Recommendations Section
    elements.append(Paragraph("Strategic Recommendations", styles['SectionHeader']))
    elements.append(CalloutBox(
        "PRIORITY ACTIONS",
        "TOP 3: 1. Invest in Blue-Sky Relationships 2. Formalize MOUs 3. Institutionalize CAP Liaison Role",
        'priority'
    ))
    
    # Build the PDF
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    print(f"Professional PDF created: {pdf_file}")
    return pdf_file

# Create the PDF
if __name__ == "__main__":
    # First ensure we have the graphics module
    import sys
    sys.path.append('/Users/jefffranzen/cap-data')
    
    pdf_path = create_professional_pdf()
    print(f"\nPDF successfully created at: {pdf_path}")
    print("\nThe PDF includes:")
    print("• Professional layout with Red Cross branding colors")
    print("• Integrated call-out boxes for key metrics")
    print("• Data visualizations as embedded graphics")
    print("• Page numbers and headers")
    print("• Formatted sections with proper typography")