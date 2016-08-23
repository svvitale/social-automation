from django.shortcuts import render_to_response
from social.pipeline.partial import partial


@partial
def get_email_for_twitter_acct(backend, response, details, user, *args, **kwargs):
    if backend.name == 'twitter':
        data = backend.strategy.request_data()

        email_param = data.get('email')

        if user.is_authenticated():
            details['email'] = user.email
        elif email_param:
            details['email'] = email_param
        else:
            return render_to_response('prompt_for_email.html', {
                'name': response.get('name')
            })

        # Update the user's details with the email address
        return {'details': details}
