---
name: architectural-line-lock
description: Restyle architectural site plans, drawings, and maps while preserving the exact positions of existing lines, boundaries, annotations, and geometry. Use when recoloring or adding textures to an existing drawing under a strict line-preservation requirement.
---

# Architectural line lock

Treat all existing geometry and line locations as fixed unless the user explicitly permits an identified change. Preserve the source file and create versioned outputs. The user's reference image is for visual treatment, not a source of replacement geometry.

## Choose a verifiable workflow

- Prefer the original editable CAD, vector, or layered drawing: keep its existing objects, coordinates, linework, labels, and boundaries untouched above separately edited color and texture layers. Do not rasterize the native master or alter its objects. Export a separate presentation image and, when available, the editable layered result.
- For a raster drawing, use an exact-size registered source and a separate, user-supplied or carefully reviewed binary line mask. White pixels identify source pixels to retain; black pixels identify background eligible for visual change. Include critical text, boundaries, symbols and other protected details. Do not treat automatic thresholding as proof that every line is captured. If the user has not supplied a mask, derive a candidate for review and mark completeness unverified until every important line is checked.
- Create color and texture on independent layers; generative tools can propose visual treatment, but their output alone cannot guarantee coordinates or counts. Use `scripts/lock_pixels.py` to restore selected source pixels onto an already registered, same-resolution treatment. Never resize, crop, rotate, or warp a treatment to force a match. If the generated image has different dimensions or a shifted view, report the mismatch and use a genuinely registered layer or an editable source instead.
- Run the helper's verification against the same source, output and reviewed mask. The exact check verifies RGB pixels inside the mask only; it does not prove that the mask covers every line, nor that geometry outside the mask stayed unchanged. Visually inspect overlaps and protected features against the source. For a native file, also verify the protected objects or exported line layer against the baseline.
- Only say line positions are confirmed when the protected-source layer is unchanged, correctly registered, complete for the scope, and the checks pass. Otherwise label the result as a concept, identify what is unverified, and do not claim exact preservation. Preserve the existing scene/viewpoint and building footprints; do not add building heights to a plan without a user decision.

## Visual direction

If requested, apply muted warm pastel color fields, textured green landscape, restrained flat shadows and collage-like vegetation without borrowing another project's composition or modifying the user's design. Maintain text readability and distinguish design evidence from generated decorative texture. Preserve original dimensions and output a lossless PNG where feasible.

## Usage

```text
python scripts/lock_pixels.py compose --source original.png --treatment treatment.png --mask approved_mask.png --output locked.png
python scripts/lock_pixels.py verify --source original.png --output locked.png --mask approved_mask.png
```

The source, treatment and mask must have identical pixel dimensions. The helper requires Pillow. The output cannot replace any input and must not already exist. Save the mask and original alongside the project record, together with the source hash, prompt, output, verification result, and known limits.
