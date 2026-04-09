async def paint_coverage_calculator(
    ceiling_height_in_m: float,
    room_length_in_m: float,
    room_width_in_m: float,
    num_windows: int,
    num_doors: int,
):
    """Calculates the square-meters of paint required for the walls of a room.

    Args:
        ceiling_height_in_m: float - ceiling height in meters
        room_length_in_m: float - Room length in meters
        room_width_in_m: float - Room width in meters
        num_windows: int - Number of windows
        num_doors: int - Number of doors

    Returns a dictionary with:
        {"square_meters": float - Square meters of paint required}
    """

    sq_meters = (
        (((2 * room_length_in_m) + (2 * room_width_in_m)) * ceiling_height_in_m)
        - (1.5 * num_windows)
        - (2 * num_doors)
    )
    return {"square_meters": sq_meters}
