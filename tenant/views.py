from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tenant.forms import EditProfileForm


def get_base_context(title, sign_in_button=True):
    context = {

        'background_color': '#FFF6E6',
        'header_color': '#FFA200',
        'header_text_color1': '#FFF6E6',
        'header_text_color2': '#CC8200',
        'footer_color': '#DB971F',
        'footer_text_color1': '#FFF6E6',
        'footer_text_color2': '#CC8200',

        'title': title,
        'if_sign_but': sign_in_button,

    }
    return context


@login_required
def profile(request):
    context = get_base_context('Profile')
    context.update({
        'user': request.user,
    })
    if request.method == 'POST':
        editprof = EditProfileForm(request.POST, instance=request.user)
        if editprof.is_valid():
            editprof.save()
            context.update({
                'editprof': editprof,
            })
        return redirect('profile')
    else:
        editprof = EditProfileForm(instance=request.user)

    context.update({
        'editprof': editprof,
    })

    return render(request, 'pages/tenant/profile.html', context)
