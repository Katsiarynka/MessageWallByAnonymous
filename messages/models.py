from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
import random


class Message(models.Model):
    text = models.TextField(verbose_name=_(u"Text"))
    date_and_time = models.DateTimeField(verbose_name=_(u"Date and time"), db_index=True)
    parent = models.ForeignKey('self', null=True)
    node_history = models.CharField(max_length=255, db_index=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.date_and_time = datetime.datetime.now()
        parent = self.parent
        self.node_history = ("" if (parent==None) else parent.node_history)+unicode(len(Message.objects.filter(parent=parent)))+"-"
        return  super(Message, self).save()

    def in__dict(self, args):
        dict = {
            'id': self.id,
            'text': self.text,
            'date_and_time': str(self.date_and_time),}
        dict.update(args)
        return dict