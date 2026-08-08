# PrintFlow — Product Catalog

## Printing Services

### Offset Printing
Offset printing is PrintFlow's highest-quality option for large-volume jobs (500+ units).

**Supported formats:** PDF (preferred), AI, EPS, TIFF  
**Minimum resolution:** 300 DPI  
**Color modes:** CMYK only — RGB files will be auto-converted and may shift in color  
**Bleed:** 3mm bleed required on all sides  
**Fonts:** Must be embedded or outlined; missing fonts will cause the job to be rejected  
**Turnaround:** 5–7 business days standard; 3-day rush available on Pro and Enterprise plans  
**Minimum order:** 500 units  
**Maximum sheet size:** 720mm × 1020mm  

### Digital Printing
Digital printing is best for short runs (under 500 units) or personalized/variable-data jobs.

**Supported formats:** PDF, DOCX, PNG, JPEG, TIFF  
**Minimum resolution:** 150 DPI (300 DPI recommended)  
**Color modes:** RGB and CMYK both accepted  
**Bleed:** 3mm bleed recommended but not required  
**Turnaround:** 1–3 business days standard  
**Minimum order:** 1 unit  
**Maximum sheet size:** 330mm × 488mm (SRA3)  

### Wide Format Printing
Wide format covers banners, posters, vehicle wraps, and exhibition displays.

**Supported formats:** PDF, AI, PSD, PNG (at final print size)  
**Minimum resolution:** 72 DPI at full print size (150 DPI recommended for close-viewing pieces)  
**Color modes:** RGB accepted; internally converted to CMYK for printing  
**Turnaround:** 3–5 business days standard  
**Minimum order:** 1 unit  
**Maximum width:** 3200mm  

---

## File Submission

All files must be submitted through the PrintFlow portal or via the API. Email submissions are not accepted.

**Portal upload limit:** 500 MB per file  
**API upload limit:** 2 GB per file (Pro and Enterprise only)  
**Accepted archive formats for bulk upload:** ZIP, TAR (files inside must still meet per-format requirements)  

### Pre-flight Check
PrintFlow automatically runs a pre-flight check on every uploaded file. Pre-flight checks verify:
- Bleed dimensions
- Font embedding (for PDF/AI/EPS)
- Color mode
- Resolution
- Page count vs. ordered quantity

Pre-flight failures are reported immediately in the portal with a specific error code. The job does not enter the production queue until the file passes pre-flight.

---

## Variable Data Printing (VDP)

Variable data printing allows different text, images, or barcodes on each printed unit — used for personalized direct mail, name badges, QR code campaigns, etc.

**Availability:** Digital printing only; not available for offset  
**Data format:** CSV (required); one row per unit  
**Template format:** PDF with tagged fields using PrintFlow's VDP markup syntax (`{{field_name}}`)  
**Maximum fields per template:** 50  
**Maximum rows per CSV:** 100,000  
**Availability by plan:** Pro and Enterprise only  

---

## Proofing

### Digital Proof
A digital proof is a screen-resolution PDF preview of your job before it goes to production. Available on all plans at no extra cost.

### Physical Proof
A physical proof is a single printed copy shipped to you before the full run. Physical proofs cost $25 and add 2 business days to the turnaround.

**Availability:** Pro and Enterprise plans only  

---

## Finishing Options

| Option | Description | Available on |
|---|---|---|
| Binding | Saddle stitch, perfect bind, coil | All plans |
| Lamination | Gloss, matte, soft-touch | All plans |
| Die cutting | Custom shapes from a template library | Pro, Enterprise |
| Custom die cutting | Fully custom die from your artwork | Enterprise only |
| Foil stamping | Gold, silver, holographic | Enterprise only |
| Embossing / debossing | Raised or recessed surface | Enterprise only |
