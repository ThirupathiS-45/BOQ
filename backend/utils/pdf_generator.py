"""
PDF generation utility for BOQ reports with floor plan images.
Generates professional PDF documents with project details, floor plan, BOQ, and cost breakdown.
"""

import io
import base64
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white, black, grey
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    KeepTogether,
)
from PIL import Image as PILImage


class PDFGenerator:
    """Generate professional PDF reports with floor plan and cost breakdowns."""

    def __init__(self):
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF."""
        # Title style
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=HexColor("#1e40af"),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Heading style
        self.styles.add(
            ParagraphStyle(
                name="CustomHeading",
                parent=self.styles["Heading2"],
                fontSize=14,
                textColor=HexColor("#1e40af"),
                spaceAfter=12,
                spaceBefore=12,
                fontName="Helvetica-Bold",
            )
        )

        # Subheading style
        self.styles.add(
            ParagraphStyle(
                name="CustomSubHeading",
                parent=self.styles["Heading3"],
                fontSize=11,
                textColor=HexColor("#1e3a8a"),
                spaceAfter=8,
                spaceBefore=8,
            )
        )

        # Body style
        self.styles.add(
            ParagraphStyle(
                name="CustomBody",
                parent=self.styles["BodyText"],
                fontSize=10,
                alignment=TA_JUSTIFY,
                spaceAfter=8,
            )
        )

    def _base64_to_image(self, base64_str: str) -> Optional[bytes]:
        """Convert base64 data URL to image bytes."""
        try:
            if "," in base64_str:
                # Data URL format: data:image/png;base64,...
                base64_str = base64_str.split(",")[1]
            return base64.b64decode(base64_str)
        except Exception as e:
            print(f"Error converting base64 to image: {e}")
            return None

    def _create_floor_plan_image(self, floor_plan_base64: str, width: float = 5 * inch, height: float = 5 * inch) -> Optional[Image]:
        """Create an Image object from base64 floor plan data."""
        try:
            image_bytes = self._base64_to_image(floor_plan_base64)
            if not image_bytes:
                return None

            # Save to temporary bytes buffer
            img_buffer = io.BytesIO(image_bytes)
            
            # Open with PIL to get dimensions
            pil_img = PILImage.open(img_buffer)
            pil_img.load()
            
            # Reset buffer
            img_buffer.seek(0)
            
            # Create reportlab Image
            img = Image(img_buffer, width=width, height=height)
            return img
        except Exception as e:
            print(f"Error creating floor plan image: {e}")
            return None

    def _create_header(self, project_description: str) -> list:
        """Create header section with title and description."""
        elements = []

        # Title
        title = Paragraph("BOQ Report", self.styles["CustomTitle"])
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))

        # Generation date
        date_text = f"Generated on {datetime.now().strftime('%d %B %Y at %H:%M')}"
        date_para = Paragraph(date_text, self.styles["Normal"])
        elements.append(date_para)
        elements.append(Spacer(1, 0.3 * inch))

        # Project Description
        if project_description:
            desc_heading = Paragraph("Project Description", self.styles["CustomHeading"])
            elements.append(desc_heading)
            desc_para = Paragraph(project_description, self.styles["CustomBody"])
            elements.append(desc_para)
            elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_floor_plan_section(self, floor_plan_base64: str) -> list:
        """Create floor plan section."""
        elements = []

        heading = Paragraph("Floor Plan", self.styles["CustomHeading"])
        elements.append(heading)

        img = self._create_floor_plan_image(floor_plan_base64, width=5.5 * inch, height=5.5 * inch)
        if img:
            elements.append(img)
        else:
            elements.append(Paragraph("Floor plan image could not be displayed", self.styles["Normal"]))

        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_boq_table(self, boq_data: Dict[str, Any], cost_data: Dict[str, Any]) -> list:
        """Create Bill of Quantities table."""
        elements = []

        heading = Paragraph("Bill of Quantities (BOQ)", self.styles["CustomHeading"])
        elements.append(heading)

        # Prepare table data
        table_data = [
            ["Material Item", "Quantity", "Unit", "Rate", "Total Cost"]
        ]

        # Add BOQ items
        if isinstance(boq_data, dict):
            for item_name, cost in boq_data.items():
                if isinstance(cost, (int, float)):
                    # Format item name
                    item_display = item_name.replace("_", " ").title()
                    table_data.append([
                        item_display,
                        "-",
                        "-",
                        "-",
                        f"₹ {cost:,.0f}"
                    ])

        # Create table
        table = Table(table_data, colWidths=[2.2 * inch, 1.2 * inch, 0.8 * inch, 1.2 * inch, 1.2 * inch])

        # Style table
        table.setStyle(
            TableStyle([
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

                # Body rows
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#f0f9ff")),
                ("TEXTCOLOR", (0, 1), (-1, -1), black),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),

                # Grid
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#e5e7eb")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f0f9ff"), white]),
            ])
        )

        elements.append(table)
        elements.append(Spacer(1, 0.3 * inch))
        return elements

    def _create_cost_breakdown_section(self, cost_data: Dict[str, Any]) -> list:
        """Create cost breakdown section."""
        elements = []

        heading = Paragraph("Cost Breakdown & Estimates", self.styles["CustomHeading"])
        elements.append(heading)

        # Extract cost components
        material_cost = cost_data.get("material_cost", 0)
        labor_cost = cost_data.get("labor_cost", 0)
        total_cost = cost_data.get("total_cost", 0)
        cost_per_sqft = cost_data.get("cost_per_sqft", 0)

        # Cost summary table
        cost_table_data = [
            ["Cost Component", "Amount (₹)"],
            ["Material Cost", f"{material_cost:,.2f}"],
            ["Labor Cost", f"{labor_cost:,.2f}"],
            ["Total Cost", f"{total_cost:,.2f}"],
            ["Cost per Sq.ft", f"{cost_per_sqft:,.2f}"],
        ]

        cost_table = Table(cost_table_data, colWidths=[3 * inch, 2.5 * inch])
        cost_table.setStyle(
            TableStyle([
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0891b2")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

                # Body rows
                ("BACKGROUND", (0, 1), (-1, -2), HexColor("#cffafe")),
                ("TEXTCOLOR", (0, 1), (-1, -2), black),
                ("ALIGN", (0, 1), (-1, -2), "RIGHT"),
                ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -2), 10),
                ("TOPPADDING", (0, 1), (-1, -2), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -2), 8),

                # Total row
                ("BACKGROUND", (0, -1), (-1, -1), HexColor("#164e63")),
                ("TEXTCOLOR", (0, -1), (-1, -1), white),
                ("ALIGN", (0, -1), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, -1), (-1, -1), 11),
                ("TOPPADDING", (0, -1), (-1, -1), 10),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 10),

                # Grid
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#e5e7eb")),
            ])
        )

        elements.append(cost_table)
        elements.append(Spacer(1, 0.2 * inch))

        # Additional costs if available
        hidden_costs = cost_data.get("hidden_costs", {})
        if hidden_costs:
            hidden_heading = Paragraph("Additional Costs & Adjustments", self.styles["CustomSubHeading"])
            elements.append(hidden_heading)

            hidden_data = [["Cost Type", "Amount (₹)"]]
            for key, value in hidden_costs.items():
                if isinstance(value, (int, float)):
                    cost_name = key.replace("_", " ").title()
                    hidden_data.append([cost_name, f"{value:,.2f}"])

            hidden_table = Table(hidden_data, colWidths=[3 * inch, 2.5 * inch])
            hidden_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#fbbf24")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), black),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, 1), (-1, -1), HexColor("#fef3c7")),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("GRID", (0, 0), (-1, -1), 1, HexColor("#e5e7eb")),
                ])
            )
            elements.append(hidden_table)

        elements.append(Spacer(1, 0.3 * inch))
        return elements

    def _create_metadata_section(self, metadata: Optional[Dict[str, Any]]) -> list:
        """Create metadata/details section."""
        elements = []

        if not metadata:
            return elements

        heading = Paragraph("Report Details", self.styles["CustomHeading"])
        elements.append(heading)

        metadata_data = [["Parameter", "Value"]]
        for key, value in metadata.items():
            if value:
                param_name = key.replace("_", " ").title()
                metadata_data.append([param_name, str(value)])

        metadata_table = Table(metadata_data, colWidths=[3 * inch, 2.5 * inch])
        metadata_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#6366f1")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#e0e7ff")),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#e5e7eb")),
            ])
        )

        elements.append(metadata_table)
        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def generate_pdf(
        self,
        project_description: str,
        floor_plan_base64: str,
        boq_data: Dict[str, Any],
        cost_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Generate a complete PDF report.

        Args:
            project_description: Description of the project
            floor_plan_base64: Base64 encoded floor plan image
            boq_data: Bill of Quantities data
            cost_data: Cost breakdown data
            metadata: Optional metadata about the generation

        Returns:
            PDF file as bytes
        """
        pdf_buffer = io.BytesIO()

        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A4),
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        # Build story (elements)
        story = []

        # Add header
        story.extend(self._create_header(project_description))

        # Add floor plan section
        if floor_plan_base64:
            story.extend(self._create_floor_plan_section(floor_plan_base64))
            story.append(PageBreak())

        # Add BOQ section
        story.extend(self._create_boq_table(boq_data, cost_data))

        # Add cost breakdown
        story.extend(self._create_cost_breakdown_section(cost_data))

        # Add metadata
        story.extend(self._create_metadata_section(metadata))

        # Add footer
        footer_text = f"<i>This is an automatically generated BOQ report. Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</i>"
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(footer_text, self.styles["Normal"]))

        # Build PDF
        doc.build(story)

        # Get PDF bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
