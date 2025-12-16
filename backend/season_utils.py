def get_season(month):
    dry_months = ["December", "January", "February", "March", "April"]
    return "Dry" if month in dry_months else "Wet"
