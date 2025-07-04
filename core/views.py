from django.shortcuts import render


def handler404(request, exception):
    """
    Custom view for 404 Not Found errors.
    """
    return render(request, '404.html', status=404)
