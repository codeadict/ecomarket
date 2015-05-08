def activities_count(request):
    if request.user.is_authenticated():
        return {
            'activities_count': request.user.get_profile().activities_count
        }
    else:
        return {}