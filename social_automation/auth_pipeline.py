from django.shortcuts import render_to_response
from social.pipeline.partial import partial


@partial
def get_email_for_twitter_acct(backend, response, details, *args, **kwargs):
    if backend.name == 'twitter':
        data = backend.strategy.request_data()

        if not data.get('email'):
            return render_to_response('prompt_for_email.html', {
                'name': response.get('name')
            })

        # Update the user's details with the email address provided
        details['email'] = data.get('email')
        return {'details': details}
