from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactUsForm
from .models import ContactUs


@login_required
def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact_message = ContactUs(
                user=request.user,
                message=form.cleaned_data["message"],
            )
            contact_message.save()
            messages.success(
                request, "Thank you for your message. We'll get back to you shortly."
            )
            return redirect("users:contact-us")
    else:
        form = ContactUsForm()

    return render(request, "users/base_contact_us.html", {"form": form})
