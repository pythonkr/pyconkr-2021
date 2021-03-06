from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.forms import ModelChoiceField, ChoiceField
from django_summernote.widgets import SummernoteInplaceWidget
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from .models import Proposal, OpenReview, ProgramCategory, LightningTalk

from constance import config


class ProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

        self.fields['brief'].initial = config.CFP_BRIEF_TEMPLATE
        self.fields['desc'].initial = config.CFP_DESC_TEMPLATE
        self.fields['category'].queryset = ProgramCategory.objects.filter(visible=True)

    class Meta:
        model = Proposal
        fields = ('title', 'brief', 'desc', 'comment',
                  'difficulty', 'duration', 'language', 'category',)
        widgets = {
            'desc': SummernoteInplaceWidget(),
            'comment': SummernoteInplaceWidget(),
        }
        labels = {
            'title': _('Proposal title (required)'),
            'brief': _('Brief (required)'),
            'desc': _('Detailed description (required)'),
            'comment': _('Comment to reviewers (optional)'),
            'difficulty': _('Session difficulty'),
            'duration': _('Session duration'),
            'language': _('Session language'),
            'category': _('Category'),
        }


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}'


class LanguageChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj}'


class OpenReviewLanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OpenReviewLanguageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('next', _('Next')))
        self.fields['language'] = ChoiceField(choices=(
            ('N', '?????? ??????'),
            ('K', '?????????'),
            ('E', 'English'),
        ), help_text=_('?????? ????????? ????????? ?????? ????????? ???????????? ???????????????.'))

    class Meta:
        fields = ('language',)
        labels = {
            'language': _('??????'),
        }


class OpenReviewCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OpenReviewCategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('next', _('Next')))
        self.fields['category'] = CategoryChoiceField(label=_('????????????'),
                                                      queryset=ProgramCategory.objects.filter(visible=True).exclude(
                                                          proposal=None),
                                                      help_text=_('????????? ????????? ???????????????. ?????? ????????? ?????? ????????? ???????????? ????????????.')
                                                      )
        # ?????? ????????? ????????? ???????????? ????????? Hidden input ?????? (View?????? helper??? ????????? ??????)

    class Meta:
        model = OpenReview
        fields = ('category',)
        labels = {
            'category': _('???????????? ??????'),
        }


class OpenReviewCommentForm(forms.ModelForm):
    comment = forms.CharField(min_length=20, max_length=2000, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(OpenReviewCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', _('Save')))

    class Meta:
        model = OpenReview
        fields = ('comment',)
        labels = {
            'comment': _('Comment')
        }


class LightningTalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LightningTalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
        LT_N = config.LIGHTNING_TALK_N
        if len(LightningTalk.objects.filter(day=1)) >= LT_N:
            if len(LightningTalk.objects.filter(day=2)) < LT_N:
                self.fields['day'] = ChoiceField(choices=((2, _('?????????')),))
        else:
            if len(LightningTalk.objects.filter(day=2)) < LT_N:
                self.fields['day'] = ChoiceField(choices=((1, _('?????????')), (2, _('?????????')),))
            else:
                self.fields['day'] = ChoiceField(choices=((1, _('?????????')),))
        self.fields['video_url'].required = True

    class Meta:
        model = LightningTalk
        fields = ('title', 'video_url', 'slide_url', 'day', 'brief', 'comment',)
        labels = {
            'title': _('?????? ??????'),
            'video_url': _('?????? ?????? URL'),
            'slide_url': _('?????? ???????????? URL'),
            'day': _('?????? ??????'),
            'brief': _('?????? ?????? ??????'),
            'comment': _('????????????????????? ????????? ?????? ???'),
        }


class ProgramUpdateForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('title', 'introduction', 'slide_url',)
        labels = {
            'title': _('Proposal title (required)'),
            'introduction': _('?????? ?????? ??????'),
            'slide_url': _('?????? ?????? URL'),
        }
        widgets = {
            'introduction': SummernoteInplaceWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ProgramUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
