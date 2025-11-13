from django.shortcuts import render, redirect
from .utils import get_custom_models
from uploads.models import Upload
from django.conf import settings
from .tasks import import_data_task, export_data_task
from django.contrib import messages
from .utils import check_csv_errors


def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # get relative path
        relative_path = str(upload.file.url)
        baseURL = str(settings.BASE_DIR)

        full_path = baseURL + relative_path

        # check csv errors
        try:
            check_csv_errors(full_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("import_data")
        # handling import data task here.
        import_data_task.delay(full_path, model_name)

        # showing messages to the user
        messages.success(
            request, "Your data is being imported, you'll be notified once it is done."
        )
        return redirect("import_data")
    else:
        custom_models = get_custom_models()
        context = {"custom_models": custom_models}
    return render(request, "dataentry/importData.html", context)


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get("model_name")

        # call the export data task
        export_data_task.delay(model_name)
        # showing messages to the user
        messages.success(
            request, "Your data is being exported, you'll be notified once it is done."
        )
        return redirect("export_data")
    else:
        custom_models = get_custom_models()
        context = {"custom_models": custom_models}

    return render(request, "dataentry/export_data.html", context)
