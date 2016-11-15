
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Comment(models.Model):
    parent = models.ForeignKey('self', null=True)
    text = models.TextField(verbose_name=_(u"Text"))
    node_history = models.CharField(max_length=255, db_index=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)

    @property
    def parent_history(self):
        return "" if not self.parent else self.parent.node_history

    def save(self, *args, **kwargs):
        self.datetime = datetime.datetime.now()
        descendants = Comment.objects.filter(parent=self.parent).count()
        new_part = self.parent_history + str(descendants)
        self.node_history = self.parent_history + new_part
        return super(Comment, self, *args, **kwargs).save()

    class Meta:
        ordering = '-node_history', '-created'
