"""Evaluate pervious pavement swap alternatives and cost comparisons."""

from __future__ import annotations

from decimal import Decimal

from .esu import annual_fee
from .models import Comparison, PerviousOption, Property, Surface, SurfaceMaterial
from .rates import EsuRate, load_material_costs

PERVIOUS_SUBSTITUTES: dict[SurfaceMaterial, list[SurfaceMaterial]] = {
    SurfaceMaterial.ASPHALT: [SurfaceMaterial.POROUS_ASPHALT],
    SurfaceMaterial.CONCRETE: [SurfaceMaterial.PERVIOUS_CONCRETE],
    SurfaceMaterial.PAVERS: [SurfaceMaterial.PERMEABLE_PAVERS],
    SurfaceMaterial.SHINGLE: [SurfaceMaterial.TURF],
    SurfaceMaterial.METAL: [SurfaceMaterial.TURF],
}


def eligible_surfaces(prop: Property) -> list:
    """Surfaces that could physically be converted to a pervious material."""
    substitute_materials = []
    for surface in prop.surfaces:
        if surface.material in PERVIOUS_SUBSTITUTES:
            substitute_materials.append(surface)
    return substitute_materials


def upfront_cost_delta(
    area_sqft: float,
    from_material: SurfaceMaterial,
    to_material: SurfaceMaterial,
) -> Decimal:
    """The EXTRA cost of choosing pervious over conventional."""
    costs = load_material_costs()
    from_cost = costs.get(from_material, Decimal(0))
    to_cost = costs.get(to_material, Decimal(0))
    return (to_cost - from_cost) * Decimal(area_sqft)


def evaluate_option(
    prop: Property, surface_label: str, to_material: SurfaceMaterial, rate: EsuRate
) -> PerviousOption:
    """Price a single swap."""
    current_fee = annual_fee(prop, rate)
    for surface in prop.surfaces:
        if surface.label == surface_label:
            if surface.material not in PERVIOUS_SUBSTITUTES:
                raise ValueError(f"Surface {surface_label} is not eligible for pervious swap")
            modified_prop = Property(
                surfaces=[s if s.label != surface_label else Surface(
                    kind=s.kind,
                    material=to_material,
                    area_sqft=s.area_sqft,
                    label=s.label,
                ) for s in prop.surfaces],
                municipality_id=prop.municipality_id,
                parcel_area_sqft=prop.parcel_area_sqft,
                address=prop.address,
            )
            modified_fee = annual_fee(modified_prop, rate)
            delta = upfront_cost_delta(surface.area_sqft, surface.material, to_material)
            annual_savings = current_fee.annual_fee - modified_fee.annual_fee
            return PerviousOption(
                surface_label=surface.label,
                from_material=surface.material,
                to_material=to_material,
                area_sqft=surface.area_sqft,
                upfront_cost_delta=delta,
                annual_fee_savings=annual_savings,
            )   
        

            
def compare(prop: Property, rate: EsuRate) -> Comparison:
    baseline = annual_fee(prop, rate)
    eligible = eligible_surfaces(prop)
    options = []

    for surface in eligible:
        # Evalutate swapping to its recommended pervious material
        to_material = PERVIOUS_SUBSTITUTES[surface.material][0]
        option = evaluate_option(prop, surface.label, to_material, rate)
        options.append(option)

    #create proposed property with all swaps applied
    mapping = {opt.surface_label: opt.to_material for opt in options}
    proposed_surfaces = []
    for s in prop.surfaces:
        if s.label not in mapping:
            swapped = Surface(
                kind=s.kind,
                material=s.material,
                area_sqft=s.area_sqft,
                label=s.label,
            )
            proposed_surfaces.append(swapped)
        else:
            s = Surface(
                kind=s.kind,
                material=mapping[s.label],
                area_sqft=s.area_sqft,
                label=s.label,
            )
            proposed_surfaces.append(s)

    proposed_prop = Property(
        surfaces=proposed_surfaces,
        municipality_id=prop.municipality_id,
        parcel_area_sqft=prop.parcel_area_sqft,
        address=prop.address
    )

    # get proposed fee
    proposed_fee = annual_fee(proposed_prop, rate)
    total_upfront = sum(opt.upfront_cost_delta for opt in options)
    total_savings = sum(opt.annual_fee_savings for opt in options)

    # Calculate payback
    payback = None if total_savings <= 0 else float(total_upfront / total_savings)

    return Comparison(
        baseline=baseline,
        proposed=proposed_fee,
        options=options,
        upfront_cost_delta=total_upfront,
        annual_savings=total_savings,
        simple_payback_years=payback,
    )
