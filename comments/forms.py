from django import forms


class WriteMessageForm(forms.Form):
    """
    Write message form
    """
    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': "50", 'rows': "10", 'style': "resize:vertical;", }),
        label=u'Your message',
        required=True,
        help_text=u'I\'m a help text and I\'m very useful',
        )


class WriteReviewToMessageForm(forms.Form):
    """
    Write message form
    """
    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': "50", 'rows': "10", 'style': "resize:vertical;", }),
        label=u'Your message',
        required=True,
        )
    message_parent_id = forms.IntegerField(widget=forms.HiddenInput(),
                                           required=True)