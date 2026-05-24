def site_stats(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        return {"user_credits": request.user.profile.credits}
    return {"user_credits": None}
