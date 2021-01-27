from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'tool/customPage.html',
                  {'text': 'Страница не найдена'}, status=404)


def server_error(request):
    return render(
        request, 'tool/customPage.html',
        {'text': 'Ошибка на сервере, попробуйте обновить страницу'},
        status=500)
