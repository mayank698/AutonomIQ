from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse


def compress(request):
    if request.method == "POST":
        user = request.user
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data["original_img"]
            quality = form.cleaned_data["quality"]

            compressed_image = form.save(commit=False)
            compressed_image.user = user

            # Perform compression
            img = Image.open(original_img)
            output_format = img.format
            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)

            # save the compressed image inside the model
            compressed_image.compressed_images.save(
                f"Compressed_{original_img}", buffer
            )
            response = HttpResponse(
                buffer.getvalue(),
                content_type=f"image/{output_format.lower()}",  # type:ignore
            )
            response["Content-Disposition"] = (
                f"attachement; filename=compressed_{original_img}"
            )
            return response

    else:
        form = CompressImageForm()
        context = {"form": form}
        return render(request, "image_compressor/compressor.html", context)
