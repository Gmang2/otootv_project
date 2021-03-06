from django.db import models
from vod.models import Video, Comment

from django_summernote import fields as summer_fields

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# -------------------- 신고 --------------------
class VideoReport(models.Model):
    Category = (
        ('1', 'Report1'),
        ('2', 'Report2'),
        ('1', '신고1'),
        ('2', '신고2'),
    )

    # 1(User 시청자) : M(Report)       #신고 하는사람
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='service_user_videoreports', verbose_name=_('User'))
    # 1(Video) : M(Report)                             #신고 비디오
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='service_video_videoreports',
                                    verbose_name=_('Video'))
    category = models.CharField(_('Category'),  choices=Category, max_length=20)
    content = models.CharField(_('Content'),max_length=50, blank=True)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)

    class Meta:
        verbose_name = _(' Video Report')
        verbose_name_plural = _(' Video Reports')
        ordering = ['-create_date']


class CommentReport(models.Model):
    Category = (
        ('1', 'Report1'),
        ('2', 'Report2'),
        ('1', '신고1'),
        ('2', '신고2'),
    )

    # 1(User 시청자. 진행자(채널 주인) : M(Report)       #신고 하는사람
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='service_user_commentreports', verbose_name=_('User'))
    # 1(Comment) : M(Report)                             #신고 댓글
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='service_comment_commentreports',
                                    verbose_name=_('Comment'))
    category = models.CharField(_('Category'), choices=Category, max_length=20)
    content = models.CharField(_('Content'), max_length=50, blank=True)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Comment Report')
        verbose_name_plural = _('Comment Reports')
        ordering = ['-create_date']

# -------------------- 도움말 --------------------


class Help(models.Model):
    question = models.CharField(_('Question'), max_length=100)
    content = summer_fields.SummernoteTextField(verbose_name=_('Content'), blank=True)
    update_date = models.DateTimeField(_('Update Date'), auto_now=True)

    belong_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,
                                  related_name='service_belong_to_helps',  verbose_name=_('Belong To'))

    class Meta:
        verbose_name = _('Help')
        verbose_name_plural = _('Helps')


    def __str__(self):
        return self.question


# -------------------- 문의하기 --------------------

class Inquiry(models.Model):
    # 1(User 로그인) : N(Inquiry)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='service_user_inquiries', verbose_name=_('User'))

    title = models.CharField(_('Title'), max_length=100)
    content = summer_fields.SummernoteTextField(verbose_name=_('Content'))
    views = models.PositiveIntegerField(_('Views'), default=0)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Inquire')
        verbose_name_plural = _('Inquires')
        ordering = ['-update_date']

    def __str__(self):
        return self.title


class Reply(models.Model):
    # 1(User 관리자) : N(Reply)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='service_user_replies',  verbose_name=_('Staff User'))
    # 1(Inquiry) : 1(Reply)
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='service_inquiry_reply',  verbose_name=_('Inquire'))

    content = summer_fields.SummernoteTextField(verbose_name=_('Content'))
    update_date = models.DateTimeField(_('Update date'), auto_now=True)

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')


